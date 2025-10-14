#!/usr/bin/env python3
"""
Direct Extra Items Template Test - Test template rendering directly
"""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def test_extra_items_template():
    """Test the extra items template directly"""
    print("🔍 DIRECT EXTRA ITEMS TEMPLATE TEST")
    print("=" * 45)
    
    # Create sample data matching template variables
    sample_data = {
        'name_of_work': 'Construction of Electrical Infrastructure Project',
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
    
    try:
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('extra_items.html')
        
        # Render template
        html_content = template.render(data=sample_data)
        
        # Save rendered HTML
        output_file = 'test_extra_items_direct.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Template rendered successfully: {output_file}")
        print(f"📄 Content size: {len(html_content):,} characters")
        
        # Analyze content structure
        print("\n📊 CONTENT ANALYSIS:")
        print("-" * 25)
        
        # Check title
        if 'EXTRA ITEM SLIP' in html_content:
            print("✅ Title: 'EXTRA ITEM SLIP' present")
        else:
            print("❌ Title: Missing or incorrect")
        
        # Check header information
        header_fields = [
            ('Name of Work:', sample_data['name_of_work']),
            ('Name of Contractor', sample_data['name_of_firm']),
            ('Reference to work order', sample_data['reference'])
        ]
        
        for field_name, expected_value in header_fields:
            if field_name in html_content and expected_value in html_content:
                print(f"✅ Header: {field_name} with correct data")
            else:
                print(f"❌ Header: {field_name} missing or incorrect")
        
        # Check table headers
        expected_headers = ['S.No.', 'Description', 'Unit', 'Qty.', 'Rate', 'Amount', 'Remarks']
        print("\n📋 TABLE HEADERS:")
        print("-" * 20)
        for header in expected_headers:
            if header in html_content:
                print(f"✅ Column: {header}")
            else:
                print(f"❌ Column: {header} missing")
        
        # Check data rows
        print(f"\n📝 DATA ROWS:")
        print("-" * 15)
        for i, item in enumerate(sample_data['extra_items'], 1):
            if item['description'] in html_content:
                print(f"✅ Item {i}: {item['description'][:50]}...")
            else:
                print(f"❌ Item {i}: Missing from output")
        
        # Check summary calculations
        print(f"\n💰 SUMMARY SECTION:")
        print("-" * 20)
        
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
        
        # Check formatting classes
        print(f"\n🎨 FORMATTING:")
        print("-" * 15)
        
        if 'text-right' in html_content:
            print("✅ Right-aligned currency columns")
        else:
            print("❌ Currency alignment missing")
        
        if 'text-center' in html_content:
            print("✅ Center-aligned serial numbers")
        else:
            print("❌ Serial number alignment missing")
        
        # Check if values are properly formatted
        print(f"\n🔢 VALUE FORMATTING:")
        print("-" * 20)
        
        # Check specific values
        test_values = [
            ('25.50', 'Quantity formatting'),
            ('450.00', 'Rate formatting'), 
            ('11475.00', 'Amount formatting'),
            ('46800.00', 'Grand total formatting'),
            ('5.00%', 'Premium percentage'),
            ('49140.00', 'Final total')
        ]
        
        for value, description in test_values:
            if value in html_content:
                print(f"✅ {description}: {value}")
            else:
                print(f"❌ {description}: {value} not found")
        
        print(f"\n🎉 TEMPLATE TEST COMPLETED!")
        print(f"📁 Output file: {output_file}")
        print("💡 Review the HTML file to compare with expected format")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing template: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_extra_items_template()