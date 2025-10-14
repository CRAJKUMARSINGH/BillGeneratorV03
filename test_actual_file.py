#!/usr/bin/env python3
"""
Test script to process actual Excel file and generate HTML output
"""

import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.excel_processor import ExcelProcessor
from src.document_generator import DocumentGenerator
import json

def test_actual_file():
    """Test processing actual Excel file"""
    try:
        # Path to sample file
        sample_file = "Input_Files_for_tests/sample_infrastructure_bill.xlsx"
        
        print(f"🔍 Testing with file: {sample_file}")
        
        # Check if file exists
        if not os.path.exists(sample_file):
            print(f"❌ File not found: {sample_file}")
            return False
        
        # Process Excel file
        print("📄 Processing Excel file...")
        processor = ExcelProcessor(sample_file)
        processed_data = processor.process_all_sheets()
        
        print(f"✅ Processed {len(processed_data)} data categories")
        
        # Print summary of processed data
        for key, value in processed_data.items():
            if isinstance(value, list):
                print(f"   - {key}: {len(value)} items")
            elif isinstance(value, dict):
                print(f"   - {key}: {len(value)} fields")
            else:
                print(f"   - {key}: {value}")
        
        # Generate HTML documents
        print("🌐 Generating HTML documents...")
        generator = DocumentGenerator(processed_data)
        html_docs = generator.generate_all_html_documents()
        
        print(f"✅ Generated {len(html_docs)} HTML documents")
        
        # Check content of HTML documents
        for doc_name, content in html_docs.items():
            content_length = len(content) if content else 0
            print(f"   - {doc_name}: {content_length} characters")
            
            # Save HTML to file for inspection
            output_file = f"test_{doc_name}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content or "")
            print(f"   - Saved to: {output_file}")
        
        # Save processed data as JSON for inspection
        with open("test_processed_data.json", 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
        print("💾 Processed data saved to: test_processed_data.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Actual Excel File Processing")
    print("=" * 50)
    
    success = test_actual_file()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")