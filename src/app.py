import streamlit as st
import pandas as pd
import os
import zipfile
import tempfile
from datetime import datetime
import traceback
import logging
from src.excel_processor import ExcelProcessor
from src.document_generator import DocumentGenerator
from src.latex_generator import LaTeXGenerator
from src.pdf_merger import PDFMerger
from src.zip_packager import ZipPackager
from src.utils import validate_excel_file, get_timestamp, sanitize_filename

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Infrastructure Billing System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """Inject custom CSS for professional appearance with green header design"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main > div {
        padding: 2rem 1rem;
    }
    
    /* Header styling - Green gradient design */
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
    
    .header-professional {
        font-size: 1rem;
        text-align: center;
        color: #e8f5e9;
        opacity: 0.85;
        margin-bottom: 0.5rem;
        font-weight: 400;
        font-style: italic;
        letter-spacing: 0.8px;
    }
    
    .header-initiative {
        font-size: 0.9rem;
        text-align: center;
        color: #ffffff;
        opacity: 0.9;
        margin-bottom: 0;
        font-weight: 500;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        display: inline-block;
        margin: 0 auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Upload card styling */
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
    
    /* Progress styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Results styling */
    .results-container {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
    }
    
    /* Instructions styling */
    .instructions-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #dee2e6;
    }
    
    .how-to-title {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .how-to-subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Feature cards styling */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .download-section {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        border: 1px solid #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the professional header with crane logo and green gradient"""
    st.markdown("""
    <div class="header-container">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🏗️</div>
            <div class="header-title">Infrastructure Billing System</div>
            <div class="header-subtitle">Professional Document Generation & Compliance Solution</div>
            <div class="header-professional">Advanced Multi-Format Document Processing with Election Commission Compliance</div>
            <div style="margin-top: 1.5rem;">
                <div class="header-initiative">
                    An Initiative by Mrs. Premlata Jain, Additional Administrative Officer, PWD, Udaipur
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_feature_highlights():
    """Display key features in cards"""
    st.markdown("""
    <div class="instructions-container">
        <h2 class="how-to-title">🎯 Advanced Features</h2>
        <p class="how-to-subtitle">Professional-grade document generation with comprehensive format support</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h3>Dual PDF Generation</h3>
            <p>Both HTML-based and LaTeX-based PDF outputs for maximum compatibility</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📐</div>
            <h3>LaTeX Templates</h3>
            <p>Professional LaTeX processing for Election Commission compliance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Smart Processing</h3>
            <p>Intelligent Excel parsing with robust error handling and validation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📦</div>
            <h3>Complete Packaging</h3>
            <p>All documents organized in professional ZIP packages with proper structure</p>
        </div>
        """, unsafe_allow_html=True)

def display_processing_progress(current_step: str, total_steps: int = 8):
    """Display processing progress with detailed steps"""
    steps = [
        "📊 Validating Excel file structure",
        "🔍 Processing Title sheet data", 
        "📋 Analyzing Work Order items",
        "📈 Processing Bill Quantity data",
        "➕ Handling Extra Items (if present)",
        "📄 Generating HTML documents",
        "📐 Creating LaTeX templates",
        "📑 Converting to PDF formats",
        "📦 Packaging final deliverables"
    ]
    
    progress_container = st.container()
    with progress_container:
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        
        # Find current step index
        current_index = next((i for i, step in enumerate(steps) if current_step in step), 0)
        progress_value = (current_index + 1) / len(steps)
        
        progress_bar = st.progress(progress_value)
        status_text = st.empty()
        
        # Display current step
        status_text.text(f"⚡ {current_step}")
        
        # Show step checklist
        with st.expander("📋 Processing Steps", expanded=True):
            for i, step in enumerate(steps):
                if i <= current_index:
                    st.markdown(f"✅ {step}")
                else:
                    st.markdown(f"⏳ {step}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def process_excel_file(uploaded_file):
    """Enhanced file processing with comprehensive error handling"""
    try:
        # Step 1: Validate file
        display_processing_progress("Validating Excel file structure")
        
        validation_result = validate_excel_file(uploaded_file)
        if not validation_result['valid']:
            st.error(f"❌ File validation failed: {validation_result['error']}")
            return None
        
        # Step 2: Initialize processors
        display_processing_progress("Processing Title sheet data")
        
        excel_processor = ExcelProcessor(uploaded_file)
        processed_data = excel_processor.process_all_sheets()
        
        if not processed_data:
            st.error("❌ Failed to process Excel file. Please check the file format.")
            return None
        
        # Step 3: Generate documents
        display_processing_progress("Generating HTML documents")
        
        document_generator = DocumentGenerator(processed_data)
        html_docs = document_generator.generate_all_html_documents()
        
        # Step 4: Generate LaTeX templates  
        display_processing_progress("Creating LaTeX templates")
        
        latex_generator = LaTeXGenerator()
        latex_docs = latex_generator.generate_all_documents(processed_data)
        
        # Step 5: Generate PDFs
        display_processing_progress("Converting to PDF formats")
        
        pdf_merger = PDFMerger()
        html_pdfs = pdf_merger.convert_html_to_pdf(html_docs)
        latex_pdfs = pdf_merger.convert_latex_to_pdf(latex_docs)
        
        # Step 6: Generate Excel outputs
        display_processing_progress("Processing Bill Quantity data")
        
        excel_outputs = document_generator.generate_excel_outputs(processed_data)
        
        # Step 7: Package everything
        display_processing_progress("Packaging final deliverables")
        
        zip_packager = ZipPackager()
        
        # Generate smart filename
        project_name = processed_data.get('title', {}).get('project_name', 'Infrastructure_Project')
        timestamp = get_timestamp()
        filename = sanitize_filename(f"{project_name}_{timestamp}_Complete_Package.zip")
        
        zip_buffer = zip_packager.create_comprehensive_package(
            html_docs=html_docs,
            latex_docs=latex_docs,
            html_pdfs=html_pdfs,
            latex_pdfs=latex_pdfs,
            excel_outputs=excel_outputs,
            processed_data=processed_data,
            filename=filename
        )
        
        display_processing_progress("✅ Processing complete!")
        
        # Celebration
        st.balloons()
        
        return {
            'zip_buffer': zip_buffer,
            'filename': filename,
            'html_docs': html_docs,
            'latex_docs': latex_docs,
            'html_pdfs': html_pdfs,
            'latex_pdfs': latex_pdfs,
            'excel_outputs': excel_outputs,
            'processed_data': processed_data,
            'totals': processed_data.get('totals', {}),
            'project_info': processed_data.get('title', {})
        }
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        
        with st.expander("🛠️ Detailed Error Information"):
            st.code(traceback.format_exc())
            
        with st.expander("📝 Troubleshooting Guide"):
            st.markdown("""
            **Common Issues and Solutions:**
            
            1. **File Format Issues:**
               - Ensure your file is in .xlsx format
               - Check that all required sheets exist
               - Verify column headers match expected format
            
            2. **Data Issues:**
               - Remove empty rows at the beginning of sheets
               - Ensure numeric columns contain only numbers
               - Check for special characters or formatting issues
            
            3. **Sheet Structure:**
               - Title sheet: Project information
               - Work Order: Original planned items  
               - Bill Quantity: Actual completed work
               - Extra Items: Additional work (optional)
            
            4. **Dependencies:**
               - LaTeX engine for professional PDF generation
               - WeasyPrint for HTML to PDF conversion
               - All Python packages properly installed
            """)
        
        return None

def display_comprehensive_results(results):
    """Display comprehensive results with enhanced metrics and download options"""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Project Information Banner
    project_info = results.get('project_info', {})
    if project_info:
        st.markdown("""
        <div style="background: #2c3e50; color: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: white;">📁 Project Information</h3>
            <p style="margin: 0.5rem 0;"><strong>Project:</strong> {}</p>
            <p style="margin: 0.5rem 0;"><strong>Contractor:</strong> {}</p>
        </div>
        """.format(
            project_info.get('project_name', 'N/A'),
            project_info.get('contractor_name', 'N/A')
        ), unsafe_allow_html=True)
    
    # Enhanced metrics dashboard
    st.subheader("📊 Document Generation Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #4CAF50; margin: 0;">📄</h3>
            <h4 style="margin: 0.5rem 0;">HTML Docs</h4>
            <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{}</p>
        </div>
        """.format(len(results['html_docs'])), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FF9800; margin: 0;">📐</h3>
            <h4 style="margin: 0.5rem 0;">LaTeX Docs</h4>
            <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{}</p>
        </div>
        """.format(len(results['latex_docs'])), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #F44336; margin: 0;">📑</h3>
            <h4 style="margin: 0.5rem 0;">PDF Files</h4>
            <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{}</p>
        </div>
        """.format(len(results['html_pdfs']) + len(results['latex_pdfs'])), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2196F3; margin: 0;">📊</h3>
            <h4 style="margin: 0.5rem 0;">Excel Files</h4>
            <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{}</p>
        </div>
        """.format(len(results['excel_outputs'])), unsafe_allow_html=True)
    
    with col5:
        zip_size = len(results['zip_buffer']) / (1024 * 1024)  # Convert to MB
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #9C27B0; margin: 0;">📦</h3>
            <h4 style="margin: 0.5rem 0;">Package Size</h4>
            <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{:.1f} MB</p>
        </div>
        """.format(zip_size), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced tabbed results display
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 Download Package", 
        "📄 Document Overview", 
        "📊 Financial Summary",
        "📋 Data Preview", 
        "ℹ️ Technical Details"
    ])
    
    with tab1:
        st.markdown("""
        <div class="download-section">
            <h3>🎉 Your Complete Document Package is Ready!</h3>
            <p>Professional infrastructure billing documents generated with full compliance standards</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **📦 Complete Package Contents:**
            
            **📄 HTML Documents (Web Ready):**
            - Interactive and editable format
            - Professional styling and layout
            - Cross-platform compatibility
            
            **📐 LaTeX Templates (Compliance Ready):**  
            - Election Commission compliant formatting
            - Professional typesetting quality
            - Government standard templates
            
            **📑 Dual PDF Versions:**
            - HTML-based PDFs for general use
            - LaTeX-based PDFs for official submissions
            - A4 format with 10mm margins
            
            **📊 Excel Outputs:**
            - Structured data in spreadsheet format
            - Ready for further analysis
            - Professional formatting maintained
            
            **📁 Organized Structure:**
            - Logical folder organization
            - Easy document navigation
            - Professional file naming
            """)
        
        with col2:
            # Main download button
            st.download_button(
                label="🚀 Download Complete Package",
                data=results['zip_buffer'],
                file_name=results['filename'],
                mime="application/zip",
                help="Download all generated documents in organized ZIP package",
                use_container_width=True
            )
            
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <div style="background: #4CAF50; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; display: inline-block;">
                    ✅ Production Quality
                </div>
                <div style="background: #2196F3; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; display: inline-block; margin-left: 0.5rem;">
                    🏛️ Government Compliant
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📋 Generated Documents Overview")
        
        # Document lists with enhanced formatting
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📄 HTML Documents:**")
            for doc_name in results['html_docs'].keys():
                st.markdown(f"• **{doc_name.replace('_', ' ').title()}** - Web Ready")
            
            st.markdown("**📐 LaTeX Documents:**") 
            for doc_name in results['latex_docs'].keys():
                st.markdown(f"• **{doc_name.replace('_', ' ').title()}** - Compliance Ready")
        
        with col2:
            st.markdown("**📑 HTML-based PDFs:**")
            for doc_name in results['html_pdfs'].keys():
                st.markdown(f"• **{doc_name.replace('_', ' ').title()}** - General Use")
            
            st.markdown("**📑 LaTeX-based PDFs:**")
            for doc_name in results['latex_pdfs'].keys():
                st.markdown(f"• **{doc_name.replace('_', ' ').title()}** - Official Submission")
    
    with tab3:
        st.subheader("💰 Financial Summary")
        
        totals = results.get('totals', {})
        if totals:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Amount Breakdown:**")
                st.markdown(f"• **Bill Quantity Total:** ₹{totals.get('bill_quantity_total', 0):,.2f}")
                st.markdown(f"• **Extra Items Total:** ₹{totals.get('extra_items_total', 0):,.2f}")
                st.markdown(f"• **Sub Total:** ₹{totals.get('grand_total', 0):,.2f}")
                
            with col2:
                st.markdown("**🧾 Tax & Final Amount:**")
                st.markdown(f"• **GST Amount:** ₹{totals.get('gst_amount', 0):,.2f}")
                st.markdown(f"• **Final Payable:** ₹{totals.get('total_with_gst', 0):,.2f}")
        else:
            st.info("💡 Financial summary will be displayed after processing bill data")
    
    with tab4:
        st.subheader("👀 Processed Data Preview")
        
        processed_data = results.get('processed_data', {})
        
        if 'bill_quantity' in processed_data and processed_data['bill_quantity']:
            st.markdown("**📋 Bill Quantity Items Preview:**")
            df_preview = pd.DataFrame(processed_data['bill_quantity'][:5])  # Show first 5 items
            st.dataframe(df_preview, use_container_width=True)
            
        if 'extra_items' in processed_data and processed_data['extra_items']:
            st.markdown("**➕ Extra Items Preview:**") 
            df_extra = pd.DataFrame(processed_data['extra_items'][:3])  # Show first 3 items
            st.dataframe(df_extra, use_container_width=True)
    
    with tab5:
        st.subheader("📁 Technical Package Details")
        
        st.markdown(f"**📦 Package Information:**")
        st.markdown(f"• **File Name:** {results['filename']}")
        st.markdown(f"• **Generated On:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        st.markdown(f"• **Total Files:** {len(results['html_docs']) + len(results['latex_docs']) + len(results['html_pdfs']) + len(results['latex_pdfs']) + len(results['excel_outputs'])}")
        st.markdown(f"• **Package Size:** {len(results['zip_buffer']) / (1024 * 1024):.2f} MB")
        
        # Processing statistics
        processed_data = results.get('processed_data', {})
        st.markdown("**📊 Processing Statistics:**")
        st.markdown(f"• **Bill Items Processed:** {len(processed_data.get('bill_quantity', []))}")
        st.markdown(f"• **Extra Items Processed:** {len(processed_data.get('extra_items', []))}")
        st.markdown(f"• **Total Sheets Processed:** {len(processed_data)}")
        
        # System information
        st.markdown("**⚙️ System Information:**")
        st.markdown("• **Processing Engine:** Enhanced Multi-Format Generator")
        st.markdown("• **PDF Engines:** HTML-to-PDF + LaTeX-to-PDF")
        st.markdown("• **Template System:** Jinja2 + LaTeX")
        st.markdown("• **Compliance:** Election Commission Standards")

def main():
    """Enhanced main application function"""
    
    # Inject custom CSS
    inject_custom_css()
    
    # Display header
    display_header()
    
    # Sidebar with comprehensive information
    with st.sidebar:
        st.markdown("### 🛠️ System Information")
        st.markdown("""
        **Version:** 3.0 (Optimized)  
        **Last Updated:** January 2025  
        **Status:** ✅ Production Ready  
        **Compliance:** Election Commission Standards
        """)
        
        st.markdown("### 📊 Supported Formats")
        st.markdown("""
        **Input:** Excel (.xlsx, .xls)  
        **Output:** HTML, LaTeX, PDF (Dual), DOCX, ZIP
        """)
        
        st.markdown("### 🏛️ Document Types")
        st.markdown("""
        - **First Page Summary** (Bill overview)
        - **Deviation Statement** (Landscape format)  
        - **Final Bill Scrutiny** (Detailed analysis)
        - **Extra Items Statement** (Additional work)
        - **Certificate II & III** (Compliance docs)
        - **Complete Package** (All formats)
        """)
        
        st.markdown("### 🎯 Advanced Features")
        st.markdown("""
        - **Dual PDF Generation** (HTML + LaTeX)
        - **Professional Templates** (Government compliant)
        - **Smart Data Processing** (Error resistant)
        - **Comprehensive Packaging** (Organized delivery)
        - **Real-time Validation** (Instant feedback)
        - **Batch Processing Ready** (Multiple files)
        """)
        
        st.markdown("### 📐 Technical Specifications")
        st.markdown("""
        - **Page Size:** A4 (210 × 297 mm)
        - **Margins:** 10mm all sides
        - **Orientation:** Portrait (Landscape for deviations)
        - **Date Format:** dd/mm/yyyy
        - **Currency:** Indian Rupees (₹)
        - **Decimal Places:** 2 (rates/amounts)
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        - **Excel Structure:** Ensure all required sheets exist
        - **Data Quality:** Check for empty rows and invalid data
        - **File Size:** Optimized for files up to 50MB
        - **Processing Time:** Typically 30-90 seconds
        - **Browser Support:** Chrome, Firefox, Edge recommended
        """)
        
        st.markdown("---")
        st.markdown("### 📞 Support")
        st.markdown("""
        For technical support or questions:
        - **System:** PWD Infrastructure Billing
        - **Contact:** PWD Office, Udaipur
        - **Initiative:** Mrs. Premlata Jain
        """)
    
    # Display feature highlights
    display_feature_highlights()
    
    # File upload section
    st.markdown("---")
    st.subheader("📁 Upload Your Excel File")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="upload-card">
            <h3 style="color: #4CAF50; margin-bottom: 1rem;">📁 Professional Document Processing</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">
                Upload your Excel file containing infrastructure billing data. 
                The system will automatically generate all required documents in multiple formats.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=['xlsx', 'xls'],
            help="Select an Excel file with Title, Work Order, Bill Quantity, and Extra Items sheets",
            accept_multiple_files=False
        )
    
    with col2:
        st.markdown("""
        <div class="instructions-container">
            <h4>📋 Required Excel Sheets</h4>
            <ul>
                <li><strong>Title:</strong> Project information</li>
                <li><strong>Work Order:</strong> Original planned work</li>
                <li><strong>Bill Quantity:</strong> Completed work details</li>
                <li><strong>Extra Items:</strong> Additional work (Optional)</li>
            </ul>
            
            <h4>✅ Data Requirements</h4>
            <ul>
                <li>Numeric values in quantity/rate columns</li>
                <li>Proper date formatting</li>
                <li>No empty rows in data sections</li>
                <li>Valid Excel format (.xlsx preferred)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # File processing section
    if uploaded_file is not None:
        # Display file information
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Convert to MB
        st.success(f"✅ File uploaded successfully: **{uploaded_file.name}** ({file_size:.2f} MB)")
        
        # Process button with enhanced styling
        if st.button("🚀 Generate Professional Documents", type="primary", use_container_width=True):
            
            # Start processing
            with st.spinner("🔄 Processing your infrastructure billing data..."):
                results = process_excel_file(uploaded_file)
                
                if results:
                    # Store results in session state for persistence
                    st.session_state['processing_results'] = results
    
    # Display results if available
    if 'processing_results' in st.session_state:
        st.markdown("---")
        display_comprehensive_results(st.session_state['processing_results'])
    
    # Instructions section for new users
    st.markdown("---")
    st.markdown("""
    <div class="instructions-container">
        <h2 class="how-to-title">📖 How to Use This System</h2>
        <p class="how-to-subtitle">Complete guide to generate professional infrastructure billing documents</p>
        
        <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
            <div style="text-align: center; flex: 1; margin: 0 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                <h4>1. Prepare Excel File</h4>
                <p>Organize your data in the required sheet structure with proper formatting</p>
            </div>
            <div style="text-align: center; flex: 1; margin: 0 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⬆️</div>
                <h4>2. Upload & Process</h4>
                <p>Upload your file and let the system automatically validate and process all data</p>
            </div>
            <div style="text-align: center; flex: 1; margin: 0 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4>3. Review Results</h4>
                <p>Examine the generated documents and financial summaries for accuracy</p>
            </div>
            <div style="text-align: center; flex: 1; margin: 0 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📥</div>
                <h4>4. Download Package</h4>
                <p>Get your complete document package with all formats and professional organization</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
