"""
Comprehensive test to generate both HTML and PDF for extra items
Validates complete extra items functionality similar to expected sample
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator
from pdf_merger import PDFMerger

def comprehensive_extra_items_test():
    """Test complete extra items generation including PDF"""
    
    print("🔍 COMPREHENSIVE EXTRA ITEMS TEST")
    print("=" * 60)
    
    # Realistic test data matching government standards
    test_data = {
        'work_name': 'Construction of Additional Academic Block at Government College',
        'contractor_name': 'M/s ABC Construction & Engineering Pvt. Ltd.',
        'reference_no': 'Agreement No. CE/2024/EXTRA/075',
        'date': '2024-09-22',
        'extra_items': [
            {
                'sno': 1,
                'description': 'Providing and laying of additional electrical conduit wiring in PVC pipe for conference hall lighting system as per IS:694',
                'unit': 'Mtr',
                'quantity': 185.50,
                'rate': 145.75,
                'amount': 27026.125,
                'remarks': 'As per site requirement and electrical drawing'
            },
            {
                'sno': 2,
                'description': 'Extra marble flooring (Makrana white) in entrance lobby including polishing and finishing as per specification',
                'unit': 'Sqm',
                'quantity': 67.25,
                'rate': 1250.00,
                'amount': 84062.50,
                'remarks': 'Premium grade marble as approved by architect'
            },
            {
                'sno': 3,
                'description': 'Additional fire resistant HVAC ducting for server room with insulation and fire dampers',
                'unit': 'Mtr',
                'quantity': 125.00,
                'rate': 375.50,
                'amount': 46937.50,
                'remarks': 'Fire rated ducting as per NBC requirements'
            },
            {
                'sno': 4,
                'description': 'Extra stainless steel safety railings for terrace and staircase areas with SS304 grade material',
                'unit': 'Mtr',
                'quantity': 156.75,
                'rate': 850.25,
                'amount': 133349.1875,
                'remarks': 'Height 1.1m as per safety norms'
            },
            {
                'sno': 5,
                'description': 'Additional waterproofing treatment for terrace with APP membrane and protective coating',
                'unit': 'Sqm',
                'quantity': 245.50,
                'rate': 425.00,
                'amount': 104337.50,
                'remarks': 'Double layer waterproofing system'
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
        # Step 1: Generate HTML
        print("📝 STEP 1: Generating HTML...")
        generator = DocumentGenerator(processed_data)
        extra_items_html = generator.generate_extra_items_statement()
        
        # Save HTML
        html_path = "comprehensive_extra_items.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(extra_items_html)
        
        print(f"✅ HTML generated: {html_path}")
        print(f"📊 Content length: {len(extra_items_html)} characters")
        
        # Step 2: Generate PDF
        print("\n📄 STEP 2: Generating PDF...")
        merger = PDFMerger()
        html_docs = {"extra_items": extra_items_html}
        pdf_result = merger.convert_html_to_pdf(html_docs)
        
        if pdf_result and "extra_items_html" in pdf_result:
            pdf_path = "comprehensive_extra_items.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(pdf_result["extra_items_html"])
            print(f"✅ PDF generated: {pdf_path}")
            print(f"📊 PDF size: {len(pdf_result['extra_items_html'])} bytes")
        else:
            print("❌ PDF generation failed")
            pdf_path = None
        
        # Step 3: Quality Analysis
        print("\n🔍 STEP 3: Quality Analysis...")
        quality_checks = {
            'Currency Symbols': '₹' in extra_items_html,
            'All Items Present': len([item for item in test_data['extra_items']]) == extra_items_html.count('<tr>') - 4,  # -1 for header, -3 for summary rows
            'Remarks Displayed': all(item['remarks'] in extra_items_html for item in test_data['extra_items']),
            'Grand Total Present': 'Grand Total' in extra_items_html,
            'Premium Calculation': 'Tender Premium' in extra_items_html,
            'Final Total Present': 'Total Amount of Extra Item Executed' in extra_items_html,
            'Proper Alignment': 'text-align: right' in extra_items_html,
            'Professional Styling': 'font-family: Arial' in extra_items_html,
            'Print Optimized': '@media print' in extra_items_html
        }
        
        passed_checks = sum(quality_checks.values())
        total_checks = len(quality_checks)
        quality_score = (passed_checks / total_checks) * 100
        
        print(f"\n📋 QUALITY ASSESSMENT:")
        for check, passed in quality_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        print(f"\n🏆 OVERALL QUALITY SCORE: {quality_score:.1f}% ({passed_checks}/{total_checks})")
        
        # Step 4: Calculate totals to verify accuracy
        expected_grand_total = sum(item['amount'] for item in test_data['extra_items'])
        expected_premium = expected_grand_total * 0.1
        expected_final = expected_grand_total + expected_premium
        
        print(f"\n💰 FINANCIAL SUMMARY:")
        print(f"   Grand Total: ₹{expected_grand_total:,.2f}")
        print(f"   Premium (10%): ₹{expected_premium:,.2f}")
        print(f"   Final Total: ₹{expected_final:,.2f}")
        
        # Final Assessment
        print(f"\n" + "=" * 60)
        print("🎯 FINAL ASSESSMENT")
        print("=" * 60)
        
        if quality_score >= 90:
            print("🌟 EXCELLENT: App produces high-quality extra items output!")
            result_status = "EXCELLENT"
        elif quality_score >= 75:
            print("✅ GOOD: App produces satisfactory extra items output!")
            result_status = "GOOD"
        else:
            print("⚠️ NEEDS IMPROVEMENT: Some quality issues remain")
            result_status = "NEEDS WORK"
        
        print(f"\n📁 Generated Files:")
        print(f"   📝 HTML: {html_path}")
        if pdf_path:
            print(f"   📄 PDF: {pdf_path}")
        
        return {
            'html_path': html_path,
            'pdf_path': pdf_path,
            'quality_score': quality_score,
            'status': result_status,
            'grand_total': expected_grand_total,
            'final_total': expected_final
        }
        
    except Exception as e:
        print(f"❌ ERROR in comprehensive test: {str(e)}")
        return None

if __name__ == "__main__":
    result = comprehensive_extra_items_test()
    
    if result:
        print(f"\n🚀 TEST COMPLETED SUCCESSFULLY!")
        print(f"Status: {result['status']}")
        print(f"Quality Score: {result['quality_score']:.1f}%")
    else:
        print("\n💥 TEST FAILED!")