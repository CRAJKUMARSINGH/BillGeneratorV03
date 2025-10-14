#!/usr/bin/env python3
"""
Automated Test Runner for BillGenerator Application
Programmatically tests all input files and generates comprehensive test reports
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime
from pathlib import Path
import pandas as pd
import tempfile
import zipfile
from typing import Dict, List, Any, Optional

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

try:
    from excel_processor import ExcelProcessor
    from latex_generator import LaTeXGenerator
    from pdf_merger import PDFMerger
    from utils import validate_excel_file, get_timestamp, sanitize_filename
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are in the src directory")
    sys.exit(1)

class TestResult:
    """Class to store individual test results"""
    def __init__(self, filename: str):
        self.filename = filename
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = "pending"  # pending, running, success, error
        self.error_message = None
        self.warnings = []
        self.processed_data = {}
        self.generated_docs = {}
        self.file_size = 0
        self.sheets_found = []
        self.validation_result = {}
        self.output_files = []
        
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'filename': self.filename,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'status': self.status,
            'error_message': self.error_message,
            'warnings': self.warnings,
            'file_size_mb': round(self.file_size / (1024 * 1024), 2),
            'sheets_found': self.sheets_found,
            'validation_result': self.validation_result,
            'output_files_count': len(self.output_files),
            'processed_data_summary': self.get_data_summary()
        }
    
    def get_data_summary(self):
        """Get summary of processed data"""
        summary = {}
        if 'title' in self.processed_data:
            summary['project_name'] = self.processed_data['title'].get('project_name', 'N/A')
            summary['contractor_name'] = self.processed_data['title'].get('contractor_name', 'N/A')
        
        if 'bill_quantity' in self.processed_data:
            summary['bill_items_count'] = len(self.processed_data['bill_quantity'])
            summary['bill_total'] = self.processed_data.get('totals', {}).get('bill_quantity_total', 0)
        
        if 'extra_items' in self.processed_data:
            summary['extra_items_count'] = len(self.processed_data['extra_items'])
            summary['extra_total'] = self.processed_data.get('totals', {}).get('extra_items_total', 0)
        
        summary['grand_total'] = self.processed_data.get('totals', {}).get('grand_total', 0)
        return summary

class AutomatedTestRunner:
    """Main test runner class"""
    
    def __init__(self, test_files_dir: str = "test_input_files", output_dir: str = "test_results"):
        self.test_files_dir = Path(test_files_dir)
        self.output_dir = Path(output_dir)
        self.test_results: List[TestResult] = []
        self.start_time = None
        self.end_time = None
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize processors
        self.excel_processor = None
        self.latex_generator = None
        self.pdf_merger = None
        
    def get_test_files(self) -> List[Path]:
        """Get all Excel test files"""
        if not self.test_files_dir.exists():
            raise FileNotFoundError(f"Test files directory not found: {self.test_files_dir}")
        
        excel_files = list(self.test_files_dir.glob("*.xlsx")) + list(self.test_files_dir.glob("*.xls"))
        if not excel_files:
            raise FileNotFoundError(f"No Excel files found in {self.test_files_dir}")
        
        return sorted(excel_files)
    
    def run_single_test(self, file_path: Path) -> TestResult:
        """Run test on a single file"""
        result = TestResult(file_path.name)
        result.start_time = datetime.now()
        result.file_size = file_path.stat().st_size
        
        print(f"\n{'='*60}")
        print(f"🧪 Testing: {file_path.name}")
        print(f"📁 File Size: {result.file_size / (1024*1024):.2f} MB")
        print(f"⏰ Start Time: {result.start_time.strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        try:
            result.status = "running"
            
            # Step 1: Validate file
            print("📋 Step 1: Validating file structure...")
            with open(file_path, 'rb') as f:
                validation_result = validate_excel_file(f)
                result.validation_result = validation_result
            
            if not validation_result['valid']:
                result.status = "error"
                result.error_message = f"Validation failed: {validation_result['error']}"
                print(f"❌ {result.error_message}")
                return result
            
            print("✅ File validation passed")
            
            # Step 2: Process Excel file
            print("📊 Step 2: Processing Excel data...")
            with open(file_path, 'rb') as f:
                self.excel_processor = ExcelProcessor(f)
                processed_data = self.excel_processor.process_all_sheets()
            
            if not processed_data:
                result.status = "error"
                result.error_message = "Failed to process Excel file"
                print("❌ Excel processing failed")
                return result
            
            result.processed_data = processed_data
            result.sheets_found = list(processed_data.keys())
            print(f"✅ Excel processing completed. Sheets: {result.sheets_found}")
            
            # Step 3: Generate documents
            print("📄 Step 3: Generating documents...")
            
            # Generate LaTeX documents
            self.latex_generator = LaTeXGenerator()
            latex_docs = self.latex_generator.generate_all_documents(processed_data)
            result.generated_docs['latex'] = list(latex_docs.keys())
            
            # Generate HTML documents (simplified)
            html_docs = self.generate_html_documents(processed_data)
            result.generated_docs['html'] = list(html_docs.keys())
            
            print(f"✅ Documents generated: {len(latex_docs)} LaTeX, {len(html_docs)} HTML")
            
            # Step 4: Test PDF generation (if possible)
            print("📑 Step 4: Testing PDF generation...")
            try:
                self.pdf_merger = PDFMerger()
                # Test HTML to PDF conversion
                html_pdfs = self.pdf_merger.convert_html_to_pdf(html_docs)
                result.generated_docs['html_pdfs'] = list(html_pdfs.keys())
                print(f"✅ HTML PDFs generated: {len(html_pdfs)}")
            except Exception as pdf_error:
                result.warnings.append(f"PDF generation failed: {str(pdf_error)}")
                print(f"⚠️ PDF generation failed: {str(pdf_error)}")
            
            # Step 5: Create test output package
            print("📦 Step 5: Creating output package...")
            output_files = self.create_test_output_package(
                file_path, processed_data, latex_docs, html_docs, result
            )
            result.output_files = output_files
            
            result.status = "success"
            print("✅ Test completed successfully!")
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            result.warnings.append(f"Exception: {traceback.format_exc()}")
            print(f"❌ Test failed: {str(e)}")
            print(f"📝 Traceback: {traceback.format_exc()}")
        
        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - result.start_time).total_seconds()
            print(f"⏱️ Duration: {result.duration:.2f} seconds")
        
        return result
    
    def generate_html_documents(self, processed_data: Dict) -> Dict:
        """Generate HTML documents (simplified version)"""
        html_docs = {}
        
        # Generate basic HTML documents
        templates = ['first_page', 'deviation_statement', 'extra_items', 'certificate_ii', 'certificate_iii']
        
        for template in templates:
            try:
                # Create basic HTML content
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{template.replace('_', ' ').title()}</title>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1>{template.replace('_', ' ').title()}</h1>
                    <p>Generated from: {processed_data.get('title', {}).get('project_name', 'Unknown Project')}</p>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Status: Test Document</p>
                </body>
                </html>
                """
                html_docs[template] = html_content
            except Exception as e:
                print(f"⚠️ Failed to generate HTML for {template}: {str(e)}")
        
        return html_docs
    
    def create_test_output_package(self, file_path: Path, processed_data: Dict, 
                                 latex_docs: Dict, html_docs: Dict, result: TestResult) -> List[str]:
        """Create test output package"""
        output_files = []
        
        try:
            # Create timestamped output directory
            timestamp = get_timestamp()
            project_name = processed_data.get('title', {}).get('project_name', 'TestProject')
            safe_project_name = sanitize_filename(project_name)
            output_dir_name = f"{safe_project_name}_{timestamp}_TestOutput"
            output_path = self.output_dir / output_dir_name
            output_path.mkdir(exist_ok=True)
            
            # Save processed data as JSON
            data_file = output_path / "processed_data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
            output_files.append(str(data_file))
            
            # Save LaTeX documents
            latex_dir = output_path / "latex_documents"
            latex_dir.mkdir(exist_ok=True)
            for doc_name, content in latex_docs.items():
                latex_file = latex_dir / f"{doc_name}.tex"
                with open(latex_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                output_files.append(str(latex_file))
            
            # Save HTML documents
            html_dir = output_path / "html_documents"
            html_dir.mkdir(exist_ok=True)
            for doc_name, content in html_docs.items():
                html_file = html_dir / f"{doc_name}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                output_files.append(str(html_file))
            
            # Save test summary
            summary_file = output_path / "test_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            output_files.append(str(summary_file))
            
            print(f"📁 Output package created: {output_path}")
            
        except Exception as e:
            result.warnings.append(f"Failed to create output package: {str(e)}")
            print(f"⚠️ Output package creation failed: {str(e)}")
        
        return output_files
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests on all files"""
        print("🚀 Starting Automated Test Suite")
        print(f"📁 Test Files Directory: {self.test_files_dir}")
        print(f"📁 Output Directory: {self.output_dir}")
        
        self.start_time = datetime.now()
        
        try:
            test_files = self.get_test_files()
            print(f"📋 Found {len(test_files)} test files")
            
            for i, file_path in enumerate(test_files, 1):
                print(f"\n🔄 Progress: {i}/{len(test_files)}")
                result = self.run_single_test(file_path)
                self.test_results.append(result)
                
                # Brief pause between tests
                time.sleep(1)
            
            self.end_time = datetime.now()
            total_duration = (self.end_time - self.start_time).total_seconds()
            
            print(f"\n{'='*60}")
            print(f"🏁 Test Suite Completed!")
            print(f"⏱️ Total Duration: {total_duration:.2f} seconds")
            print(f"📊 Tests Run: {len(self.test_results)}")
            print(f"✅ Successful: {sum(1 for r in self.test_results if r.status == 'success')}")
            print(f"❌ Failed: {sum(1 for r in self.test_results if r.status == 'error')}")
            print(f"{'='*60}")
            
            return self.generate_test_report()
            
        except Exception as e:
            print(f"❌ Test suite failed: {str(e)}")
            return {'error': str(e), 'traceback': traceback.format_exc()}
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        report = {
            'test_suite_info': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat(),
                'total_duration': (self.end_time - self.start_time).total_seconds(),
                'total_tests': len(self.test_results),
                'successful_tests': sum(1 for r in self.test_results if r.status == 'success'),
                'failed_tests': sum(1 for r in self.test_results if r.status == 'error'),
                'success_rate': (sum(1 for r in self.test_results if r.status == 'success') / len(self.test_results)) * 100
            },
            'test_results': [result.to_dict() for result in self.test_results],
            'summary_statistics': self.calculate_summary_statistics(),
            'recommendations': self.generate_recommendations()
        }
        
        # Save report to file
        report_file = self.output_dir / f"test_report_{get_timestamp()}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Test report saved: {report_file}")
        
        return report
    
    def calculate_summary_statistics(self) -> Dict[str, Any]:
        """Calculate summary statistics"""
        successful_tests = [r for r in self.test_results if r.status == 'success']
        failed_tests = [r for r in self.test_results if r.status == 'error']
        
        stats = {
            'file_size_stats': {
                'min_mb': min(r.file_size for r in self.test_results) / (1024*1024),
                'max_mb': max(r.file_size for r in self.test_results) / (1024*1024),
                'avg_mb': sum(r.file_size for r in self.test_results) / len(self.test_results) / (1024*1024)
            },
            'processing_time_stats': {
                'min_seconds': min(r.duration for r in self.test_results if r.duration),
                'max_seconds': max(r.duration for r in self.test_results if r.duration),
                'avg_seconds': sum(r.duration for r in self.test_results if r.duration) / len(self.test_results)
            },
            'sheets_analysis': {},
            'document_generation_stats': {
                'total_latex_docs': sum(len(r.generated_docs.get('latex', [])) for r in successful_tests),
                'total_html_docs': sum(len(r.generated_docs.get('html', [])) for r in successful_tests),
                'total_pdf_docs': sum(len(r.generated_docs.get('html_pdfs', [])) for r in successful_tests)
            }
        }
        
        # Analyze sheet patterns
        all_sheets = []
        for result in self.test_results:
            all_sheets.extend(result.sheets_found)
        
        from collections import Counter
        sheet_counts = Counter(all_sheets)
        stats['sheets_analysis'] = dict(sheet_counts)
        
        return stats
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if r.status == 'error']
        if failed_tests:
            recommendations.append(f"⚠️ {len(failed_tests)} tests failed. Review error messages for common issues.")
        
        # Check for common validation issues
        validation_errors = [r.error_message for r in failed_tests if 'validation' in r.error_message.lower()]
        if validation_errors:
            recommendations.append("📋 Multiple validation errors detected. Check Excel file structure and required sheets.")
        
        # Check processing time
        avg_time = sum(r.duration for r in self.test_results if r.duration) / len(self.test_results)
        if avg_time > 30:
            recommendations.append("⏱️ Average processing time is high. Consider optimizing file sizes or processing logic.")
        
        # Check file sizes
        large_files = [r for r in self.test_results if r.file_size > 10 * 1024 * 1024]  # > 10MB
        if large_files:
            recommendations.append(f"📁 {len(large_files)} large files detected. Consider file size optimization.")
        
        if not recommendations:
            recommendations.append("✅ All tests passed successfully! System is working optimally.")
        
        return recommendations

def main():
    """Main function to run automated tests"""
    print("🧪 BillGenerator Automated Test Suite")
    print("=" * 50)
    
    try:
        # Initialize test runner
        test_runner = AutomatedTestRunner()
        
        # Run all tests
        report = test_runner.run_all_tests()
        
        # Display summary
        print("\n📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {report['test_suite_info']['total_tests']}")
        print(f"Successful: {report['test_suite_info']['successful_tests']}")
        print(f"Failed: {report['test_suite_info']['failed_tests']}")
        print(f"Success Rate: {report['test_suite_info']['success_rate']:.1f}%")
        print(f"Total Duration: {report['test_suite_info']['total_duration']:.2f} seconds")
        
        print("\n📋 RECOMMENDATIONS")
        print("=" * 50)
        for rec in report['recommendations']:
            print(f"• {rec}")
        
        print(f"\n📁 Detailed report saved in: {test_runner.output_dir}")
        
        return report
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        print(f"📝 Traceback: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    main()
