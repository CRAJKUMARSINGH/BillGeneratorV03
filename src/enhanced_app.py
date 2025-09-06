"""
Enhanced BillGenerator App with Performance Optimization and Advanced Caching
Integrates comprehensive performance monitoring, caching, and memory optimization
"""

import streamlit as st
import pandas as pd
import os
import hashlib
import zipfile
import tempfile
from datetime import datetime
import traceback
import logging
from typing import List, Dict, Any, Optional
import functools
import time

# Import performance optimization modules
from performance_optimizer import (
    PerformanceOptimizer, 
    performance_optimizer, 
    monitor_performance, 
    optimize_dataframe, 
    cached_operation
)
from enhanced_cache import (
    enhanced_cache, 
    cached_excel_operation, 
    cached_pdf_operation, 
    cached_template_operation
)

# Import existing modules
from excel_processor import ExcelProcessor
from document_generator import DocumentGenerator
from latex_generator import LaTeXGenerator
from pdf_merger import PDFMerger
from zip_packager import ZipPackager
from utils import validate_excel_file, get_timestamp, sanitize_filename

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('billgen_performance.log')
    ]
)
logger = logging.getLogger(__name__)

# Enhanced page configuration with performance settings
st.set_page_config(
    page_title="BillGenerator Optimized - Performance Enhanced",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/crajkumarsingh/BillGenerator',
        'Report a bug': "mailto:crajkumarsingh@hotmail.com",
        'About': "Professional Infrastructure Billing System v2.0 - Performance Enhanced"
    }
)

