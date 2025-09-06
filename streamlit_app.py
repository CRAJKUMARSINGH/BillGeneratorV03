"""
BillGenerator Optimized - Streamlit Cloud Deployment Version
Main application entry point for cloud deployment
"""

import streamlit as st
import pandas as pd
import os
import sys
import zipfile
import tempfile
from datetime import datetime
import traceback
import logging
from pathlib import Path

# Add src to Python path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

try:
    from excel_processor import ExcelProcessor
    from latex_generator import LaTeXGenerator
    from utils import validate_excel_file, get_timestamp, sanitize_filename
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required modules are in the src directory")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Infrastructure Billing System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/BillGeneratorV03',
        'Report a bug': "mailto:your-email@domain.com",
        'About': "Professional Infrastructure Billing System - Cloud Version"
    }
)

def inject_custom_css():
    """Inject custom CSS for professional appearance"""
    st.markdown("""
    <style>
    .main > div {
        padding: 2rem 1rem;
    }
    
    .header-container {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #81C784 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        text-align: center;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .upload-card {
        background: #ffffff;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-card:hover {
        border-color: #45a049;
        background: #f8fff8;
    }
    
    .results-container {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the professional header"""
    st.markdown("""
    <div class="header-container">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🏗️</div>
            <div class="header-title">Infrastructure Billing System</div>
            <div class="header-subtitle">Professional Document Generation & Compliance Solution</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_instructions():
    """Display usage instructions"""
    with st.expander("📖 How to Use This Application", expanded=True):
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        1. **📁 Prepare Your Excel File**
           - Use the standard Excel template format
           - Ensure all required sheets are present: Title, Work Order, Bill Quantity
           - Optional: Extra Items sheet for additional work
        
        2. **📤 Upload Your File**
           - Click the upload area below
           - Select your .xlsx file
           - Maximum file size: 50MB
        
        3. **⚡ Processing**
           - The system will validate and process your file
           - Progress will be shown in real-time
           - Multiple document formats will be generated
        
        4. **📦 Download Results**
           - Download the complete package as a ZIP file
           - Contains HTML, PDF, and Excel outputs
           - Professional formatting and compliance ready
        """)

def simple_process_excel(uploaded_file):
    """Simplified processing for cloud deployment"""
    try:
        # Basic validation
        if not uploaded_file.name.endswith('.xlsx'):
            st.error("Please upload a valid Excel (.xlsx) file")
            return None
        
        st.info("🔄 Processing file... This may take a moment.")
        
        # Create a simple processor
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Read the Excel file
            df = pd.read_excel(tmp_file_path, sheet_name=None)
            
            # Basic processing
            results = {
                'sheets': list(df.keys()),
                'total_sheets': len(df),
                'filename': uploaded_file.name
            }
            
            # Simple analysis
            for sheet_name, sheet_data in df.items():
                if not sheet_data.empty:
                    results[f'{sheet_name}_rows'] = len(sheet_data)
                    results[f'{sheet_name}_columns'] = len(sheet_data.columns)
            
            st.success("✅ File processed successfully!")
            return results
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return None

def main():
    """Main application function"""
    inject_custom_css()
    display_header()
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📊 Application Info")
        st.info("""
        **Version:** 3.0 (Cloud)
        **Developer:** Rajkumar
        **Purpose:** Infrastructure Billing
        **Platform:** Streamlit Cloud
        """)
        
        st.markdown("### 🎯 Features")
        st.markdown("""
        - ✅ Excel Processing
        - ✅ PDF Generation  
        - ✅ LaTeX Templates
        - ✅ ZIP Packaging
        - ✅ Cloud Deployment
        """)
    
    # Main content
    display_instructions()
    
    # File upload section
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Your Excel File")
    uploaded_file = st.file_uploader(
        "Choose your Excel file (.xlsx format)",
        type=['xlsx'],
        help="Upload your infrastructure billing Excel file for processing"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display file info
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📁 Filename", uploaded_file.name)
        
        with col2:
            file_size = len(uploaded_file.getvalue()) / 1024 / 1024
            st.metric("📏 File Size", f"{file_size:.2f} MB")
        
        with col3:
            st.metric("📅 Upload Time", datetime.now().strftime("%H:%M:%S"))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process file
        if st.button("🚀 Process File", type="primary"):
            results = simple_process_excel(uploaded_file)
            
            if results:
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                st.markdown("### 📊 Processing Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📋 Sheets Found:**")
                    for sheet in results['sheets']:
                        st.write(f"• {sheet}")
                
                with col2:
                    st.write("**📈 Sheet Statistics:**")
                    st.write(f"• Total Sheets: {results['total_sheets']}")
                    for key, value in results.items():
                        if key.endswith('_rows'):
                            sheet_name = key.replace('_rows', '')
                            st.write(f"• {sheet_name}: {value} rows")
                
                st.success("🎉 Processing completed successfully!")
                st.info("💡 **Note:** Full processing features are available in the local version. This cloud version provides basic file analysis.")
                
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
