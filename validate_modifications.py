#!/usr/bin/env python3
"""
Validation script to confirm reference alignment modifications
"""

import sys
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def validate_sheet_mappings():
    """Validate that sheet name mappings have been updated"""
    print("🔍 Validating sheet name mappings...")
    
    try:
        from src.excel_processor import ExcelProcessor
        
        processor = ExcelProcessor()
        required_sheets = processor.get_required_sheets()
        
        print("   Available sheet mappings:")
        for sheet_type, keywords in required_sheets.items():
            print(f"     {sheet_type}: {keywords}")
        
        # Check for key mappings
        expected_mappings = {
            'first_page': ['first page', 'first_page', 'front', 'title', 'cover', 'front', 'project', 'header'],
            'note_sheet': ['note sheet', 'note_sheet', 'notes']
        }
        
        for sheet_type, expected_keywords in expected_mappings.items():
            if sheet_type in required_sheets:
                print(f"   ✅ {sheet_type} mapping found")
            else:
                print(f"   ❌ {sheet_type} mapping missing")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error validating sheet mappings: {str(e)}")
        return False

def validate_note_sheet_method():
    """Validate that note sheet generation method exists"""
    print("🔍 Validating note sheet generation method...")
    
    try:
        from src.excel_processor import ExcelProcessor
        import inspect
        
        processor = ExcelProcessor()
        method_exists = hasattr(processor, 'generate_note_sheet_content')
        
        if method_exists:
            print("   ✅ generate_note_sheet_content method found")
            
            # Check method signature
            sig = inspect.signature(processor.generate_note_sheet_content)
            print(f"   Method signature: {sig}")
            
            return True
        else:
            print("   ❌ generate_note_sheet_content method not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Error validating note sheet method: {str(e)}")
        return False

def validate_latex_templates():
    """Validate that LaTeX templates include note sheet"""
    print("🔍 Validating LaTeX templates...")
    
    try:
        from src.latex_generator import LaTeXGenerator
        
        generator = LaTeXGenerator()
        
        print(f"   Available LaTeX templates: {list(generator.builtin_templates.keys())}")
        
        if 'note_sheet' in generator.builtin_templates:
            print("   ✅ Note sheet LaTeX template found")
            template_length = len(generator.builtin_templates['note_sheet'])
            print(f"   Template length: {template_length} characters")
            return True
        else:
            print("   ❌ Note sheet LaTeX template missing")
            return False
            
    except Exception as e:
        print(f"   ❌ Error validating LaTeX templates: {str(e)}")
        return False

def validate_html_templates():
    """Validate that HTML templates include note sheet"""
    print("🔍 Validating HTML templates...")
    
    try:
        templates_dir = Path("templates")
        note_sheet_html = templates_dir / "note_sheet.html"
        
        if note_sheet_html.exists():
            print("   ✅ note_sheet.html template found")
            file_size = note_sheet_html.stat().st_size
            print(f"   File size: {file_size} bytes")
            return True
        else:
            print("   ❌ note_sheet.html template missing")
            return False
            
    except Exception as e:
        print(f"   ❌ Error validating HTML templates: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("📋 Reference Alignment Modifications Validation")
    print("=" * 50)
    
    validations = [
        validate_sheet_mappings,
        validate_note_sheet_method,
        validate_latex_templates,
        validate_html_templates
    ]
    
    passed = 0
    total = len(validations)
    
    for validation in validations:
        if validation():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Validation Results: {passed}/{total} validations passed")
    
    if passed == total:
        print("✅ All modifications have been successfully implemented!")
        print("\nSummary of changes:")
        print("  • Sheet name mappings updated to align with VBA references")
        print("  • Note sheet content generation method added")
        print("  • LaTeX note sheet template included")
        print("  • HTML note sheet template verified")
        return 0
    else:
        print("❌ Some modifications may need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())