#!/usr/bin/env python3
"""
Comprehensive App Tester for BillGenerator Application
Tests both Excel File Upload Mode and Online Mode with proper output organization
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime
from pathlib import Path
import random
import shutil
from typing import Dict, List, Any, Optional

# Try to import pandas
try:
    import pandas as pd
except ImportError:
    print("pandas is required for this script. Please install it with: pip install pandas")
    sys.exit(1)

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

# Try to import required modules
try:
    from src.excel_processor import ExcelProcessor
    from src.latex_generator import LaTeXGenerator
    from src.utils import get_timestamp, sanitize_filename
except ImportError:
    try:
        from excel_processor import ExcelProcessor
        from latex_generator import LaTeXGenerator
        from utils import get_timestamp, sanitize_filename
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required modules are in the src directory")
        sys.exit(1)

class TestResult:
    """Class to store individual test results"""
    def __init__(self, test_name: str, test_type: str):
        self.test_name = test_name
        self.test_type = test_type  # 'upload' or 'online'
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.status = "pending"  # pending, running, success, error
        self.error_message: Optional[str] = None
        self.warnings: List[str] = []
        self.processed_data: Dict[str, Any] = {}
        self.generated_docs: Dict[str, Any] = {}
        self.output_files: List[str] = []
        self.validation_summary: Dict[str, Any] = {}
        
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'test_name': self.test_name,
            'test_type': self.test_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'status': self.status,
            'error_message': self.error_message,
            'warnings': self.warnings,
            'validation_summary': self.validation_summary,
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

class ComprehensiveAppTester:
    """Main comprehensive test runner class"""
    
    def __init__(self, input_dir: str = "INPUT_FILES", output_dir: str = "OUTPUT_FILES"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.test_results: List[TestResult] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.test_input_dir = Path("test_input_files")
        
        # Create required directories
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.test_input_dir.mkdir(exist_ok=True)
        
        # Initialize processors
        self.excel_processor = None
        self.latex_generator = None
        
    def get_date_time_folder_name(self) -> str:
        """Generate folder name with date and time"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d_%H-%M-%S")
    
    def get_output_subfolder(self) -> Path:
        """Create and return output subfolder with date-time naming"""
        folder_name = self.get_date_time_folder_name()
        subfolder = self.output_dir / folder_name
        subfolder.mkdir(exist_ok=True)
        return subfolder
    
    def get_input_files(self) -> List[Path]:
        """Get all Excel input files from INPUT_FILES and test_input_files directories"""
        input_files = []
        
        # Get files from INPUT_FILES directory
        if self.input_dir.exists():
            input_files.extend(list(self.input_dir.glob("*.xlsx")))
            input_files.extend(list(self.input_dir.glob("*.xls")))
        
        # Get files from test_input_files directory
        if self.test_input_dir.exists():
            input_files.extend(list(self.test_input_dir.glob("*.xlsx")))
            input_files.extend(list(self.test_input_dir.glob("*.xls")))
        
        return sorted(input_files)
    
    def create_sample_excel_files(self, count: int = 25) -> List[Path]:
        """Create sample Excel files for testing"""
        created_files = []
        
        for i in range(count):
            # Create a sample Excel file with required sheets
            filename = f"sample_test_file_{i+1:02d}.xlsx"
            file_path = self.test_input_dir / filename
            
            # Create sample data for each sheet
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Title sheet
                title_data = {
                    'Field': ['Project Name', 'Contractor Name', 'Work Order No', 'Location', 'Estimated Cost'],
                    'Value': [
                        f'Sample Project {i+1}',
                        f'Contractor {random.choice(["A", "B", "C"])} Ltd',
                        f'WO-{random.randint(1000, 9999)}',
                        f'Location {random.choice(["North", "South", "East", "West"])} Zone',
                        f'{random.randint(500000, 5000000)}'
                    ]
                }
                pd.DataFrame(title_data).to_excel(writer, sheet_name='Title', index=False)
                
                # Work Order sheet
                work_order_data = {
                    'S.No': [1, 2, 3],
                    'Description': [
                        f'Earthwork Excavation for Sample Project {i+1}',
                        f'Concrete Work for Sample Project {i+1}',
                        f'Brickwork for Sample Project {i+1}'
                    ],
                    'Unit': ['Cum', 'Cum', 'Sqm'],
                    'Quantity': [random.randint(100, 1000), random.randint(50, 500), random.randint(200, 800)],
                    'Rate': [random.randint(500, 1500), random.randint(2000, 5000), random.randint(800, 2000)],
                    'Amount': [0, 0, 0]  # Will be calculated
                }
                work_order_df = pd.DataFrame(work_order_data)
                work_order_df['Amount'] = work_order_df['Quantity'] * work_order_df['Rate']
                work_order_df.to_excel(writer, sheet_name='Work Order', index=False)
                
                # Bill Quantity sheet
                bill_qty_data = {
                    'S.No': [1, 2, 3],
                    'Description': [
                        f'Earthwork Excavation Executed for Sample Project {i+1}',
                        f'Concrete Work Executed for Sample Project {i+1}',
                        f'Brickwork Executed for Sample Project {i+1}'
                    ],
                    'Unit': ['Cum', 'Cum', 'Sqm'],
                    'Quantity': [random.randint(80, 900), random.randint(40, 450), random.randint(150, 750)],
                    'Rate': [random.randint(500, 1500), random.randint(2000, 5000), random.randint(800, 2000)],
                    'Amount': [0, 0, 0]  # Will be calculated
                }
                bill_qty_df = pd.DataFrame(bill_qty_data)
                bill_qty_df['Amount'] = bill_qty_df['Quantity'] * bill_qty_df['Rate']
                bill_qty_df.to_excel(writer, sheet_name='Bill Quantity', index=False)
                
                # Extra Items sheet (optional)
                if random.choice([True, False]):  # 50% chance of having extra items
                    extra_items_data = {
                        'S.No': [1, 2],
                        'Description': [
                            f'Additional Earthwork for Sample Project {i+1}',
                            f'Extra Concrete Work for Sample Project {i+1}'
                        ],
                        'Unit': ['Cum', 'Cum'],
                        'Quantity': [random.randint(10, 100), random.randint(5, 50)],
                        'Rate': [random.randint(600, 1600), random.randint(2100, 5100)],
                        'Amount': [0, 0]  # Will be calculated
                    }
                    extra_items_df = pd.DataFrame(extra_items_data)
                    extra_items_df['Amount'] = extra_items_df['Quantity'] * extra_items_df['Rate']
                    extra_items_df.to_excel(writer, sheet_name='Extra Items', index=False)
            
            created_files.append(file_path)
            print(f"📄 Created sample file: {filename}")
        
        return created_files
    
    def run_excel_upload_mode_test(self) -> TestResult:
        """Test Excel File Upload Mode"""
        result = TestResult("Excel File Upload Mode", "upload")
        result.start_time = datetime.now()
        
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: Excel File Upload Mode")
        print(f"⏰ Start Time: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        try:
            result.status = "running"
            
            # Step 1: Get all input files
            print("📋 Step 1: Identifying input files...")
            input_files = self.get_input_files()
            
            if not input_files:
                # Create sample files if none exist
                print("⚠️ No input files found. Creating sample files...")
                input_files = self.create_sample_excel_files(25)
                input_files.extend(list(self.test_input_dir.glob("*.xlsx")))
            
            print(f"📁 Found {len(input_files)} input files")
            
            # Create output subfolder
            output_subfolder = self.get_output_subfolder()
            print(f"📂 Output will be saved to: {output_subfolder}")
            
            # Process each file
            processed_files = 0
            successful_files = 0
            
            for i, file_path in enumerate(input_files, 1):
                print(f"\n🔄 Processing file {i}/{len(input_files)}: {file_path.name}")
                
                try:
                    # Process the Excel file
                    with open(file_path, 'rb') as f:
                        processor = ExcelProcessor(f)
                        processed_data = processor.process_all_sheets()
                    
                    if processed_data:
                        successful_files += 1
                        print(f"✅ Processed successfully")
                        
                        # Save processed data
                        file_output_dir = output_subfolder / f"file_{i:02d}_{file_path.stem}"
                        file_output_dir.mkdir(exist_ok=True)
                        
                        # Save JSON data
                        data_file = file_output_dir / "processed_data.json"
                        with open(data_file, 'w', encoding='utf-8') as f:
                            json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
                        
                        # Save validation summary
                        validation_summary = processor.get_processing_summary()
                        summary_file = file_output_dir / "validation_summary.json"
                        with open(summary_file, 'w', encoding='utf-8') as f:
                            json.dump(validation_summary, f, indent=2, default=str, ensure_ascii=False)
                        
                        # Add to result
                        result.output_files.append(str(data_file))
                        result.output_files.append(str(summary_file))
                    else:
                        print(f"❌ Failed to process {file_path.name}")
                
                except Exception as e:
                    print(f"❌ Error processing {file_path.name}: {str(e)}")
                    result.warnings.append(f"Error processing {file_path.name}: {str(e)}")
                
                processed_files += 1
                
                # Brief pause to avoid overwhelming the system
                time.sleep(0.1)
            
            # Summary
            result.processed_data = {
                'total_files': len(input_files),
                'processed_files': processed_files,
                'successful_files': successful_files,
                'failed_files': processed_files - successful_files
            }
            
            result.validation_summary = {
                'total_files_processed': processed_files,
                'success_rate': (successful_files / processed_files * 100) if processed_files > 0 else 0,
                'files_with_warnings': len(result.warnings)
            }
            
            result.status = "success" if successful_files > 0 else "error"
            print(f"\n✅ Excel Upload Mode Test Completed!")
            print(f"📊 Files Processed: {processed_files}, Successful: {successful_files}")
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            result.warnings.append(f"Exception: {traceback.format_exc()}")
            print(f"❌ Excel Upload Mode Test Failed: {str(e)}")
        
        finally:
            result.end_time = datetime.now()
            if result.start_time:
                result.duration = (result.end_time - result.start_time).total_seconds()
            print(f"⏱️ Duration: {result.duration:.2f} seconds")
        
        return result
    
    def run_online_mode_test(self) -> TestResult:
        """Test Online Mode with manual data entry"""
        result = TestResult("Online Mode", "online")
        result.start_time = datetime.now()
        
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: Online Mode")
        print(f"⏰ Start Time: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        try:
            result.status = "running"
            
            # Create output subfolder
            output_subfolder = self.get_output_subfolder()
            print(f"📂 Output will be saved to: {output_subfolder}")
            
            # Step 1: Simulate manual data entry (60-75% of items)
            print("📋 Step 1: Simulating manual data entry (60-75% of items)...")
            
            # Get sample input files to base our online entry on
            input_files = self.get_input_files()
            if not input_files:
                # Create sample files if none exist
                print("⚠️ No input files found. Creating sample files...")
                input_files = self.create_sample_excel_files(5)  # Create fewer for online mode
            
            if input_files:
                # Use the first file as basis for online entry
                sample_file = input_files[0]
                print(f"📄 Using {sample_file.name} as sample for online entry")
                
                # Process the sample file to get structure
                with open(sample_file, 'rb') as f:
                    processor = ExcelProcessor(f)
                    sample_data = processor.process_all_sheets()
                
                if sample_data and 'work_order' in sample_data:
                    # Simulate manual online entry
                    work_order_items = sample_data['work_order']
                    selected_items = []
                    
                    # Select 60-75% of items randomly
                    selection_percentage = random.randint(60, 75) / 100
                    items_to_select = max(1, int(len(work_order_items) * selection_percentage))
                    
                    # Randomly select items
                    selected_indices = random.sample(
                        range(len(work_order_items)), 
                        min(items_to_select, len(work_order_items))
                    )
                    
                    for idx in selected_indices:
                        item = work_order_items[idx].copy()
                        # Modify quantities to be within 10-125% of original
                        original_qty = item.get('quantity', 0)
                        if original_qty > 0:
                            new_qty = original_qty * random.randint(10, 125) / 100
                            item['quantity'] = round(new_qty, 2)
                            item['amount'] = round(item['quantity'] * item.get('rate', 0), 2)
                        selected_items.append(item)
                    
                    print(f"✅ Selected {len(selected_items)} items for online entry ({selection_percentage*100:.0f}%)")
                    
                    # Step 2: Add 1-10 extra items
                    print("➕ Step 2: Adding 1-10 extra items...")
                    extra_items_count = random.randint(1, 10)
                    extra_items = []
                    
                    for i in range(extra_items_count):
                        extra_item = {
                            'serial_no': f"EX{i+1:02d}",
                            'description': f"Additional Work Item {i+1} - Online Entry",
                            'unit': random.choice(['Cum', 'Sqm', 'Meter', 'Nos']),
                            'quantity': round(random.uniform(5, 100), 2),
                            'rate': round(random.uniform(500, 5000), 2),
                            'amount': 0,
                            'remark': 'Added via Online Mode'
                        }
                        extra_item['amount'] = round(extra_item['quantity'] * extra_item['rate'], 2)
                        extra_items.append(extra_item)
                    
                    print(f"✅ Added {len(extra_items)} extra items")
                    
                    # Step 3: Create processed data structure
                    processed_data = {
                        'title': sample_data.get('title', {
                            'project_name': 'Online Test Project',
                            'contractor_name': 'Online Test Contractor',
                            'work_order_no': 'ONLINE-WO-001',
                            'location': 'Online Test Location'
                        }),
                        'work_order': selected_items,
                        'bill_quantity': selected_items,  # In online mode, bill quantity is based on work order
                        'extra_items': extra_items,
                        'totals': {
                            'bill_quantity_total': sum(item.get('amount', 0) for item in selected_items),
                            'extra_items_total': sum(item.get('amount', 0) for item in extra_items),
                            'grand_total': 0,
                            'gst_rate': 18.0,
                            'gst_amount': 0,
                            'total_with_gst': 0,
                            'net_payable': 0
                        }
                    }
                    
                    # Calculate totals
                    processed_data['totals']['grand_total'] = (
                        processed_data['totals']['bill_quantity_total'] + 
                        processed_data['totals']['extra_items_total']
                    )
                    processed_data['totals']['gst_amount'] = (
                        processed_data['totals']['grand_total'] * 0.18
                    )
                    processed_data['totals']['total_with_gst'] = (
                        processed_data['totals']['grand_total'] + 
                        processed_data['totals']['gst_amount']
                    )
                    processed_data['totals']['net_payable'] = processed_data['totals']['total_with_gst']
                    
                    # Save processed data
                    online_output_dir = output_subfolder / "online_mode_test"
                    online_output_dir.mkdir(exist_ok=True)
                    
                    # Save JSON data
                    data_file = online_output_dir / "online_processed_data.json"
                    with open(data_file, 'w', encoding='utf-8') as f:
                        json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
                    
                    # Save validation summary
                    validation_summary = {
                        'mode': 'online',
                        'items_selected': len(selected_items),
                        'extra_items_added': len(extra_items),
                        'total_amount': processed_data['totals']['grand_total'],
                        'processing_timestamp': datetime.now().isoformat()
                    }
                    summary_file = online_output_dir / "online_validation_summary.json"
                    with open(summary_file, 'w', encoding='utf-8') as f:
                        json.dump(validation_summary, f, indent=2, default=str, ensure_ascii=False)
                    
                    # Add to result
                    result.processed_data = processed_data
                    result.output_files.append(str(data_file))
                    result.output_files.append(str(summary_file))
                    
                    result.validation_summary = validation_summary
                    result.status = "success"
                    
                    print(f"✅ Online Mode Test Completed!")
                    print(f"📊 Items Selected: {len(selected_items)}, Extra Items: {len(extra_items)}")
                else:
                    result.status = "error"
                    result.error_message = "Could not process sample file for online mode"
                    print("❌ Could not process sample file for online mode")
            else:
                result.status = "error"
                result.error_message = "No input files available for online mode testing"
                print("❌ No input files available for online mode testing")
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            result.warnings.append(f"Exception: {traceback.format_exc()}")
            print(f"❌ Online Mode Test Failed: {str(e)}")
        
        finally:
            result.end_time = datetime.now()
            if result.start_time:
                result.duration = (result.end_time - result.start_time).total_seconds()
            print(f"⏱️ Duration: {result.duration:.2f} seconds")
        
        return result
    
    def generate_comparison_report(self, upload_result: TestResult, online_result: TestResult) -> Dict[str, Any]:
        """Generate comparison report between upload and online modes"""
        comparison = {
            'report_generated': datetime.now().isoformat(),
            'upload_mode_summary': upload_result.to_dict(),
            'online_mode_summary': online_result.to_dict(),
            'comparison_metrics': {}
        }
        
        # Compare processing times
        comparison['comparison_metrics']['processing_time'] = {
            'upload_mode_seconds': upload_result.duration,
            'online_mode_seconds': online_result.duration,
            'faster_mode': 'upload' if (upload_result.duration is not None and 
                                      online_result.duration is not None and
                                      upload_result.duration < online_result.duration) else 'online'
        }
        
        # Compare success rates
        comparison['comparison_metrics']['success_status'] = {
            'upload_mode_success': upload_result.status == 'success',
            'online_mode_success': online_result.status == 'success'
        }
        
        # Compare output files
        comparison['comparison_metrics']['output_files'] = {
            'upload_mode_files': len(upload_result.output_files),
            'online_mode_files': len(online_result.output_files)
        }
        
        return comparison
    
    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive tests for both modes"""
        print("🚀 Starting Comprehensive App Testing")
        print(f"📁 Input Directory: {self.input_dir}")
        print(f"📁 Output Directory: {self.output_dir}")
        print(f"📁 Test Input Directory: {self.test_input_dir}")
        
        self.start_time = datetime.now()
        
        try:
            # Run Excel File Upload Mode Test
            print("\n" + "="*100)
            upload_result = self.run_excel_upload_mode_test()
            self.test_results.append(upload_result)
            
            # Brief pause between tests
            time.sleep(2)
            
            # Run Online Mode Test
            print("\n" + "="*100)
            online_result = self.run_online_mode_test()
            self.test_results.append(online_result)
            
            self.end_time = datetime.now()
            total_duration = (self.end_time - self.start_time).total_seconds() if self.start_time else 0
            
            print(f"\n{'='*100}")
            print(f"🏁 COMPREHENSIVE TESTING COMPLETED!")
            print(f"⏱️ Total Duration: {total_duration:.2f} seconds")
            print(f"📊 Tests Run: {len(self.test_results)}")
            print(f"✅ Successful: {sum(1 for r in self.test_results if r.status == 'success')}")
            print(f"❌ Failed: {sum(1 for r in self.test_results if r.status == 'error')}")
            print(f"{'='*100}")
            
            # Generate comparison report
            comparison_report = self.generate_comparison_report(upload_result, online_result)
            
            # Generate final test report
            return self.generate_final_report(comparison_report)
            
        except Exception as e:
            print(f"❌ Comprehensive test suite failed: {str(e)}")
            return {'error': str(e), 'traceback': traceback.format_exc()}
    
    def generate_final_report(self, comparison_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final comprehensive test report"""
        report = {
            'test_suite_info': {
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': self.end_time.isoformat() if self.end_time else None,
                'total_duration': (self.end_time - self.start_time).total_seconds() if (self.start_time and self.end_time) else 0,
                'total_tests': len(self.test_results),
                'successful_tests': sum(1 for r in self.test_results if r.status == 'success'),
                'failed_tests': sum(1 for r in self.test_results if r.status == 'error'),
                'success_rate': (sum(1 for r in self.test_results if r.status == 'success') / len(self.test_results)) * 100 if self.test_results else 0
            },
            'test_results': [result.to_dict() for result in self.test_results],
            'comparison_report': comparison_report,
            'recommendations': self.generate_recommendations()
        }
        
        # Save report to file in output directory
        timestamp = self.get_date_time_folder_name()
        report_file = self.output_dir / f"comprehensive_test_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Final test report saved: {report_file}")
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if r.status == 'error']
        if failed_tests:
            recommendations.append(f"⚠️ {len(failed_tests)} tests failed. Review error messages for common issues.")
        
        # Check processing time
        valid_durations = [r.duration for r in self.test_results if r.duration is not None]
        avg_time = sum(valid_durations) / len(valid_durations) if valid_durations else 0
        if avg_time > 60:
            recommendations.append("⏱️ Average processing time is high. Consider optimizing processing logic.")
        
        if not recommendations:
            recommendations.append("✅ All tests passed successfully! System is working optimally.")
        
        return recommendations

def main():
    """Main function to run comprehensive tests"""
    print("🧪 BillGenerator Comprehensive App Tester")
    print("=" * 60)
    
    try:
        # Initialize comprehensive test runner
        tester = ComprehensiveAppTester()
        
        # Run comprehensive tests
        report = tester.run_comprehensive_tests()
        
        # Display summary
        if 'test_suite_info' in report:
            print("\n📊 COMPREHENSIVE TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {report['test_suite_info']['total_tests']}")
            print(f"Successful: {report['test_suite_info']['successful_tests']}")
            print(f"Failed: {report['test_suite_info']['failed_tests']}")
            print(f"Success Rate: {report['test_suite_info']['success_rate']:.1f}%")
            print(f"Total Duration: {report['test_suite_info']['total_duration']:.2f} seconds")
        
        if 'recommendations' in report:
            print("\n📋 RECOMMENDATIONS")
            print("=" * 60)
            for rec in report['recommendations']:
                print(f"• {rec}")
        
        print(f"\n📁 Detailed reports saved in: OUTPUT_FILES/")
        
        return report
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        print(f"📝 Traceback: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    main()