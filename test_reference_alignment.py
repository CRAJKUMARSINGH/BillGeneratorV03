#!/usr/bin/env python3
"""
Test script to verify reference alignment modifications
"""

import sys
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def test_sheet_name_mapping():
    """Test that sheet name mapping includes all required sheets"""
    try:
        from src.excel_processor import ExcelProcessor
        
        processor = ExcelProcessor()
        required_sheets = processor.get_required_sheets()
        
        # Check that all required sheets are present
        expected_sheets = ['first_page', 'work_order', 'bill_quantity', 'extra_items', 'deviation_statement', 'note_sheet']
        for sheet in expected_sheets:
            assert sheet in required_sheets, f"Missing sheet mapping for {sheet}"
        
        print("✅ Sheet name mapping test passed")
        return True
        
    except Exception as e:
        print(f"❌ Sheet name mapping test failed: {str(e)}")
        return False

def test_note_sheet_generation():
    """Test that note sheet content generation works"""
    try:
        from src.excel_processor import ExcelProcessor
        
        # Create a mock processed data structure
        processed_data = {
            'title': {
                'project_name': 'Test Project',
                'contractor_name': 'Test Contractor',
                'agreement_no': 'TEST-001',
                'work_order_no': 'WO-001'
            },
            'totals': {
                'work_order_total': 100000,
                'bill_quantity_total': 95000,
                'grand_total': 95000,
                'extra_items_total': 5000
            },
            'extra_items': [
                {'description': 'Extra Item 1', 'amount': 3000},
                {'description': 'Extra Item 2', 'amount': 2000}
            ]
        }
        
        processor = ExcelProcessor()
        note_content = processor.generate_note_sheet_content(processed_data)
        
        # Check that note content was generated
        assert isinstance(note_content, str), "Note content should be a string"
        assert len(note_content) > 0, "Note content should not be empty"
        assert "Premlata Jain" in note_content, "Note content should include signature"
        
        print("✅ Note sheet generation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Note sheet generation test failed: {str(e)}")
        return False

def test_latex_note_sheet_template():
    """Test that LaTeX note sheet template is available"""
    try:
        from src.latex_generator import LaTeXGenerator
        
        generator = LaTeXGenerator()
        
        # Check that note_sheet template is in builtin_templates
        assert 'note_sheet' in generator.builtin_templates, "Note sheet template should be available"
        
        # Check that the template content is not empty
        template_content = generator.builtin_templates['note_sheet']
        assert len(template_content) > 100, "Note sheet template should not be empty"
        
        print("✅ LaTeX note sheet template test passed")
        return True
        
    except Exception as e:
        print(f"❌ LaTeX note sheet template test failed: {str(e)}")
        return False

def test_document_generator_includes_note_sheet():
    """Test that DocumentGenerator includes note sheet generation"""
    try:
        from src.document_generator import DocumentGenerator
        
        # Create mock processed data
        processed_data = {
            'title': {
                'project_name': 'Test Project',
                'contractor_name': 'Test Contractor'
            },
            'totals': {
                'grand_total': 100000,
                'gst_amount': 18000,
                'total_with_gst': 118000
            }
        }
        
        generator = DocumentGenerator(processed_data)
        
        # Test that generate_all_html_documents includes note_sheet
        html_docs = generator.generate_all_html_documents()
        assert 'note_sheet' in html_docs, "HTML documents should include note_sheet"
        
        print("✅ Document generator note sheet test passed")
        return True
        
    except Exception as e:
        print(f"❌ Document generator note sheet test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Reference Alignment Modifications")
    print("=" * 50)
    
    tests = [
        test_sheet_name_mapping,
        test_note_sheet_generation,
        test_latex_note_sheet_template,
        test_document_generator_includes_note_sheet
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All tests passed! Reference alignment modifications are working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())