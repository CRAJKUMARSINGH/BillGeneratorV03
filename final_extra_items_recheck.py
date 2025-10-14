"""
Final recheck of extra items output - Comprehensive validation
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator
from pdf_merger import PDFMerger

def final_extra_items_recheck():
    """Comprehensive recheck of extra items functionality"""
    
    print("🔍 FINAL EXTRA ITEMS RECHECK")
    print("=" * 60)
    
    # Test data
    test_data = {
        'work_name': 'Construction of Additional Academic Block at Government College',
        'contractor_name': 'M/s ABC Construction & Engineering Pvt. Ltd.',
        'reference_no': 'Agreement No. CE/2024/EXTRA/075',
        'extra_items': [
            {
                'description': 'Additional electrical wiring for conference room',
                'unit': 'Mtr',
                'quantity': 185.50,
                'rate': 145.75,
                'amount': 27036.625,
                'remarks': 'As per site requirement'
            },
            {
                'description': 'Extra marble flooring in entrance lobby',
                'unit': 'Sqm',
                'quantity': 67.25,
                'rate': 1250.00,
                'amount': 84062.50,
                'remarks': 'Premium grade marble'
            },
            {
                'description': 'Additional HVAC ducting for server room',
                'unit': 'Mtr',
                'quantity': 125.00,
                'rate': 375.50,
                'amount': 46937.50,
                'remarks': 'Fire rated ducting'
            }
        ]
    }
    
    # Prepare processed data
    processed_data = {
        'title': {
            'project_name': test_data['work_name'],
            'contractor_name': test_data['contractor_name'],
            'agreement_no': test_data['reference_no']
        },
        'extra_items': test_data['extra_items']
    }
    
    try:
        # Generate HTML
        generator = DocumentGenerator(processed_data)
        html_content = generator.generate_extra_items_statement()
        
        # Save for inspection
        output_file = "final_recheck_extra_items.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated: {output_file}")
        print(f"📊 Content length: {len(html_content)} characters")
        
        # Detailed validation
        print("\n📋 DETAILED VALIDATION:")
        
        validations = []
        
        # 1. Check title
        if "EXTRA ITEM SLIP" in html_content:
            validations.append("✅ Title: EXTRA ITEM SLIP present")
        else:
            validations.append("❌ Title missing")
        
        # 2. Check work details
        if test_data['work_name'] in html_content:
            validations.append("✅ Work name displayed correctly")
        else:
            validations.append("❌ Work name missing")
            
        if test_data['contractor_name'] in html_content:
            validations.append("✅ Contractor name displayed correctly")
        else:
            validations.append("❌ Contractor name missing")
        
        # 3. Check currency formatting
        currency_count = html_content.count('₹')
        if currency_count >= 9:  # Rate, Amount for 3 items + 3 totals = 9
            validations.append(f"✅ Currency symbols: {currency_count} found")
        else:
            validations.append(f"❌ Currency symbols: only {currency_count} found")
        
        # 4. Check all items present
        item_rows = html_content.count('<tr>') - 1 - 3  # -1 header, -3 summary
        expected_items = len(test_data['extra_items'])
        if item_rows == expected_items:
            validations.append(f"✅ All {expected_items} items present")
        else:
            validations.append(f"❌ Expected {expected_items} items, found {item_rows}")
        
        # 5. Check remarks
        remarks_found = 0
        for item in test_data['extra_items']:
            if item['remarks'] in html_content:
                remarks_found += 1
        
        if remarks_found == len(test_data['extra_items']):
            validations.append(f"✅ All {remarks_found} remarks displayed")
        else:
            validations.append(f"❌ Only {remarks_found}/{len(test_data['extra_items'])} remarks displayed")
        
        # 6. Check totals
        if "Grand Total" in html_content:
            validations.append("✅ Grand Total present")
        else:
            validations.append("❌ Grand Total missing")
            
        if "Tender Premium" in html_content:
            validations.append("✅ Tender Premium calculation present")
        else:
            validations.append("❌ Tender Premium missing")
            
        if "Total Amount of Extra Item Executed" in html_content:
            validations.append("✅ Final total present")
        else:
            validations.append("❌ Final total missing")
        
        # 7. Check styling
        if "text-align: right" in html_content:
            validations.append("✅ Right alignment styles present")
        else:
            validations.append("❌ Right alignment missing")
            
        if "font-family: Arial" in html_content:
            validations.append("✅ Arial font specified")
        else:
            validations.append("❌ Arial font missing")
        
        # 8. Check print optimization
        if "@media print" in html_content:
            validations.append("✅ Print media queries present")
        else:
            validations.append("❌ Print optimization missing")
        
        # Print all validations
        for validation in validations:
            print(f"   {validation}")
        
        # Calculate score
        passed = len([v for v in validations if v.startswith("✅")])
        total = len(validations)
        score = (passed / total) * 100
        
        print(f"\n🏆 VALIDATION SCORE: {score:.1f}% ({passed}/{total})")
        
        # Test PDF generation
        print("\n📄 PDF GENERATION TEST:")
        try:
            merger = PDFMerger()
            pdf_docs = merger.convert_html_to_pdf({"extra_items": html_content})
            
            if pdf_docs and "extra_items_html" in pdf_docs:
                pdf_file = "final_recheck_extra_items.pdf"
                with open(pdf_file, 'wb') as f:
                    f.write(pdf_docs["extra_items_html"])
                print(f"✅ PDF generated: {pdf_file}")
                print(f"📊 PDF size: {len(pdf_docs['extra_items_html'])} bytes")
            else:
                print("❌ PDF generation failed")
        except Exception as e:
            print(f"❌ PDF generation error: {str(e)}")
        
        # Final assessment
        print(f"\n" + "=" * 60)
        print("🎯 FINAL ASSESSMENT")
        print("=" * 60)
        
        if score >= 95:
            print("🌟 EXCELLENT: Extra items output is of exceptional quality!")
            status = "EXCELLENT"
        elif score >= 85:
            print("✅ VERY GOOD: Extra items output meets high standards!")
            status = "VERY GOOD"
        elif score >= 75:
            print("✅ GOOD: Extra items output is satisfactory!")
            status = "GOOD"
        else:
            print("⚠️ NEEDS IMPROVEMENT: Some issues need attention")
            status = "NEEDS WORK"
        
        # Calculate expected totals
        grand_total = sum(item['amount'] for item in test_data['extra_items'])
        premium = grand_total * 0.1
        final_total = grand_total + premium
        
        print(f"\n💰 FINANCIAL VERIFICATION:")
        print(f"   Expected Grand Total: ₹{grand_total:,.2f}")
        print(f"   Expected Premium (10%): ₹{premium:,.2f}")
        print(f"   Expected Final Total: ₹{final_total:,.2f}")
        
        return {
            'status': status,
            'score': score,
            'html_file': output_file,
            'validations': validations
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

if __name__ == "__main__":
    result = final_extra_items_recheck()
    
    if result:
        print(f"\n🚀 RECHECK COMPLETED!")
        print(f"Final Status: {result['status']}")
        print(f"Quality Score: {result['score']:.1f}%")
    else:
        print("\n💥 RECHECK FAILED!")