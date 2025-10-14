#!/usr/bin/env python3
"""
Test Extra Items Format - Generate current output to compare against expected sample
"""

import os
import sys
sys.path.append('src')

from document_generator import DocumentGenerator
from pdf_merger import PDFMerger
import json
from datetime import datetime

def create_sample_extra_items_data():
    """Create comprehensive sample data for extra items testing"""
    return {
        'name_of_work': 'Construction of Electrical Infrastructure',
        'name_of_firm': 'ABC Engineering Solutions Pvt. Ltd.',
        'reference': 'Agreement No. 2024/EE/001 dated 15.03.2024',
        'extra_items': [
            {
                'serial_no': '1',
                'description': 'Extra Excavation for Cable Laying beyond specified depth',
                'unit': 'Cum',
                'quantity': 25.50,
                'rate': 450.00,
                'amount': 11475.00,
                'remark': 'Rock encountered at 1.5m depth'
            },
            {
                'serial_no': '2', 
                'description': 'Additional PVC Conduit 50mm dia for extra cable runs',
                'unit': 'Mtr',
                'quantity': 125.00,
                'rate': 85.00,
                'amount': 10625.00,
                'remark': 'As per site requirement'
            },
            {
                'serial_no': '3',
                'description': 'Extra Junction Boxes (Cast Iron) - 150x150x75mm',
                'unit': 'Nos',
                'quantity': 8.00,
                'rate': 275.00,
                'amount': 2200.00,
                'remark': 'Additional distribution points required'
            },
            {
                'serial_no': '4',
                'description': 'Additional Cable 3.5C x 16 Sq.mm XLPE for extra circuits',
                'unit': 'Mtr',
                'quantity': 180.00,
                'rate': 125.00,
                'amount': 22500.00,
                'remark': 'Extended cable run due to layout change'
            },
        ],
        'grand_total': 46800.00,
        'tender_premium_percent': 0.05,  # 5%
        'tender_premium': 2340.00,
        'total_executed': 49140.00
    }

def test_extra_items_generation():
    """Test the extra items document generation"""
    print("🔍 EXTRA ITEMS FORMAT ANALYSIS")
    print("=" * 50)
    
    # Create sample data
    sample_data = create_sample_extra_items_data()
    
    # Create processed data structure expected by DocumentGenerator
    processed_data = {
        'extra_items_data': sample_data,
        'title_data': {
            'Name of Work ;-': sample_data['name_of_work'],
            'Name of Contractor or supplier :': sample_data['name_of_firm'],
            'Reference to work order or Agreement :': sample_data['reference'],
            'Agreement No.': 'EE/001/2024',
            'Bill Number': 'BILL/001/2024',
            'Date': datetime.now().strftime('%d/%m/%Y')
        }
    }
    
    try:
        # Generate documents
        print("📄 Generating Extra Items Document...")
        doc_gen = DocumentGenerator(processed_data)
        html_docs = doc_gen.generate_all_html_documents()
        
        if 'extra_items_statement' in html_docs:
            # Save HTML for inspection
            html_path = 'test_extra_items_output.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_docs['extra_items_statement'])
            print(f"✅ HTML saved: {html_path} ({len(html_docs['extra_items_statement'])} chars)")
            
            # Generate PDF
            print("📑 Generating PDF...")
            pdf_merger = PDFMerger()
            pdf_path = 'test_extra_items_output.pdf'
            
            # Use the correct method from PDFMerger
            html_docs_for_pdf = {'extra_items': html_docs['extra_items_statement']}
            pdf_docs = pdf_merger.convert_html_to_pdf(html_docs_for_pdf)
            
            if pdf_docs and 'extra_items_html' in pdf_docs:
                # Save PDF bytes to file
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_docs['extra_items_html'])
                print(f"✅ PDF saved: {pdf_path}")
            
            if os.path.exists(pdf_path):
                pdf_size = os.path.getsize(pdf_path) / 1024
                print(f"✅ PDF generated: {pdf_path} ({pdf_size:.1f} KB)")
                
                # Analyze content
                print("\n📊 CONTENT ANALYSIS:")
                print("-" * 30)
                print(f"📋 Items Count: {len(sample_data['extra_items'])}")
                print(f"💰 Grand Total: ₹{sample_data['grand_total']:,.2f}")
                print(f"📈 Premium: {sample_data['tender_premium_percent']*100}% = ₹{sample_data['tender_premium']:,.2f}")
                print(f"🎯 Final Total: ₹{sample_data['total_executed']:,.2f}")
                
                # Check template structure
                print("\n🏗️ TEMPLATE STRUCTURE ANALYSIS:")
                print("-" * 35)
                html_content = html_docs['extra_items_statement']
                
                if 'EXTRA ITEM SLIP' in html_content:
                    print("✅ Title: 'EXTRA ITEM SLIP' found")
                else:
                    print("❌ Title: 'EXTRA ITEM SLIP' missing")
                
                if 'Name of Work:' in html_content:
                    print("✅ Header Info: Work name field present")
                else:
                    print("❌ Header Info: Work name field missing")
                
                if 'Name of Contractor' in html_content:
                    print("✅ Header Info: Contractor field present")
                else:
                    print("❌ Header Info: Contractor field missing")
                
                if 'Reference to work order' in html_content:
                    print("✅ Header Info: Reference field present")
                else:
                    print("❌ Header Info: Reference field missing")
                
                # Check table structure
                print("\n📋 TABLE STRUCTURE ANALYSIS:")
                print("-" * 32)
                expected_headers = ['S.No.', 'Description', 'Unit', 'Qty.', 'Rate', 'Amount', 'Remarks']
                for header in expected_headers:
                    if header in html_content:
                        print(f"✅ Column: {header}")
                    else:
                        print(f"❌ Column: {header} missing")
                
                # Check summary section
                print("\n💰 SUMMARY SECTION ANALYSIS:")
                print("-" * 31)
                if 'Grand Total' in html_content:
                    print("✅ Grand Total row present")
                else:
                    print("❌ Grand Total row missing")
                
                if 'Tender Premium' in html_content:
                    print("✅ Tender Premium row present")
                else:
                    print("❌ Tender Premium row missing")
                
                if 'Total Amount of Extra Item' in html_content:
                    print("✅ Final total row present")
                else:
                    print("❌ Final total row missing")
                
                print("\n🎨 FORMATTING ANALYSIS:")
                print("-" * 25)
                if 'text-right' in html_content:
                    print("✅ Right-aligned currency columns")
                else:
                    print("❌ Currency alignment missing")
                
                if 'text-center' in html_content:
                    print("✅ Center-aligned serial numbers")
                else:
                    print("❌ Serial number alignment missing")
                
                return True
                
            else:
                print("❌ PDF generation failed")
                return False
        else:
            print("❌ Extra items document not generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 EXTRA ITEMS FORMAT TESTING")
    print("=" * 40)
    
    success = test_extra_items_generation()
    
    if success:
        print("\n🎉 TEST COMPLETED SUCCESSFULLY!")
        print("\n📋 NEXT STEPS:")
        print("1. Review test_extra_items_output.html for HTML format")
        print("2. Review test_extra_items_output.pdf for PDF format") 
        print("3. Compare with expected extra_item_output_sample.pdf")
        print("4. Identify any formatting differences")
    else:
        print("\n❌ TEST FAILED - Check errors above")