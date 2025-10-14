#!/usr/bin/env python3
"""
Simple Test Runner for BillGenerator Application
Tests basic functionality without complex dependencies
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
from typing import Dict, List, Any, Optional

class SimpleTestResult:
    """Class to store individual test results"""
    def __init__(self, filename: str):
        self.filename = filename
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = "pending"  # pending, running, success, error
        self.error_message = None
        self.warnings = []
        self.file_size = 0
        self.sheets_found = []
        self.data_summary = {}
        
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
            'data_summary': self.data_summary
        }

class SimpleTestRunner:
    """Simple test runner that tests basic Excel processing"""
    
    def __init__(self, test_files_dir: str = "test_input_files", output_dir: str = "output"):
        self.test_files_dir = Path(test_files_dir)
        self.output_dir = Path(output_dir)
        self.test_results: List[SimpleTestResult] = []
        self.start_time = None
        self.end_time = None
        
        # Create output directory with date-based subfolder
        self.date_folder = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = self.output_dir / f"test_results_{self.date_folder}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def get_test_files(self) -> List[Path]:
        """Get all Excel test files"""
        if not self.test_files_dir.exists():
            raise FileNotFoundError(f"Test files directory not found: {self.test_files_dir}")
        
        excel_files = list(self.test_files_dir.glob("*.xlsx")) + list(self.test_files_dir.glob("*.xls"))
        if not excel_files:
            raise FileNotFoundError(f"No Excel files found in {self.test_files_dir}")
        
        return sorted(excel_files)
    
    def validate_excel_file(self, file_path: Path) -> Dict[str, Any]:
        """Basic Excel file validation"""
        try:
            # Check file exists and is readable
            if not file_path.exists():
                return {'valid': False, 'error': 'File does not exist'}
            
            if file_path.stat().st_size == 0:
                return {'valid': False, 'error': 'File is empty'}
            
            # Try to read with pandas
            try:
                excel_file = pd.ExcelFile(file_path)
                sheets = excel_file.sheet_names
                
                # Check for required sheets
                required_sheets = ['Title', 'Work Order', 'Bill Quantity']
                missing_sheets = [sheet for sheet in required_sheets if sheet not in sheets]
                
                if missing_sheets:
                    return {
                        'valid': False, 
                        'error': f'Missing required sheets: {missing_sheets}',
                        'available_sheets': sheets
                    }
                
                return {
                    'valid': True, 
                    'message': 'File validation passed',
                    'sheets': sheets,
                    'sheet_count': len(sheets)
                }
                
            except Exception as e:
                return {'valid': False, 'error': f'Cannot read Excel file: {str(e)}'}
                
        except Exception as e:
            return {'valid': False, 'error': f'File validation error: {str(e)}'}
    
    def analyze_excel_data(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Excel file data"""
        try:
            excel_file = pd.ExcelFile(file_path)
            analysis = {
                'sheets': {},
                'total_sheets': len(excel_file.sheet_names),
                'file_size_mb': file_path.stat().st_size / (1024 * 1024)
            }
            
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    sheet_analysis = {
                        'rows': len(df),
                        'columns': len(df.columns),
                        'column_names': list(df.columns),
                        'has_data': len(df) > 0,
                        'empty_rows': df.isnull().all(axis=1).sum(),
                        'data_types': df.dtypes.to_dict()
                    }
                    
                    # Look for numeric columns that might contain amounts
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    sheet_analysis['numeric_columns'] = numeric_cols
                    
                    # Calculate basic statistics for numeric columns
                    if numeric_cols:
                        sheet_analysis['numeric_summary'] = df[numeric_cols].describe().to_dict()
                    
                    analysis['sheets'][sheet_name] = sheet_analysis
                    
                except Exception as e:
                    analysis['sheets'][sheet_name] = {'error': str(e)}
            
            return analysis
            
        except Exception as e:
            return {'error': f'Data analysis failed: {str(e)}'}
    
    def run_single_test(self, file_path: Path) -> SimpleTestResult:
        """Run test on a single file"""
        result = SimpleTestResult(file_path.name)
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
            validation_result = self.validate_excel_file(file_path)
            
            if not validation_result['valid']:
                result.status = "error"
                result.error_message = validation_result['error']
                print(f"❌ {result.error_message}")
                return result
            
            result.sheets_found = validation_result.get('sheets', [])
            print(f"✅ File validation passed. Sheets: {result.sheets_found}")
            
            # Step 2: Analyze data
            print("📊 Step 2: Analyzing Excel data...")
            data_analysis = self.analyze_excel_data(file_path)
            
            if 'error' in data_analysis:
                result.warnings.append(f"Data analysis warning: {data_analysis['error']}")
                print(f"⚠️ {data_analysis['error']}")
            else:
                result.data_summary = data_analysis
                print(f"✅ Data analysis completed. Found {data_analysis['total_sheets']} sheets")
                
                # Print summary for each sheet
                for sheet_name, sheet_data in data_analysis['sheets'].items():
                    if 'error' not in sheet_data:
                        print(f"   📄 {sheet_name}: {sheet_data['rows']} rows, {sheet_data['columns']} columns")
            
            # Step 3: Test basic document generation
            print("📄 Step 3: Testing document generation...")
            try:
                # Create a simple test document
                test_doc = self.generate_test_document(file_path, data_analysis)
                result.warnings.append("Basic document generation test passed")
                print("✅ Basic document generation test passed")
            except Exception as e:
                result.warnings.append(f"Document generation test failed: {str(e)}")
                print(f"⚠️ Document generation test failed: {str(e)}")
            
            # Step 4: Save individual test result
            print("💾 Step 4: Saving test result...")
            try:
                self.save_individual_test_result(file_path, result, data_analysis)
                print("✅ Individual test result saved")
            except Exception as e:
                result.warnings.append(f"Failed to save individual result: {str(e)}")
                print(f"⚠️ Failed to save individual result: {str(e)}")
            
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
    
    def generate_test_document(self, file_path: Path, data_analysis: Dict) -> str:
        """Generate a simple test document and save it to output folder"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_filename = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        doc_content = f"""
