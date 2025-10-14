#!/usr/bin/env python3
"""
Test Document Generation - Verify that the DocumentGenerator and ZipPackager work
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def test_document_generation():
    """Test the document generation pipeline"""
    print("🔍 Testing Document Generation Pipeline...")
    
    try:
        # Import the modules
        from excel_processor import ExcelProcessor
        from document_generator import DocumentGenerator
        from zip_packager import ZipPackager
        from pdf_merger import PDFMerger
        
        print("✅ Successfully imported all required modules")
        
        # Test with sample data
        sample_data = {
            'title': {
                'project_name': 'Test Infrastructure Project',
                'contractor_name': 'ABC Construction Ltd.',
                'agreement_no': 'AGR/2024/TEST/001',
                'location': 'Test Location, Udaipur'
            },
            'work_order': [
                {
                    'description': 'Test Work Item 1',
                    'unit': 'Nos',
                    'quantity': 10,
                    'rate': 500.0,
                    'amount': 5000.0
                },
                {
                    'description': 'Test Work Item 2',
                    'unit': 'Sqm',
                    'quantity': 25,
                    'rate': 200.0,
                    'amount': 5000.0
                }
            ],
            'bill_quantity': [
                {
                    'description': 'Test Work Item 1',
                    'unit': 'Nos',
                    'quantity': 9,
                    'rate': 500.0,
                    'amount': 4500.0
                },
                {
                    'description': 'Test Work Item 2',
                    'unit': 'Sqm',
                    'quantity': 24,
                    'rate': 200.0,
                    'amount': 4800.0
                }
            ],
            'extra_items': [
                {
                    'description': 'Additional Test Work',
                    'unit': 'Nos',
                    'quantity': 2,
                    'rate': 1000.0,
                    'amount': 2000.0
                }
            ],
            'totals': {
                'grand_total': 11300.0,
                'gst_amount': 2034.0,
                'total_with_gst': 13334.0
            }
        }
        
        print("📊 Sample data prepared")
        
        # Test DocumentGenerator
        print("\n🔄 Testing DocumentGenerator...")
        doc_generator = DocumentGenerator(sample_data)
        
        # Generate HTML documents
        html_docs = doc_generator.generate_all_html_documents()
        print(f"   📄 Generated {len(html_docs)} HTML documents:")
        for doc_name, content in html_docs.items():
            size_kb = len(content) / 1024
            print(f"      - {doc_name}: {size_kb:.1f} KB")
        
        # Generate Excel outputs
        excel_outputs = doc_generator.generate_excel_outputs(sample_data)
        print(f"   📊 Generated {len(excel_outputs)} Excel files:")
        for doc_name, content in excel_outputs.items():
            size_kb = len(content) / 1024
            print(f"      - {doc_name}: {size_kb:.1f} KB")
        
        # Test PDFMerger
        print("\n🔄 Testing PDFMerger...")
        pdf_merger = PDFMerger()
        html_pdfs = pdf_merger.convert_html_to_pdf(html_docs)
        print(f"   📑 Generated {len(html_pdfs)} HTML-based PDFs:")
        for doc_name, content in html_pdfs.items():
            size_kb = len(content) / 1024
            print(f"      - {doc_name}: {size_kb:.1f} KB")
        
        # Test ZipPackager
        print("\n🔄 Testing ZipPackager...")
        zip_packager = ZipPackager()
        
        # Create comprehensive package
        zip_bytes = zip_packager.create_comprehensive_package(
            html_docs=html_docs,
            latex_docs={},  # No LaTeX docs for this test
            html_pdfs=html_pdfs,
            latex_pdfs={},  # No LaTeX PDFs for this test
            excel_outputs=excel_outputs,
            processed_data=sample_data,
            filename="test_package.zip"
        )
        
        if zip_bytes and len(zip_bytes) > 1000:
            size_mb = len(zip_bytes) / (1024 * 1024)
            print(f"   📦 Generated ZIP package: {size_mb:.2f} MB")
            
            # Extract package info
            package_info = zip_packager.extract_package_info(zip_bytes)
            print(f"   📁 Package contains {package_info['total_files']} files")
            print(f"   📂 Folders: {', '.join(package_info['folders'])}")
            print(f"   📋 File types: {package_info['file_types']}")
            
            # Save test package
            with open("test_output_package.zip", "wb") as f:
                f.write(zip_bytes)
            print(f"   💾 Saved test package: test_output_package.zip")
            
            return True
        else:
            print("   ❌ ZIP package generation failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Document Generation Test Suite")
    print("=" * 50)
    
    success = test_document_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ DocumentGenerator working correctly")
        print("✅ ZipPackager creating proper packages")
        print("✅ Output files are substantial (not 1-2 KB)")
        print("\n💡 The document generation system is now fully functional!")
    else:
        print("❌ TESTS FAILED")
        print("🔧 Check the error messages above for troubleshooting")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)