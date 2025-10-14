import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

print("Testing Bill Scrutiny Sheet Generation...")

try:
    # Import the required classes
    from src.document_generator import DocumentGenerator
    
    # Sample data for testing
    sample_data = {
        'title': {
            'project_name': 'Test Infrastructure Project',
            'contractor_name': 'Test Contractor Ltd',
            'agreement_no': 'AG-2025-001',
            'Name of Work ;-': 'Road Construction',
            'Name of Contractor or supplier :': 'Test Contractor Ltd',
            'Agreement No :': 'AG-2025-001',
            'Date of commencement  :': '01/01/2025',
            'Schedule Date of completion  :': '31/12/2025',
            'Actual date of completion  :': '31/12/2025'
        },
        'totals': {
            'grand_total': 11300.0,
            'gst_amount': 2034.0,
            'total_with_gst': 13334.0,
            'work_order_amount': 12000.0,
            'payable': 11300.0,
            'extra_items_sum': 500.0,
            'sd_amount': 1130.0,
            'it_amount': 226.0,
            'lc_amount': 113.0,
            'net_payable': 9835.0
        },
        'notes': [
            'Work completed as per schedule',
            'All measurements verified',
            'Quality as per specifications'
        ]
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
        
        # Save each document for inspection
        if content:
            filename = f"test_{doc_name}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"      - Saved to: {filename}")
    
    # Check specifically for bill scrutiny sheet
    if 'bill_scrutiny_sheet' in html_docs:
        print("\n✅ Bill Scrutiny Sheet generation successful!")
        content_length = len(html_docs['bill_scrutiny_sheet'])
        print(f"   Size: {content_length} characters")
        
        if content_length > 1000:
            print("   ✅ Content appears substantial (not blank)")
        else:
            print("   ⚠️ Content appears minimal")
    else:
        print("\n❌ Bill Scrutiny Sheet not found in generated documents")
    
    print("\n🎉 Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()