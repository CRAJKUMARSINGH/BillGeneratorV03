import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

print("=" * 60)
print("MANUAL TEST: Bill Scrutiny Sheet Generation")
print("=" * 60)

# Check if required files exist
print("\n1. CHECKING REQUIRED FILES:")

# Check template file
template_path = current_dir / "templates" / "bill_scrutiny_sheet.html"
print(f"   Template file: {'✅ EXISTS' if template_path.exists() else '❌ MISSING'}")

# Check DocumentGenerator
doc_generator_class = None
try:
    from src.document_generator import DocumentGenerator
    doc_generator_class = DocumentGenerator
    print("   DocumentGenerator: ✅ IMPORT SUCCESSFUL")
    
    # Check if method exists
    if hasattr(DocumentGenerator, 'generate_bill_scrutiny_sheet'):
        print("   generate_bill_scrutiny_sheet method: ✅ FOUND")
    else:
        print("   generate_bill_scrutiny_sheet method: ❌ NOT FOUND")
        
    # Check if method is called in main generation
    import inspect
    source = inspect.getsource(DocumentGenerator.generate_all_html_documents)
    if 'bill_scrutiny_sheet' in source:
        print("   Integration in generate_all_html_documents: ✅ CONFIRMED")
    else:
        print("   Integration in generate_all_html_documents: ❌ NOT FOUND")
        
except ImportError as e:
    print(f"   DocumentGenerator: ❌ IMPORT FAILED - {str(e)}")

print("\n2. CREATING TEST DATA:")
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

print("   ✅ Sample data created")

print("\n3. TESTING GENERATION:")
if doc_generator_class:
    try:
        # Create DocumentGenerator instance
        doc_generator = doc_generator_class(sample_data)
        print("   ✅ DocumentGenerator instance created")
        
        # Test the specific method
        scrutiny_sheet = doc_generator.generate_bill_scrutiny_sheet()
        print(f"   ✅ Bill scrutiny sheet generated ({len(scrutiny_sheet)} characters)")
        
        # Save for inspection
        output_file = "manual_test_bill_scrutiny_output.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(scrutiny_sheet)
        print(f"   ✅ Output saved to {output_file}")
        
        # Test main generation method
        all_docs = doc_generator.generate_all_html_documents()
        print(f"   ✅ All HTML documents generated ({len(all_docs)} documents)")
        
        if 'bill_scrutiny_sheet' in all_docs:
            print("   ✅ Bill scrutiny sheet included in all documents")
            size = len(all_docs['bill_scrutiny_sheet'])
            print(f"   📄 Bill scrutiny sheet size: {size} characters")
        else:
            print("   ❌ Bill scrutiny sheet NOT included in all documents")
            
    except Exception as e:
        print(f"   ❌ Generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("   ❌ DocumentGenerator not available, skipping generation tests")

print("\n4. VERIFYING OUTPUT:")
try:
    # Check if output file exists
    if os.path.exists("manual_test_bill_scrutiny_output.html"):
        print("   ✅ Output file created successfully")
        
        # Check content
        with open("manual_test_bill_scrutiny_output.html", 'r', encoding='utf-8') as f:
            content = f.read()
            
        if len(content) > 1000:
            print("   ✅ Output file has substantial content")
        else:
            print("   ⚠️ Output file content appears minimal")
            
        # Check for key elements
        checks = [
            ("<title>Bill Scrutiny Sheet</title>", "Title tag"),
            ("<h2>________ BILL SCRUTINY SHEET</h2>", "Header"),
            ("Chargeable Head", "Key field"),
            ("Test Infrastructure Project", "Project name"),
            ("Test Contractor Ltd", "Contractor name")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description} found")
            else:
                print(f"   ❌ {description} NOT found")
    else:
        print("   ❌ Output file NOT created")
        
except Exception as e:
    print(f"   ❌ Verification failed: {str(e)}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)