def inject_enhanced_css():
    """Inject enhanced CSS with performance indicators"""
    st.markdown("""
    <style>
    /* Enhanced main container styling */
    .main > div {
        padding: 1.5rem 1rem;
    }
    
    /* Performance header styling */
    .performance-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4CAF50 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 6px 25px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .performance-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .performance-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Cache status indicators */
    .cache-status {
        background: #e8f5e9;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .cache-hit {
        color: #2e7d32;
        font-weight: 600;
    }
    
    .cache-miss {
        color: #d84315;
        font-weight: 600;
    }
    
    /* Performance metrics dashboard */
    .perf-metric {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #4CAF50;
    }
    
    .perf-metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2e7d32;
        margin: 0;
    }
    
    .perf-metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Enhanced upload area */
    .enhanced-upload {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 3px dashed #4CAF50;
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.4s ease;
        position: relative;
    }
    
    .enhanced-upload:hover {
        border-color: #45a049;
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Processing progress enhancement */
    .processing-container {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 6px solid #ff9800;
        position: relative;
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .progress-step:last-child {
        border-bottom: none;
    }
    
    .step-icon {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 0.8rem;
    }
    
    .step-completed {
        background: #4CAF50;
        color: white;
    }
    
    .step-current {
        background: #ff9800;
        color: white;
        animation: pulse 2s infinite;
    }
    
    .step-pending {
        background: #e0e0e0;
        color: #666;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Results enhancement */
    .results-enhanced {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #4CAF50;
        position: relative;
    }
    
    .success-badge {
        position: absolute;
        top: -10px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

def display_performance_header():
    """Display enhanced header with performance indicators"""
    st.markdown("""
    <div class="performance-header">
        <div style="text-align: center; position: relative; z-index: 1;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
            <div style="font-size: 2.8rem; font-weight: 700; margin-bottom: 0.5rem;">
                BillGenerator Optimized
            </div>
            <div style="font-size: 1.3rem; margin-bottom: 1rem; opacity: 0.9;">
                Performance-Enhanced Infrastructure Billing System v2.0
            </div>
            <div style="font-size: 1rem; color: #e8f5e9; margin-bottom: 1.5rem;">
                Advanced Multi-Format Document Processing with Intelligent Caching
            </div>
            <div>
                <span class="performance-badge">⚡ Performance Optimized</span>
                <span class="performance-badge">🚀 Smart Caching</span>
                <span class="performance-badge">💾 Memory Efficient</span>
                <span class="performance-badge">📊 Real-time Monitoring</span>
                <span class="performance-badge">🏛️ Government Compliant</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_performance_dashboard():
    """Display comprehensive performance dashboard"""
    st.markdown("### ⚡ Performance Dashboard")
    
    # Get performance statistics
    perf_stats = performance_optimizer.get_performance_stats()
    cache_stats = enhanced_cache.get_cache_stats()
    
    # Performance metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-value">{perf_stats['memory_usage_mb']:.1f}</div>
            <div class="perf-metric-label">MB Memory</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-value">{perf_stats['cache_hit_rate']:.1f}%</div>
            <div class="perf-metric-label">Cache Hit Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-value">{perf_stats['system_info']['cpu_percent']:.1f}%</div>
            <div class="perf-metric-label">CPU Usage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        memory_cache_items = cache_stats['memory_cache']['items']
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-value">{memory_cache_items}</div>
            <div class="perf-metric-label">Cached Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        file_cache_items = cache_stats['file_cache']['items']
        st.markdown(f"""
        <div class="perf-metric">
            <div class="perf-metric-value">{file_cache_items}</div>
            <div class="perf-metric-label">File Cache</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed cache statistics
    with st.expander("📊 Detailed Cache Statistics", expanded=False):
        st.json(cache_stats)
    
    # Performance recommendations
    recommendations = perf_stats.get('optimization_recommendations', [])
    if recommendations:
        st.markdown("### 🔧 Performance Recommendations")
        for rec in recommendations:
            st.info(f"💡 {rec}")

@cached_excel_operation(ttl=3600)
@monitor_performance("Excel File Processing")
def process_uploaded_file_enhanced(file_content: bytes, filename: str) -> Optional[Dict]:
    """Enhanced file processing with caching and performance monitoring"""
    try:
        # Create cache key based on file content
        content_hash = hashlib.md5(file_content).hexdigest()
        cache_key = f"excel_processing_{content_hash}_{filename}"
        
        # Check cache first
        cached_result = enhanced_cache.get(cache_key, "excel_processing")
        if cached_result is not None:
            st.success("🚀 Using cached processing results - Lightning fast!")
            return cached_result
        
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        try:
            # Validate file structure
            with performance_optimizer.performance_monitor("File Validation"):
                validation_result = validate_excel_file(tmp_file_path)
                if not validation_result['valid']:
                    return {'error': f"File validation failed: {validation_result['error']}"}
            
            # Process Excel file with enhanced monitoring
            with performance_optimizer.performance_monitor("Excel Processing"):
                excel_processor = ExcelProcessor(tmp_file_path)
                processed_data = excel_processor.process_all_sheets()
                
                if not processed_data:
                    return {'error': "Failed to process Excel file"}
            
            # Generate documents with batch processing
            with performance_optimizer.performance_monitor("Document Generation"):
                document_generator = DocumentGenerator(processed_data)
                
                # Use batch processing for large datasets
                if len(processed_data.get('bill_quantity', [])) > 100:
                    st.info("📊 Large dataset detected - Using optimized batch processing")
                    html_docs = performance_optimizer.batch_process_items(
                        [processed_data],
                        batch_size=50,
                        processor_func=lambda batch: document_generator.generate_all_html_documents()
                    )[0] if processed_data else {}
                else:
                    html_docs = document_generator.generate_all_html_documents()
            
            # Generate LaTeX templates with caching
            with performance_optimizer.performance_monitor("LaTeX Generation"):
                latex_generator = LaTeXGenerator()
                latex_docs = latex_generator.generate_all_documents(processed_data)
            
            # Generate PDFs with optimization
            with performance_optimizer.performance_monitor("PDF Generation"):
                pdf_merger = PDFMerger()
                html_pdfs = pdf_merger.convert_html_to_pdf(html_docs)
                latex_pdfs = pdf_merger.convert_latex_to_pdf(latex_docs)
            
            # Generate Excel outputs
            with performance_optimizer.performance_monitor("Excel Output Generation"):
                excel_outputs = document_generator.generate_excel_outputs(processed_data)
            
            # Package everything
            with performance_optimizer.performance_monitor("ZIP Packaging"):
                zip_packager = ZipPackager()
                
                project_name = processed_data.get('title', {}).get('project_name', 'Infrastructure_Project')
                timestamp = get_timestamp()
                filename_clean = sanitize_filename(f"{project_name}_{timestamp}_Enhanced_Package.zip")
                
                zip_buffer = zip_packager.create_comprehensive_package(
                    html_docs=html_docs,
                    latex_docs=latex_docs,
                    html_pdfs=html_pdfs,
                    latex_pdfs=latex_pdfs,
                    excel_outputs=excel_outputs,
                    processed_data=processed_data,
                    filename=filename_clean
                )
            
            # Prepare result
            result = {
                'zip_buffer': zip_buffer,
                'filename': filename_clean,
                'html_docs': html_docs,
                'latex_docs': latex_docs,
                'html_pdfs': html_pdfs,
                'latex_pdfs': latex_pdfs,
                'excel_outputs': excel_outputs,
                'processed_data': processed_data,
                'totals': processed_data.get('totals', {}),
                'project_info': processed_data.get('title', {}),
                'performance_metrics': {
                    'processing_time': time.time(),
                    'cache_key': cache_key,
                    'optimizations_applied': True
                }
            }
            
            # Cache the result
            enhanced_cache.set(
                cache_key, 
                result, 
                ttl=3600, 
                namespace="excel_processing",
                tags=["excel", "processing", "documents"]
            )
            
            return result
            
        finally:
            # Cleanup temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
                
    except Exception as e:
        logger.error(f"Enhanced processing error: {str(e)}", exc_info=True)
        return {'error': f"Processing error: {str(e)}"}

def display_enhanced_progress(steps_completed: int, total_steps: int, current_step: str):
    """Display enhanced progress with performance metrics"""
    st.markdown(f"""
    <div class="processing-container">
        <h3 style="margin: 0 0 1rem 0; color: #e65100;">⚡ Processing with Performance Optimization</h3>
        <div style="margin-bottom: 1rem;">
            <strong>Current Step:</strong> {current_step}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_percentage = (steps_completed / total_steps) * 100
    progress_bar = st.progress(progress_percentage / 100)
    
    # Performance metrics during processing
    current_memory = performance_optimizer.get_memory_usage()
    st.info(f"💾 Memory Usage: {current_memory:.1f} MB | ⚡ Optimizations Active")
    
    return progress_bar

def display_enhanced_results(results: Dict):
    """Display enhanced results with performance insights"""
    st.markdown('<div class="results-enhanced">', unsafe_allow_html=True)
    st.markdown('<div class="success-badge">✅ Performance Enhanced</div>', unsafe_allow_html=True)
    
    # Performance summary
    perf_metrics = results.get('performance_metrics', {})
    if perf_metrics:
        st.markdown("### ⚡ Performance Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Processing Mode", "🚀 Optimized", delta="Cache Enhanced")
        with col2:
            cache_status = "Hit" if 'cache_key' in perf_metrics else "Miss"
            st.metric("Cache Status", f"📊 {cache_status}", delta="Memory Efficient")
        with col3:
            st.metric("Optimization", "✅ Active", delta="Performance Boost")
    
    # Project information with enhanced styling
    project_info = results.get('project_info', {})
    if project_info:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a237e 0%, #283593 100%); color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
            <h3 style="margin: 0; color: white; display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">🏗️</span>Project Information
            </h3>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div><strong>Project:</strong> {project_info.get('project_name', 'N/A')}</div>
                <div><strong>Contractor:</strong> {project_info.get('contractor_name', 'N/A')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced metrics dashboard
    st.markdown("### 📊 Generation Summary")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics_data = [
        (col1, "📄", "HTML Docs", len(results['html_docs']), "#4CAF50"),
        (col2, "📐", "LaTeX Docs", len(results['latex_docs']), "#FF9800"),
        (col3, "📑", "PDF Files", len(results['html_pdfs']) + len(results['latex_pdfs']), "#F44336"),
        (col4, "📊", "Excel Files", len(results['excel_outputs']), "#2196F3"),
        (col5, "📦", "Package Size", f"{len(results['zip_buffer']) / (1024 * 1024):.1f} MB", "#9C27B0"),
        (col6, "⚡", "Performance", "Enhanced", "#4CAF50")
    ]
    
    for col, icon, label, value, color in metrics_data:
        with col:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 1rem; text-align: center; 
                        box-shadow: 0 3px 15px rgba(0,0,0,0.1); border-left: 4px solid {color};">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 600; color: {color};">{value}</div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.3rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced download section
    st.markdown("### 🚀 Download Enhanced Package")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **🎉 Your Performance-Enhanced Package is Ready!**
        
        **✨ Enhanced Features:**
        - ⚡ **Performance Optimized**: Intelligent caching and memory management
        - 🚀 **Smart Processing**: Batch processing for large datasets
        - 💾 **Memory Efficient**: Optimized DataFrame operations and garbage collection
        - 📊 **Real-time Monitoring**: Performance metrics and optimization insights
        - 🔄 **Intelligent Caching**: Multi-level caching for lightning-fast repeated operations
        
        **📦 Complete Package Contents:**
        - 📄 HTML Documents (Web Ready, Performance Optimized)
        - 📐 LaTeX Templates (Compliance Ready, Cached)
        - 📑 Dual PDF Versions (Enhanced Generation)
        - 📊 Excel Outputs (Memory Optimized)
        - 📁 Organized Structure (Smart Organization)
        """)
    
    with col2:
        st.download_button(
            label="🚀 Download Enhanced Package",
            data=results['zip_buffer'],
            file_name=results['filename'],
            mime="application/zip",
            help="Download your performance-enhanced document package",
            use_container_width=True
        )
        
        # Performance badges
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <div style="background: #4CAF50; color: white; padding: 0.4rem 1rem; 
                       border-radius: 20px; font-size: 0.8rem; margin: 0.2rem; display: inline-block;">
                ⚡ Performance Enhanced
            </div>
            <div style="background: #2196F3; color: white; padding: 0.4rem 1rem; 
                       border-radius: 20px; font-size: 0.8rem; margin: 0.2rem; display: inline-block;">
                🚀 Cache Optimized
            </div>
            <div style="background: #FF9800; color: white; padding: 0.4rem 1rem; 
                       border-radius: 20px; font-size: 0.8rem; margin: 0.2rem; display: inline-block;">
                💾 Memory Efficient
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Enhanced main application with performance optimization"""
    # Inject enhanced CSS
    inject_enhanced_css()
    
    # Display performance header
    display_performance_header()
    
    # Performance dashboard in sidebar
    with st.sidebar:
        st.markdown("### ⚡ Performance Controls")
        
        show_dashboard = st.checkbox("Show Performance Dashboard", value=False)
        if show_dashboard:
            display_performance_dashboard()
        
        # Cache controls
        st.markdown("### 🗄️ Cache Management")
        if st.button("📊 View Cache Stats"):
            cache_stats = enhanced_cache.get_cache_stats()
            st.json(cache_stats)
        
        if st.button("🧹 Clear All Caches"):
            enhanced_cache.cleanup_expired_entries()
            performance_optimizer.optimize_memory()
            st.success("✅ Caches cleared and memory optimized!")
        
        # Memory optimization
        current_memory = performance_optimizer.get_memory_usage()
        st.metric("Memory Usage", f"{current_memory:.1f} MB")
        
        if st.button("🔧 Optimize Memory"):
            freed = performance_optimizer.optimize_memory()
            st.success(f"✅ Freed {freed:.1f} MB of memory!")
    
    # Main application
    st.markdown("### 📁 Upload Your Excel File")
    
    # Enhanced file uploader
    st.markdown("""
    <div class="enhanced-upload">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
            Upload Excel File for Processing
        </div>
        <div style="color: #666; margin-bottom: 1rem;">
            Supports .xlsx files with optimized processing and intelligent caching
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx'],
        help="Upload your infrastructure billing Excel file for enhanced processing"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name} ({len(uploaded_file.getvalue()) / 1024:.1f} KB)")
        
        # Processing button
        if st.button("🚀 Process with Performance Enhancement", type="primary", use_container_width=True):
            # Progress tracking
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with st.spinner("⚡ Processing with performance optimization..."):
                # Enhanced processing
                file_content = uploaded_file.getvalue()
                
                with performance_optimizer.performance_monitor("Complete File Processing"):
                    results = process_uploaded_file_enhanced(file_content, uploaded_file.name)
                
                if results and 'error' not in results:
                    # Success celebration
                    st.balloons()
                    st.success("🎉 Processing completed with performance enhancement!")
                    
                    # Display enhanced results
                    display_enhanced_results(results)
                    
                    # Performance summary
                    final_stats = performance_optimizer.get_performance_stats()
                    st.info(f"⚡ Processing completed using {final_stats['memory_usage_mb']:.1f} MB memory "
                           f"with {final_stats['cache_hit_rate']:.1f}% cache hit rate")
                    
                elif results and 'error' in results:
                    st.error(f"❌ {results['error']}")
                else:
                    st.error("❌ Processing failed. Please check your file format.")
    
    # Instructions and features
    st.markdown("---")
    st.markdown("### 🎯 Enhanced Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **⚡ Performance Optimized**
        - Intelligent memory management
        - Smart caching system
        - Batch processing for large files
        - Real-time performance monitoring
        """)
    
    with col2:
        st.markdown("""
        **🚀 Advanced Processing**
        - Multi-level caching (Memory/File/Redis)
        - DataFrame memory optimization
        - Lazy loading of heavy modules
        - Progress tracking with ETA
        """)
    
    with col3:
        st.markdown("""
        **💾 Memory Efficient**
        - Automatic garbage collection
        - Memory usage monitoring
        - Cache eviction policies
        - Resource cleanup automation
        """)

if __name__ == "__main__":
    main()
