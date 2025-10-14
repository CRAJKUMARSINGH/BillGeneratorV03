"""
Integration example showing how to use the new output folder system
with the existing Bill Generator application
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from enhanced_bill_generator import EnhancedBillGenerator

def integrate_with_existing_app():
    """
    Example of how to integrate the output folder system 
    with your existing bill generation workflow
    """
    
    print("🔗 INTEGRATION EXAMPLE")
    print("=" * 50)
    
    # Initialize with your preferred output directory
    # You can change this to any location you prefer
    generator = EnhancedBillGenerator("C:/BillOutputs")
    
    # Example: Processing files from Input_Files_for_tests directory
    input_dir = Path("Input_Files_for_tests")
    
    if input_dir.exists():
        print(f"📁 Found input directory: {input_dir}")
        
        # List available input files
        excel_files = list(input_dir.glob("*.xlsx"))
        print(f"📊 Found {len(excel_files)} Excel files")
        
        if excel_files:
            # Use first Excel file for demonstration
            sample_file = excel_files[0]
            print(f"📄 Using sample file: {sample_file.name}")
            
            # In a real integration, you would:
            # 1. Process the Excel file using your existing ExcelProcessor
            # 2. Extract project and contractor information
            # 3. Generate documents using the enhanced generator
            
            # For this example, we'll use sample data
            sample_processed_data = {
                'title': {
                    'project_name': f'Project from {sample_file.stem}',
                    'contractor_name': 'Sample Contractor from File',
                    'bill_number': 'BILL-2024-SAMPLE',
                    'agreement_no': 'AGR/2024/SAMPLE'
                },
                'bill_quantity': [
                    {
                        'description': 'Sample work item from Excel',
                        'unit': 'Nos',
                        'quantity': 100,
                        'rate': 250.0,
                        'amount': 25000.0
                    }
                ],
                'totals': {
                    'grand_total': 25000.0,
                    'gst_amount': 4500.0,
                    'total_with_gst': 29500.0
                }
            }
            
            # Generate using organized output system
            print(f"\n📝 Generating documents with organized output...")
            result = generator.generate_complete_bill_package(
                processed_data=sample_processed_data,
                project_name=f"Project from {sample_file.stem}",
                contractor_name="Sample Contractor"
            )
            
            if result['errors']:
                print("❌ Generation errors:")
                for error in result['errors']:
                    print(f"   - {error}")
            else:
                print("✅ Documents generated successfully!")
                print(f"📁 Session: {result['session_info']['session_id']}")
                
                # Show generated file paths
                print(f"\n📄 Generated Files:")
                for file_type, files in [
                    ('HTML', result['html_files']), 
                    ('PDF', result['pdf_files']), 
                    ('Excel', result['excel_files'])
                ]:
                    if files:
                        print(f"   {file_type} Files:")
                        for name, path in files.items():
                            print(f"      - {name}: {path}")
        else:
            print("❌ No Excel files found for processing")
    else:
        print(f"❌ Input directory not found: {input_dir}")
        print("💡 This example expects the Input_Files_for_tests directory")
    
    # Show current output statistics
    print(f"\n📊 Current Output Statistics:")
    stats = generator.get_output_statistics()
    if 'error' not in stats:
        print(f"   Sessions: {stats['total_sessions']}")
        print(f"   Files: {stats['total_files']}")
        print(f"   Size: {stats['total_size_mb']} MB")
    else:
        print(f"   No outputs yet - {stats['error']}")

def streamlit_integration_example():
    """
    Example of how to integrate with Streamlit app
    """
    print(f"\n🎨 STREAMLIT INTEGRATION EXAMPLE")
    print("=" * 50)
    
    print("""
    # In your streamlit_app.py, you can integrate like this:
    
    import streamlit as st
    from enhanced_bill_generator import EnhancedBillGenerator
    
    # Initialize at the top of your app
    if 'output_generator' not in st.session_state:
        st.session_state.output_generator = EnhancedBillGenerator("outputs")
    
    # When user uploads files and processes them:
    if st.button("Generate Documents"):
        with st.spinner("Generating organized documents..."):
            result = st.session_state.output_generator.generate_complete_bill_package(
                processed_data=processed_data,
                project_name=project_info['name'],
                contractor_name=project_info['contractor']
            )
            
            if result['errors']:
                st.error("Generation failed!")
                for error in result['errors']:
                    st.error(f"- {error}")
            else:
                st.success(f"Documents generated! Session: {result['session_info']['session_id']}")
                
                # Provide download links
                for file_type, files in result.items():
                    if file_type.endswith('_files') and files:
                        st.subheader(f"{file_type.replace('_files', '').upper()} Files")
                        for name, path in files.items():
                            with open(path, 'rb') as f:
                                st.download_button(
                                    label=f"Download {name}",
                                    data=f.read(),
                                    file_name=Path(path).name,
                                    mime="application/octet-stream"
                                )
    
    # Show recent outputs in sidebar
    with st.sidebar:
        st.subheader("Recent Outputs")
        recent = st.session_state.output_generator.list_recent_outputs(7)
        for session in recent[:5]:
            st.write(f"📅 {session['date']} - {session.get('project_name', 'Unknown')}")
    """)

if __name__ == "__main__":
    integrate_with_existing_app()
    streamlit_integration_example()
    
    print(f"\n🎯 INTEGRATION COMPLETE!")
    print("=" * 50)
    print("✅ Output folder system is ready for use!")
    print("📁 Check the generated folders and files")
    print("📖 See OUTPUT_FOLDER_SYSTEM_GUIDE.md for detailed documentation")