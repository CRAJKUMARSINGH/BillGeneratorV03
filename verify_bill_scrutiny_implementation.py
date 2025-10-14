import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

print("Verifying Bill Scrutiny Sheet Implementation...")

try:
    # Check if the template file exists
    template_path = current_dir / "templates" / "bill_scrutiny_sheet.html"
    print(f"1. Checking template file: {template_path}")
    if template_path.exists():
        print("   ✅ Template file exists")
        # Check file size
        size = template_path.stat().st_size
        print(f"   📄 File size: {size} bytes")
        if size > 1000:
            print("   ✅ Template file has substantial content")
        else:
            print("   ⚠️ Template file appears small")
    else:
        print("   ❌ Template file NOT found")
    
    # Check if DocumentGenerator has the new method
    from src.document_generator import DocumentGenerator
    print("\n2. Checking DocumentGenerator class...")
    
    # Check if the method exists
    if hasattr(DocumentGenerator, 'generate_bill_scrutiny_sheet'):
        print("   ✅ generate_bill_scrutiny_sheet method exists")
    else:
        print("   ❌ generate_bill_scrutiny_sheet method NOT found")
    
    # Check if the method is called in generate_all_html_documents
    import inspect
    source = inspect.getsource(DocumentGenerator.generate_all_html_documents)
    if 'bill_scrutiny_sheet' in source:
        print("   ✅ Bill scrutiny sheet is included in generate_all_html_documents")
    else:
        print("   ❌ Bill scrutiny sheet is NOT included in generate_all_html_documents")
    
    print("\n🎉 Verification completed!")
    
except Exception as e:
    print(f"❌ Error during verification: {str(e)}")
    import traceback
    traceback.print_exc()