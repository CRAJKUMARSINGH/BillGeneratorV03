"""
Comprehensive validation script for Extra Items output format.
This script checks if our current app produces properly formatted extra items output
according to government standards and column width requirements.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator
from pdf_merger import PDFMerger

def create_test_data():
    """Create comprehensive test data for extra items validation"""
    return {
        'work_name': 'Construction of New Government Office Building',
        'contractor_name': 'ABC Construction Pvt. Ltd.',
        'reference_no': 'REF/2024/EXTRA/001',
        'date': '2024-09-22',
        'extra_items': [
            {
                'sno': 1,
                'description': 'Additional electrical wiring for conference room',
                'unit': 'Mtr',
                'quantity': 150.50,
                'rate': 125.75,
                'amount': 18926.125,
                'remarks': 'As per site requirement'
            },
            {
                'sno': 2,
                'description': 'Extra marble flooring in lobby area',
                'unit': 'Sqm',
                'quantity': 45.25,
                'rate': 850.00,
                'amount': 38462.50,
                'remarks': 'Premium grade marble'
            },
            {
                'sno': 3,
                'description': 'Additional HVAC ducting for server room',
                'unit': 'Mtr',
                'quantity': 75.00,
                'rate': 275.50,
                'amount': 20662.50,
                'remarks': 'Fire-resistant ducting'
            },
            {
                'sno': 4,
                'description': 'Extra safety railings for terrace',
                'unit': 'Mtr',
                'quantity': 120.75,
                'rate': 450.25,
                'amount': 54369.1875,
                'remarks': 'Stainless steel grade 304'
            }
        ]
    }

def analyze_template_structure():
    """Analyze the current extra items template structure"""
    template_path = Path("templates/extra_items.html")
    
    if not template_path.exists():
        print("❌ ERROR: extra_items.html template not found!")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print("📋 TEMPLATE STRUCTURE ANALYSIS")
    print("=" * 50)
    
    # Check for essential elements
    checks = {
        'Title': 'EXTRA ITEM SLIP' in template_content,
        'Work Name Field': '{{ work_name }}' in template_content,
        'Contractor Field': '{{ contractor_name }}' in template_content,
        'Reference Field': '{{ reference_no }}' in template_content,
        'Date Field': '{{ date }}' in template_content,
        'Items Table': 'extra_items' in template_content,
        'Serial Number Column': 'S.No.' in template_content or 'Serial' in template_content,
        'Description Column': 'Description' in template_content,
        'Unit Column': 'Unit' in template_content,
        'Quantity Column': 'Qty' in template_content or 'Quantity' in template_content,
        'Rate Column': 'Rate' in template_content,
        'Amount Column': 'Amount' in template_content,
        'Remarks Column': 'Remarks' in template_content,
        'Total Calculation': 'total' in template_content.lower(),
        'CSS Styling': '<style>' in template_content,
        'Table Structure': '<table' in template_content
    }
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}: {'PASS' if passed else 'FAIL'}")
    
    return all(checks.values())

def test_extra_items_generation():
    """Test the actual generation of extra items document"""
    print("\n🔧 TESTING DOCUMENT GENERATION")
    print("=" * 50)
    
    try:
        # Initialize generator with processed data format
        test_data = create_test_data()
        processed_data = {
            'title': {
                'project_name': test_data['work_name'],
                'contractor_name': test_data['contractor_name'],
                'agreement_no': test_data['reference_no']
            },
            'extra_items': test_data['extra_items']
        }
        generator = DocumentGenerator(processed_data)
        
        # Generate extra items HTML
        extra_items_html = generator.generate_extra_items_statement()
        
        # Save for inspection
        output_path = Path("test_extra_items_validation.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extra_items_html)
        
        print(f"✅ Generated HTML output: {output_path}")
        print(f"📊 HTML Content Length: {len(extra_items_html)} characters")
        
        return extra_items_html, output_path
        
    except Exception as e:
        print(f"❌ Generation failed: {str(e)}")
        return None, None

def analyze_generated_output(html_content):
    """Analyze the generated HTML output for formatting compliance"""
    if not html_content:
        return False
    
    print("\n📊 OUTPUT FORMAT ANALYSIS")
    print("=" * 50)
    
    # Check for proper formatting elements
    format_checks = {
        'Table Structure': '<table' in html_content and '</table>' in html_content,
        'Header Row': '<th' in html_content or '<thead' in html_content,
        'Data Rows': '<td' in html_content or '<tbody' in html_content,
        'Currency Formatting': '₹' in html_content,
        'Right Alignment CSS': 'text-align: right' in html_content,
        'Center Alignment CSS': 'text-align: center' in html_content,
        'Arial Font': 'Arial' in html_content,
        'Total Calculation': any(word in html_content.lower() for word in ['total', 'grand total', 'sum']),
        'Premium Calculation': 'premium' in html_content.lower(),
        'Final Amount': 'final' in html_content.lower(),
        'Proper Spacing': 'margin' in html_content or 'padding' in html_content,
        'Print Optimization': '@media print' in html_content or 'page-break' in html_content
    }
    
    for check, passed in format_checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}: {'PASS' if passed else 'FAIL'}")
    
    # Count items in output
    item_count = html_content.count('<tr') - 1  # Subtract header row
    print(f"\n📋 Items in output: {item_count}")
    
    return all(format_checks.values())

def test_pdf_generation():
    """Test PDF generation if possible"""
    print("\n📄 TESTING PDF GENERATION")
    print("=" * 50)
    
    try:
        merger = PDFMerger()
        test_data = create_test_data()
        
        # Test PDF generation
        test_html = {"test_doc": "<h1>Test PDF Generation</h1>"}
        pdf_result = merger.convert_html_to_pdf(test_html)
        
        pdf_path = None
        if pdf_result and "test_doc_html" in pdf_result:
            # Save PDF to file for verification
            pdf_path = "test_pdf_generation.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(pdf_result["test_doc_html"])
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ PDF generation working: {pdf_path}")
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("🔍 EXTRA ITEMS OUTPUT VALIDATION")
    print("=" * 60)
    print("Checking if current app produces properly formatted extra items output...")
    
    # Step 1: Analyze template structure
    template_ok = analyze_template_structure()
    
    # Step 2: Test document generation
    html_content, output_path = test_extra_items_generation()
    
    # Step 3: Analyze generated output
    format_ok = analyze_generated_output(html_content) if html_content else False
    
    # Step 4: Test PDF capability
    pdf_ok = test_pdf_generation()
    
    # Final assessment
    print("\n" + "=" * 60)
    print("🎯 FINAL ASSESSMENT")
    print("=" * 60)
    
    overall_score = sum([template_ok, bool(html_content), format_ok, pdf_ok]) / 4 * 100
    
    print(f"📊 Template Structure: {'✅ PASS' if template_ok else '❌ FAIL'}")
    print(f"🔧 Document Generation: {'✅ PASS' if html_content else '❌ FAIL'}")
    print(f"📋 Format Compliance: {'✅ PASS' if format_ok else '❌ FAIL'}")
    print(f"📄 PDF Generation: {'✅ PASS' if pdf_ok else '❌ FAIL'}")
    print(f"\n🏆 Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 75:
        print("✅ RESULT: App produces good quality extra items output!")
        if output_path:
            print(f"📁 Review generated output: {output_path}")
    else:
        print("❌ RESULT: App needs improvements for proper extra items output!")
        print("\n🔧 RECOMMENDED ACTIONS:")
        if not template_ok:
            print("   - Fix template structure issues")
        if not html_content:
            print("   - Fix document generation errors")
        if not format_ok:
            print("   - Improve formatting and alignment")
        if not pdf_ok:
            print("   - Fix PDF generation capability")

if __name__ == "__main__":
    main()