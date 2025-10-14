"""
Final test script to validate the updated extra items template
Tests if our app now produces proper output similar to expected format
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator

def test_updated_extra_items():
    """Test the updated extra items template"""
    
    # Create test data with remarks
    test_data = {
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
    
    # Prepare processed data format
    processed_data = {
        'title': {
            'project_name': test_data['work_name'],
            'contractor_name': test_data['contractor_name'],
            'agreement_no': test_data['reference_no']
        },
        'extra_items': test_data['extra_items']
    }
    
    try:
        # Generate extra items HTML with updated template
        generator = DocumentGenerator(processed_data)
        extra_items_html = generator.generate_extra_items_statement()
        
        # Save for inspection
        output_path = "test_final_extra_items.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extra_items_html)
        
        print("✅ FINAL EXTRA ITEMS TEST COMPLETE")
        print("=" * 50)
        print(f"📁 Generated output: {output_path}")
        print(f"📊 HTML Content Length: {len(extra_items_html)} characters")
        
        # Check for improvements
        improvements = []
        if '₹' in extra_items_html:
            improvements.append("✅ Currency symbols (₹) added")
        else:
            improvements.append("❌ Currency symbols still missing")
            
        if '@media print' in extra_items_html:
            improvements.append("✅ Print optimization styles added")
        else:
            improvements.append("❌ Print styles still missing")
            
        if 'As per site requirement' in extra_items_html:
            improvements.append("✅ Remarks properly displayed")
        else:
            improvements.append("❌ Remarks not showing")
            
        if 'Total Amount of Extra Item Executed' in extra_items_html:
            improvements.append("✅ Final amount calculation present")
        else:
            improvements.append("❌ Final amount missing")
        
        print("\n📋 VALIDATION RESULTS:")
        for improvement in improvements:
            print(f"   {improvement}")
        
        # Count successful improvements
        success_count = len([i for i in improvements if i.startswith("✅")])
        total_count = len(improvements)
        score = (success_count / total_count) * 100
        
        print(f"\n🏆 Final Score: {score:.1f}% ({success_count}/{total_count} checks passed)")
        
        if score >= 75:
            print("✅ SUCCESS: App now produces proper extra items output!")
        else:
            print("❌ NEEDS WORK: Some issues still remain")
            
        return extra_items_html, score >= 75
        
    except Exception as e:
        print(f"❌ Error in final test: {str(e)}")
        return None, False

if __name__ == "__main__":
    test_updated_extra_items()