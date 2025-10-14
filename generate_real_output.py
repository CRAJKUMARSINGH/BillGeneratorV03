#!/usr/bin/env python3
"""
Script to process actual Excel file and generate real output files for review
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.excel_processor import ExcelProcessor
from src.document_generator import DocumentGenerator
from src.output_manager import OutputManager
from src.pdf_merger import PDFMerger

def generate_real_output():
    """Generate real output files from actual Excel file"""
    try:
        # Create output directory
        output_dir = current_dir / "REAL_OUTPUT_REVIEW"
        output_dir.mkdir(exist_ok=True)
        
        print(f"📁 Creating output directory: {output_dir}")
        
        # Path to sample file
        sample_file = "Input_Files_for_tests/sample_infrastructure_bill.xlsx"
        
        print(f"🔍 Processing file: {sample_file}")
        
        # Check if file exists
        if not os.path.exists(sample_file):
            print(f"❌ File not found: {sample_file}")
            # Try alternative locations
            alternative_paths = [
                "Input_Files_for_tests/sample_infrastructure_bill.xlsx",
                "input_files/sample_infrastructure_bill.xlsx",
                "sample_infrastructure_bill.xlsx"
            ]
            
            found = False
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    sample_file = alt_path
                    found = True
                    print(f"✅ Found file at: {sample_file}")
                    break
            
            if not found:
                print("❌ No sample file found. Creating sample data instead...")
                return create_sample_output(output_dir)
        
        # Process Excel file
        print("📄 Processing Excel file...")
        processor = ExcelProcessor(sample_file)
        processed_data = processor.process_all_sheets()
        
        print(f"✅ Processed {len(processed_data)} data categories")
        
        # Save processed data as JSON
        data_file = output_dir / "processed_data.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, default=str, ensure_ascii=False)
        print(f"💾 Processed data saved to: {data_file}")
        
        # Generate HTML documents
        print("🌐 Generating HTML documents...")
        generator = DocumentGenerator(processed_data)
        html_docs = generator.generate_all_html_documents()
        
        print(f"✅ Generated {len(html_docs)} HTML documents")
        
        # Save HTML documents
        html_dir = output_dir / "html_documents"
        html_dir.mkdir(exist_ok=True)
        
        for doc_name, content in html_docs.items():
            if content:  # Only save non-empty content
                html_file = html_dir / f"{doc_name}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"💾 HTML saved: {html_file} ({len(content)} characters)")
        
        # Generate PDF documents
        print("📑 Generating PDF documents...")
        pdf_merger = PDFMerger()
        pdf_docs = pdf_merger.convert_html_to_pdf(html_docs)
        
        print(f"✅ Generated {len(pdf_docs)} PDF documents")
        
        # Save PDF documents
        pdf_dir = output_dir / "pdf_documents"
        pdf_dir.mkdir(exist_ok=True)
        
        for doc_name, pdf_bytes in pdf_docs.items():
            if pdf_bytes:  # Only save non-empty content
                pdf_file = pdf_dir / f"{doc_name}.pdf"
                with open(pdf_file, 'wb') as f:
                    f.write(pdf_bytes)
                print(f"💾 PDF saved: {pdf_file} ({len(pdf_bytes)} bytes)")
        
        # Generate Excel outputs
        print("📊 Generating Excel documents...")
        excel_docs = generator.generate_excel_outputs(processed_data)
        
        print(f"✅ Generated {len(excel_docs)} Excel documents")
        
        # Save Excel documents
        excel_dir = output_dir / "excel_documents"
        excel_dir.mkdir(exist_ok=True)
        
        for doc_name, excel_bytes in excel_docs.items():
            if excel_bytes:  # Only save non-empty content
                excel_file = excel_dir / f"{doc_name}.xlsx"
                with open(excel_file, 'wb') as f:
                    f.write(excel_bytes)
                print(f"💾 Excel saved: {excel_file} ({len(excel_bytes)} bytes)")
        
        # Create summary report
        summary = {
            "processing_timestamp": datetime.now().isoformat(),
            "input_file": sample_file,
            "data_categories": len(processed_data),
            "html_documents": len(html_docs),
            "pdf_documents": len(pdf_docs),
            "excel_documents": len(excel_docs),
            "output_directory": str(output_dir)
        }
        
        summary_file = output_dir / "summary_report.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"📋 Summary report saved: {summary_file}")
        
        print(f"\n🎉 Real output files generated successfully!")
        print(f"📂 Output location: {output_dir}")
        print(f"📄 Files generated:")
        print(f"   - Processed Data: 1 JSON file")
        print(f"   - HTML Documents: {len(html_docs)} files")
        print(f"   - PDF Documents: {len(pdf_docs)} files")
        print(f"   - Excel Documents: {len(excel_docs)} files")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_output(output_dir):
    """Create sample output when no real file is available"""
    print("📝 Creating sample output data...")
    
    # Sample processed data
    sample_data = {
        "title": {
            "project_name": "Sample Infrastructure Project",
            "contractor_name": "Sample Contractor Ltd",
            "work_order_no": "WO-2025-001",
            "location": "Sample Location",
            "agreement_no": "AG-2025-001"
        },
        "work_order": [
            {
                "serial_no": "1",
                "description": "Earthwork Excavation",
                "unit": "Cum",
                "quantity": 100.0,
                "rate": 500.0,
                "amount": 50000.0,
                "remark": "As per specifications"
            },
            {
                "serial_no": "2",
                "description": "Concrete Work M20",
                "unit": "Cum",
                "quantity": 50.0,
                "rate": 2500.0,
                "amount": 125000.0,
                "remark": "RCC work"
            }
        ],
        "bill_quantity": [
            {
                "serial_no": "1",
                "description": "Earthwork Excavation",
                "unit": "Cum",
                "quantity": 95.0,
                "rate": 500.0,
                "amount": 47500.0,
                "remark": "Executed quantity"
            },
            {
                "serial_no": "2",
                "description": "Concrete Work M20",
                "unit": "Cum",
                "quantity": 52.0,
                "rate": 2500.0,
                "amount": 130000.0,
                "remark": "Executed quantity"
            }
        ],
        "extra_items": [
            {
                "serial_no": "1",
                "description": "Additional Concrete Work",
                "unit": "Cum",
                "quantity": 5.0,
                "rate": 2600.0,
                "amount": 13000.0,
                "approval_ref": "APR-2025-001",
                "remark": "Extra work approved"
            }
        ],
        "totals": {
            "bill_quantity_total": 177500.0,
            "extra_items_total": 13000.0,
            "grand_total": 190500.0,
            "gst_rate": 18.0,
            "gst_amount": 34290.0,
            "total_with_gst": 224790.0,
            "net_payable": 224790.0
        }
    }
    
    # Save sample processed data
    data_file = output_dir / "processed_data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, default=str, ensure_ascii=False)
    print(f"💾 Sample data saved to: {data_file}")
    
    # Generate sample HTML documents
    generator = DocumentGenerator(sample_data)
    html_docs = generator.generate_all_html_documents()
    
    # Save HTML documents
    html_dir = output_dir / "html_documents"
    html_dir.mkdir(exist_ok=True)
    
    for doc_name, content in html_docs.items():
        if content:  # Only save non-empty content
            html_file = html_dir / f"{doc_name}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Sample HTML saved: {html_file} ({len(content)} characters)")
    
    print(f"\n🎉 Sample output files generated successfully!")
    print(f"📂 Output location: {output_dir}")
    return True

if __name__ == "__main__":
    print("🧪 Generating Real Output Files for Review")
    print("=" * 50)
    
    success = generate_real_output()
    
    if success:
        print("\n✅ Output generation completed successfully!")
        print("📂 Check the REAL_OUTPUT_REVIEW folder for generated files")
    else:
        print("\n❌ Output generation failed!")