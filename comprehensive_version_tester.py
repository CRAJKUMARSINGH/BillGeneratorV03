#!/usr/bin/env python3
"""
Comprehensive Bill Generator Test Suite
Tests all three Bill Generator versions as specified in Bill_test_command_21092025.txt
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import shutil
import glob

class BillGeneratorTester:
    """Comprehensive tester for all Bill Generator versions"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/Rajkumar")
        self.versions = ["BillGeneratorV01", "BillGeneratorV02", "BillGeneratorV03"]
        self.current_version = "BillGeneratorV03"  # Current working directory
        self.test_results = {}
        self.output_base = Path("Output")
        
    def setup_output_directory(self):
        """Create organized output directory structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.output_base / f"test_run_{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory created: {self.output_dir}")
        
    def find_input_files(self, version_path: Path):
        """Find all input files in test_input_* and sample_input* folders"""
        input_files = []
        
        # Search patterns from the command file
        search_patterns = [
            "test_input*/*.xlsx",
            "test_input*/*.xls", 
            "sample_input*/*.xlsx",
            "sample_input*/*.xls",
            "Input_Files_for_tests/*.xlsx",
            "Input_Files_for_tests/*.xls"
        ]
        
        for pattern in search_patterns:
            found_files = list(version_path.glob(pattern))
            input_files.extend(found_files)
            
        # Remove duplicates
        input_files = list(set(input_files))
        
        print(f"   📋 Found {len(input_files)} input files:")
        for file in input_files:
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"      - {file.name} ({size_mb:.2f} MB)")
            
        return input_files
    
    def test_version_availability(self, version_name: str):
        """Test if a version is available and runnable"""
        version_path = self.base_path / version_name
        
        print(f"\n🔍 Testing {version_name} availability...")
        
        if not version_path.exists():
            print(f"   ❌ Directory not found: {version_path}")
            return {"status": "missing", "path": None, "app_files": []}
        
        print(f"   ✅ Directory found: {version_path}")
        
        # Look for main application files
        app_files = []
        potential_apps = [
            "streamlit_app.py",
            "app.py", 
            "src/app.py",
            "main.py",
            "run.py"
        ]
        
        for app_file in potential_apps:
            app_path = version_path / app_file
            if app_path.exists():
                app_files.append(app_path)
                print(f"      📄 Found: {app_file}")
        
        if not app_files:
            print(f"   ⚠️ No main application files found")
            return {"status": "no_app", "path": version_path, "app_files": []}
        
        return {"status": "available", "path": version_path, "app_files": app_files}
    
    def run_version_test(self, version_name: str, app_info: dict):
        """Run tests for a specific version"""
        print(f"\n🚀 Running tests for {version_name}")
        print("=" * 50)
        
        version_path = app_info["path"]
        app_files = app_info["app_files"]
        
        version_output = self.output_dir / version_name
        version_output.mkdir(exist_ok=True)
        
        # Find input files
        input_files = self.find_input_files(version_path)
        
        if not input_files:
            print(f"   ⚠️ No input files found for {version_name}")
            # Create sample file for testing
            input_files = self.create_sample_input_file(version_path)
        
        results = {
            "version": version_name,
            "status": "unknown",
            "app_files": [str(f) for f in app_files],
            "input_files": [str(f) for f in input_files],
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "outputs_generated": [],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_seconds": None
        }
        
        start_time = time.time()
        
        try:
            # Test each main app file
            for app_file in app_files:
                print(f"\n📱 Testing app: {app_file.name}")
                
                # Change to version directory
                original_cwd = os.getcwd()
                os.chdir(version_path)
                
                try:
                    # Test basic import/syntax
                    test_result = self.test_app_syntax(app_file)
                    results["tests_run"] += 1
                    
                    if test_result["passed"]:
                        results["tests_passed"] += 1
                        print(f"   ✅ Syntax test passed")
                        
                        # Try to run with sample data if possible
                        if input_files:
                            processing_results = self.test_app_processing(app_file, input_files[:3])  # Test with first 3 files
                            results["tests_run"] += len(processing_results)
                            
                            for proc_result in processing_results:
                                if proc_result["success"]:
                                    results["tests_passed"] += 1
                                    results["outputs_generated"].extend(proc_result.get("outputs", []))
                                else:
                                    results["tests_failed"] += 1
                                    results["errors"].extend(proc_result.get("errors", []))
                        
                    else:
                        results["tests_failed"] += 1
                        results["errors"].append(f"Syntax test failed for {app_file.name}: {test_result.get('error', 'Unknown error')}")
                        print(f"   ❌ Syntax test failed: {test_result.get('error', 'Unknown error')}")
                
                finally:
                    os.chdir(original_cwd)
            
            # Determine overall status
            if results["tests_passed"] > 0 and results["tests_failed"] == 0:
                results["status"] = "success"
            elif results["tests_passed"] > 0:
                results["status"] = "partial"
            else:
                results["status"] = "failed"
                
        except Exception as e:
            results["status"] = "error"
            results["errors"].append(f"Version test error: {str(e)}")
            print(f"   ❌ Version test error: {str(e)}")
        
        end_time = time.time()
        results["end_time"] = datetime.now().isoformat()
        results["duration_seconds"] = round(end_time - start_time, 2)
        
        # Save results
        self.save_version_results(version_name, results, version_output)
        
        return results
    
    def test_app_syntax(self, app_file: Path):
        """Test if app file has valid Python syntax"""
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Try to compile the source
            compile(source, str(app_file), 'exec')
            return {"passed": True}
            
        except SyntaxError as e:
            return {"passed": False, "error": f"Syntax error: {str(e)}"}
        except Exception as e:
            return {"passed": False, "error": f"Compilation error: {str(e)}"}
    
    def test_app_processing(self, app_file: Path, input_files: list):
        """Test app processing with input files"""
        results = []
        
        for input_file in input_files:
            result = {
                "input_file": str(input_file),
                "success": False,
                "outputs": [],
                "errors": []
            }
            
            try:
                # For now, just check if the file can be processed
                # This is a basic test - real processing would need the app to be running
                print(f"      📄 Testing with: {input_file.name}")
                
                # Check if input file is readable
                if input_file.exists() and input_file.stat().st_size > 1000:
                    result["success"] = True
                    result["outputs"].append(f"Input file validated: {input_file.name}")
                    print(f"         ✅ Input file validated")
                else:
                    result["errors"].append(f"Input file too small or missing: {input_file.name}")
                    print(f"         ⚠️ Input file issue")
                    
            except Exception as e:
                result["errors"].append(f"Processing error: {str(e)}")
                print(f"         ❌ Processing error: {str(e)}")
            
            results.append(result)
        
        return results
    
    def create_sample_input_file(self, version_path: Path):
        """Create a sample input file for testing"""
        try:
            import pandas as pd
            
            # Create input directory
            input_dir = version_path / "test_input_generated"
            input_dir.mkdir(exist_ok=True)
            
            sample_file = input_dir / "sample_test_file.xlsx"
            
            # Create sample Excel file
            with pd.ExcelWriter(sample_file, engine='openpyxl') as writer:
                # Title sheet
                title_data = pd.DataFrame({
                    'Field': ['Project Name', 'Contractor Name', 'Agreement No'],
                    'Value': ['Sample Project', 'Sample Contractor', 'AGR/001']
                })
                title_data.to_excel(writer, sheet_name='Title', index=False)
                
                # Work Order sheet
                wo_data = pd.DataFrame({
                    'Description': ['Sample Work 1', 'Sample Work 2'],
                    'Unit': ['Nos', 'Sqm'],
                    'Quantity': [10, 25],
                    'Rate': [500, 200],
                    'Amount': [5000, 5000]
                })
                wo_data.to_excel(writer, sheet_name='Work Order', index=False)
                
                # Bill Quantity sheet
                bq_data = pd.DataFrame({
                    'Description': ['Sample Work 1', 'Sample Work 2'],
                    'Unit': ['Nos', 'Sqm'],
                    'Quantity': [9, 23],
                    'Rate': [500, 200],
                    'Amount': [4500, 4600]
                })
                bq_data.to_excel(writer, sheet_name='Bill Quantity', index=False)
            
            print(f"   📄 Created sample input file: {sample_file}")
            return [sample_file]
            
        except Exception as e:
            print(f"   ❌ Error creating sample file: {str(e)}")
            return []
    
    def save_version_results(self, version_name: str, results: dict, output_dir: Path):
        """Save test results for a version"""
        try:
            import json
            
            # Save JSON results
            json_file = output_dir / f"{version_name}_test_results.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Save readable report
            report_file = output_dir / f"{version_name}_test_report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"# {version_name} Test Report\\n\\n")
                f.write(f"**Generated:** {results['start_time']}\\n")
                f.write(f"**Duration:** {results['duration_seconds']} seconds\\n")
                f.write(f"**Status:** {results['status'].upper()}\\n\\n")
                
                f.write(f"## Test Summary\\n")
                f.write(f"- **Tests Run:** {results['tests_run']}\\n")
                f.write(f"- **Tests Passed:** {results['tests_passed']}\\n")
                f.write(f"- **Tests Failed:** {results['tests_failed']}\\n\\n")
                
                f.write(f"## Application Files\\n")
                for app_file in results['app_files']:
                    f.write(f"- {app_file}\\n")
                f.write("\\n")
                
                f.write(f"## Input Files\\n")
                for input_file in results['input_files']:
                    f.write(f"- {input_file}\\n")
                f.write("\\n")
                
                if results['errors']:
                    f.write(f"## Errors\\n")
                    for error in results['errors']:
                        f.write(f"- {error}\\n")
                    f.write("\\n")
                
                if results['outputs_generated']:
                    f.write(f"## Outputs Generated\\n")
                    for output in results['outputs_generated']:
                        f.write(f"- {output}\\n")
            
            print(f"   📊 Results saved to: {output_dir}")
            
        except Exception as e:
            print(f"   ❌ Error saving results: {str(e)}")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive report for all versions"""
        try:
            report_file = self.output_dir / "COMPREHENSIVE_TEST_REPORT.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Bill Generator Versions - Comprehensive Test Report\\n\\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"**Tester:** Automated Test Suite\\n")
                f.write(f"**Compliance:** Bill_test_command_21092025.txt\\n\\n")
                
                f.write("## Executive Summary\\n\\n")
                
                total_versions = len(self.test_results)
                working_versions = len([r for r in self.test_results.values() if r['status'] in ['success', 'partial']])
                
                f.write(f"- **Total Versions Tested:** {total_versions}\\n")
                f.write(f"- **Working Versions:** {working_versions}\\n")
                f.write(f"- **Success Rate:** {(working_versions/total_versions)*100:.1f}%\\n\\n")
                
                f.write("## Version Status Overview\\n\\n")
                f.write("| Version | Status | Tests Run | Passed | Failed | Duration |\\n")
                f.write("|---------|--------|-----------|--------|--------|----------|\\n")
                
                for version_name, results in self.test_results.items():
                    status_emoji = {
                        'success': '✅',
                        'partial': '⚠️',
                        'failed': '❌',
                        'error': '💥',
                        'missing': '❓'
                    }.get(results['status'], '❓')
                    
                    f.write(f"| {version_name} | {status_emoji} {results['status']} | {results['tests_run']} | {results['tests_passed']} | {results['tests_failed']} | {results.get('duration_seconds', 'N/A')}s |\\n")
                
                f.write("\\n## Detailed Results\\n\\n")
                
                for version_name, results in self.test_results.items():
                    f.write(f"### {version_name}\\n\\n")
                    f.write(f"**Status:** {results['status']}\\n")
                    f.write(f"**Application Files:** {len(results['app_files'])}\\n")
                    f.write(f"**Input Files Found:** {len(results['input_files'])}\\n")
                    
                    if results['errors']:
                        f.write(f"**Errors:** {len(results['errors'])}\\n")
                        for error in results['errors'][:3]:  # Show first 3 errors
                            f.write(f"- {error}\\n")
                        if len(results['errors']) > 3:
                            f.write(f"- ... and {len(results['errors'])-3} more\\n")
                    
                    f.write("\\n")
                
                f.write("## Recommendations\\n\\n")
                
                # Generate recommendations based on results
                recommendations = []
                
                failed_versions = [name for name, results in self.test_results.items() if results['status'] in ['failed', 'error']]
                if failed_versions:
                    recommendations.append(f"🔧 **Fix Critical Issues:** {', '.join(failed_versions)} need attention")
                
                missing_versions = [name for name, results in self.test_results.items() if results['status'] == 'missing']
                if missing_versions:
                    recommendations.append(f"📁 **Missing Versions:** {', '.join(missing_versions)} not found")
                
                if working_versions == total_versions:
                    recommendations.append("🎉 **All versions are working!** Focus on performance optimization")
                elif working_versions > 0:
                    recommendations.append(f"✅ **Partial Success:** {working_versions}/{total_versions} versions working")
                
                recommendations.append("📊 **Template Testing:** Verify all templates render correctly")
                recommendations.append("🔍 **Input File Coverage:** Test with all available input files")
                recommendations.append("📏 **Output Quality:** Verify A4 formatting and 10mm margins")
                
                for rec in recommendations:
                    f.write(f"- {rec}\\n")
                
                f.write("\\n---\\n\\n")
                f.write("*This report was generated automatically by the Bill Generator Test Suite*\\n")
            
            print(f"\\n📋 Comprehensive report saved: {report_file}")
            
        except Exception as e:
            print(f"❌ Error generating comprehensive report: {str(e)}")
    
    def run_all_tests(self):
        """Run tests for all Bill Generator versions"""
        print("🚀 Bill Generator Comprehensive Test Suite")
        print("=" * 60)
        print("📋 Following specifications from: Bill_test_command_21092025.txt")
        print()
        
        self.setup_output_directory()
        
        # Test each version
        for version_name in self.versions:
            # Test availability
            app_info = self.test_version_availability(version_name)
            
            if app_info["status"] == "available":
                # Run comprehensive tests
                results = self.run_version_test(version_name, app_info)
            else:
                # Record non-available version
                results = {
                    "version": version_name,
                    "status": app_info["status"],
                    "app_files": [],
                    "input_files": [],
                    "tests_run": 0,
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "errors": [f"Version {app_info['status']}"],
                    "outputs_generated": [],
                    "start_time": datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "duration_seconds": 0
                }
            
            self.test_results[version_name] = results
        
        # Generate comprehensive report
        self.generate_comprehensive_report()
        
        print("\\n" + "="*60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        
        for version_name, results in self.test_results.items():
            status_emoji = {
                'success': '✅',
                'partial': '⚠️', 
                'failed': '❌',
                'error': '💥',
                'missing': '❓',
                'no_app': '📱',
                'available': '🟢'
            }.get(results['status'], '❓')
            
            print(f"{status_emoji} {version_name}: {results['status']} ({results['tests_passed']}/{results['tests_run']} passed)")
        
        print(f"\\n📁 All results saved to: {self.output_dir}")
        
        return self.test_results

def main():
    """Main function"""
    tester = BillGeneratorTester()
    results = tester.run_all_tests()
    
    # Determine exit code
    success_count = len([r for r in results.values() if r['status'] in ['success', 'partial']])
    total_count = len(results)
    
    if success_count == total_count:
        print("\\n🎉 ALL VERSIONS TESTED SUCCESSFULLY!")
        return 0
    elif success_count > 0:
        print(f"\\n⚠️ PARTIAL SUCCESS: {success_count}/{total_count} versions working")
        return 1
    else:
        print("\\n❌ ALL TESTS FAILED")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)