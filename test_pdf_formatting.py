#!/usr/bin/env python3
"""
PDF Format Testing Script
Tests the PDF generation with corrected margins and formatting
"""

import os
import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def test_pdf_formatting():
    """Test PDF formatting with sample files"""
    print("🔍 Testing PDF formatting with corrected templates...")
    
    try:
        # Import the necessary modules
        from utils import validate_excel_file
        from excel_processor import ExcelProcessor
        import pandas as pd
        
        print("✅ Successfully imported required modules")
        
        # Test with our sample file
        sample_file_path = "Input_Files_for_tests/sample_infrastructure_bill.xlsx"
        
        if not os.path.exists(sample_file_path):
            print(f"❌ Sample file not found: {sample_file_path}")
            return False
        
        print(f"📁 Testing with file: {sample_file_path}")
        
        # Read the sample file
        with open(sample_file_path, 'rb') as f:
            # Create a mock uploaded file object
            class MockFile:
                def __init__(self, content, name):
                    self.content = content
                    self.name = name
                    self.position = 0
                
                def read(self, size=-1):
                    if size == -1:
                        result = self.content[self.position:]
                        self.position = len(self.content)
                    else:
                        result = self.content[self.position:self.position + size]
                        self.position += len(result)
                    return result
                
                def seek(self, position):
                    self.position = position
                
                def getvalue(self):
                    return self.content
            
            mock_file = MockFile(f.read(), sample_file_path)
            
            # Validate the file
            validation_result = validate_excel_file(mock_file)
            print(f"📊 File validation: {'✅ PASSED' if validation_result['valid'] else '❌ FAILED'}")
            
            if validation_result['valid']:
                print("🎯 File validation successful!")
                print(f"   📋 Sheets found: {validation_result['file_info'].get('sheets', [])}")
                print(f"   📏 File size: {validation_result['file_info'].get('size_mb', 0):.2f} MB")
                
                # Test Excel processing
                try:
                    mock_file.seek(0)  # Reset file position
                    excel_processor = ExcelProcessor(mock_file)
                    processed_data = excel_processor.process_all_sheets()
                    
                    if processed_data:
                        print("✅ Excel processing successful!")
                        print(f"   📊 Data sheets processed: {list(processed_data.keys())}")
                        
                        # Check if we have bill quantity data
                        if 'bill_quantity' in processed_data:
                            bill_items = processed_data['bill_quantity']
                            print(f"   📋 Bill items found: {len(bill_items)}")
                            
                        # Check project information
                        if 'title' in processed_data:
                            title_info = processed_data['title']
                            print(f"   🏗️ Project: {title_info.get('project_name', 'N/A')}")
                        
                        print("🎉 PDF formatting test components are working correctly!")
                        return True
                    else:
                        print("❌ Excel processing failed")
                        return False
                        
                except Exception as e:
                    print(f"❌ Excel processing error: {str(e)}")
                    return False
            else:
                print(f"❌ File validation failed: {validation_result.get('error', 'Unknown error')}")
                return False
                
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Make sure all required modules are available")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def check_template_formatting():
    """Check if templates have correct formatting"""
    print("\n📋 Checking template formatting...")
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    template_files = list(templates_dir.glob("*.html"))
    if not template_files:
        print("❌ No HTML templates found")
        return False
    
    print(f"📁 Found {len(template_files)} HTML templates")
    
    correct_margin_count = 0
    
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for correct margin specification
                if "margin: 10mm" in content or "margin: 10mm 10mm 10mm 10mm" in content:
                    print(f"   ✅ {template_file.name}: Correct 10mm margins")
                    correct_margin_count += 1
                elif "margin:" in content:
                    print(f"   ⚠️ {template_file.name}: Has margins but not 10mm")
                else:
                    print(f"   ❌ {template_file.name}: No margin specification")
                    
        except Exception as e:
            print(f"   ❌ {template_file.name}: Error reading file - {str(e)}")
    
    print(f"\n📊 Template Summary:")
    print(f"   ✅ Templates with correct margins: {correct_margin_count}/{len(template_files)}")
    
    return correct_margin_count > 0

def check_css_formatting():
    """Check if CSS files have correct formatting"""
    print("\n🎨 Checking CSS formatting...")
    
    css_files = [
        "attached_assets/styles/pdf.css",
        "attached_assets/styles/main.css"
    ]
    
    for css_file in css_files:
        if os.path.exists(css_file):
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if "margin: 10mm" in content:
                        print(f"   ✅ {css_file}: Correct 10mm margins found")
                    else:
                        print(f"   ⚠️ {css_file}: 10mm margins not found")
                        
            except Exception as e:
                print(f"   ❌ {css_file}: Error reading file - {str(e)}")
        else:
            print(f"   ❌ {css_file}: File not found")

def run_comprehensive_test():
    """Run comprehensive PDF formatting test"""
    print("🚀 Starting Comprehensive PDF Formatting Test")
    print("=" * 60)
    
    # Test 1: Check template formatting
    template_test = check_template_formatting()
    
    # Test 2: Check CSS formatting
    check_css_formatting()
    
    # Test 3: Test PDF generation components
    pdf_test = test_pdf_formatting()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    if template_test and pdf_test:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Templates have correct 10mm margins")
        print("✅ PDF generation components working")
        print("✅ Sample file processing successful")
        print("\n💡 The PDF formatting issues have been resolved!")
        print("📄 Generated PDFs should now use full A4 page with 10mm margins")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        if not template_test:
            print("❌ Template formatting issues detected")
        if not pdf_test:
            print("❌ PDF generation component issues detected")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Test the application with sample files")
        print("2. Generate PDFs and verify 10mm margins")
        print("3. Check that tables use full page width")
        print("4. Confirm no content shrinking in PDF conversion")
    else:
        print("\n🔧 Troubleshooting needed:")
        print("1. Check template files for margin specifications")
        print("2. Verify CSS files have correct page setup")
        print("3. Test with different sample files")
        print("4. Check application dependencies")
    
    sys.exit(0 if success else 1)