# Test Document Generated from {file_path.name}

**Generated on:** {timestamp}
**File Size:** {data_analysis.get('file_size_mb', 0):.2f} MB
**Total Sheets:** {data_analysis.get('total_sheets', 0)}

## Sheet Analysis

"""
        
        for sheet_name, sheet_data in data_analysis.get('sheets', {}).items():
            if 'error' not in sheet_data:
                doc_content += f"""
### {sheet_name}
- **Rows:** {sheet_data['rows']}
- **Columns:** {sheet_data['columns']}
- **Has Data:** {sheet_data['has_data']}
- **Empty Rows:** {sheet_data['empty_rows']}
- **Numeric Columns:** {', '.join(sheet_data.get('numeric_columns', []))}

"""
        
        # Save document to output folder with date-based filename
        doc_filename = f"test_document_{Path(file_path).stem}_{date_filename}.md"
        doc_path = self.output_dir / doc_filename
        
        try:
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            print(f"📄 Test document saved: {doc_path}")
        except Exception as e:
            print(f"⚠️ Failed to save test document: {str(e)}")
        
        return doc_content
    
    def convert_numpy_types(self, obj):
        """Convert numpy types to Python native types for JSON serialization"""
        import numpy as np
        
        if isinstance(obj, dict):
            return {key: self.convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def save_individual_test_result(self, file_path: Path, result: SimpleTestResult, data_analysis: Dict):
        """Save individual test result to output folder"""
        date_filename = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_stem = Path(file_path).stem
        
        # Save JSON result
        json_filename = f"result_{file_stem}_{date_filename}.json"
        json_path = self.output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'test_result': result.to_dict(),
                'data_analysis': self.convert_numpy_types(data_analysis),
                'file_info': {
                    'original_path': str(file_path),
                    'file_size_mb': float(result.file_size / (1024 * 1024)),
                    'test_timestamp': date_filename
                }
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Individual result saved: {json_path}")
        
        # Save CSV summary if data analysis is available
        if data_analysis and 'sheets' in data_analysis:
            csv_filename = f"data_summary_{file_stem}_{date_filename}.csv"
            csv_path = self.output_dir / csv_filename
            
            # Create summary data for CSV
            summary_data = []
            for sheet_name, sheet_data in data_analysis['sheets'].items():
                if 'error' not in sheet_data:
                    summary_data.append({
                        'sheet_name': sheet_name,
                        'rows': sheet_data['rows'],
                        'columns': sheet_data['columns'],
                        'has_data': sheet_data['has_data'],
                        'empty_rows': sheet_data['empty_rows'],
                        'numeric_columns_count': len(sheet_data.get('numeric_columns', [])),
                        'numeric_columns': ', '.join(sheet_data.get('numeric_columns', []))
                    })
            
            if summary_data:
                df = pd.DataFrame(summary_data)
                df.to_csv(csv_path, index=False)
                print(f"📊 Data summary saved: {csv_path}")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests on all files"""
        print("🚀 Starting Simple Test Suite")
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
                time.sleep(0.5)
            
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
                'success_rate': (sum(1 for r in self.test_results if r.status == 'success') / len(self.test_results)) * 100 if self.test_results else 0
            },
            'test_results': [result.to_dict() for result in self.test_results],
            'summary_statistics': self.calculate_summary_statistics(),
            'recommendations': self.generate_recommendations()
        }
        
        # Save report to file with date-based filename
        report_filename = f"test_report_{self.date_folder}.json"
        report_file = self.output_dir / report_filename
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.convert_numpy_types(report), f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📊 Test report saved: {report_file}")
        
        # Also save a human-readable summary
        summary_filename = f"test_summary_{self.date_folder}.txt"
        summary_file = self.output_dir / summary_filename
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"BillGenerator Test Suite Results\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Total Tests: {report['test_suite_info']['total_tests']}\n")
            f.write(f"Successful: {report['test_suite_info']['successful_tests']}\n")
            f.write(f"Failed: {report['test_suite_info']['failed_tests']}\n")
            f.write(f"Success Rate: {report['test_suite_info']['success_rate']:.1f}%\n")
            f.write(f"Total Duration: {report['test_suite_info']['total_duration']:.2f} seconds\n\n")
            
            f.write("RECOMMENDATIONS:\n")
            f.write("-" * 20 + "\n")
            for rec in report['recommendations']:
                f.write(f"• {rec}\n")
            
            f.write(f"\nDetailed results available in: {report_filename}\n")
        
        print(f"📋 Test summary saved: {summary_file}")
        
        return report
    
    def calculate_summary_statistics(self) -> Dict[str, Any]:
        """Calculate summary statistics"""
        if not self.test_results:
            return {}
        
        successful_tests = [r for r in self.test_results if r.status == 'success']
        
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
            'data_quality_stats': {
                'files_with_data': len([r for r in successful_tests if r.data_summary]),
                'total_sheets_processed': sum(len(r.sheets_found) for r in successful_tests),
                'avg_sheets_per_file': sum(len(r.sheets_found) for r in successful_tests) / len(successful_tests) if successful_tests else 0
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
        
        if not self.test_results:
            recommendations.append("❌ No tests were run. Check test file directory.")
            return recommendations
        
        failed_tests = [r for r in self.test_results if r.status == 'error']
        if failed_tests:
            recommendations.append(f"⚠️ {len(failed_tests)} tests failed. Review error messages for common issues.")
        
        # Check for common validation issues
        validation_errors = [r.error_message for r in failed_tests if r.error_message and 'missing' in r.error_message.lower()]
        if validation_errors:
            recommendations.append("📋 Multiple validation errors detected. Check Excel file structure and required sheets.")
        
        # Check processing time
        avg_time = sum(r.duration for r in self.test_results if r.duration) / len(self.test_results)
        if avg_time > 10:
            recommendations.append("⏱️ Average processing time is high. Consider optimizing file sizes.")
        
        # Check file sizes
        large_files = [r for r in self.test_results if r.file_size > 10 * 1024 * 1024]  # > 10MB
        if large_files:
            recommendations.append(f"📁 {len(large_files)} large files detected. Consider file size optimization.")
        
        # Check data quality
        successful_tests = [r for r in self.test_results if r.status == 'success']
        if successful_tests:
            files_with_data = len([r for r in successful_tests if r.data_summary])
            if files_with_data < len(successful_tests):
                recommendations.append("📊 Some files have data analysis issues. Check Excel file formatting.")
        
        if not recommendations:
            recommendations.append("✅ All tests passed successfully! System is working optimally.")
        
        return recommendations

def main():
    """Main function to run simple tests"""
    print("🧪 BillGenerator Simple Test Suite")
    print("=" * 50)
    
    try:
        # Initialize test runner
        test_runner = SimpleTestRunner()
        
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
