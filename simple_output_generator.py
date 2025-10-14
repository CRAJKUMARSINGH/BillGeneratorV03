import sys
from pathlib import Path
import json
import os

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

print("Starting output generation...")

try:
    # Import the required classes
    from src.excel_processor import ExcelProcessor
    from src.document_generator import DocumentGenerator
    
    # Path to sample file
    sample_file = "Input_Files_for_tests/sample_infrastructure_bill.xlsx"
    
    print(f"Processing file: {sample_file}")
    print(f"File exists: {os.path.exists(sample_file)}")
    
    # Process Excel file
    print("Processing Excel file...")
    processor = ExcelProcessor(sample_file)
    processed_data = processor.process_all_sheets()
    
    print(f"Processed {len(processed_data)} data categories")
    
    # Save processed data as JSON
    with open("processed_data_output.json", 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
    print("Saved processed data to processed_data_output.json")
    
    # Generate HTML documents
    print("Generating HTML documents...")
    generator = DocumentGenerator(processed_data)
    html_docs = generator.generate_all_html_documents()
    
    print(f"Generated {len(html_docs)} HTML documents")
    
    # Save HTML documents
    for doc_name, content in html_docs.items():
        if content:  # Only save non-empty content
            filename = f"{doc_name}_output.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved HTML: {filename} ({len(content)} characters)")
    
    print("Output generation completed successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()