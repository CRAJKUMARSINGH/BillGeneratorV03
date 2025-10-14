"""
ZIP Packager Module for Infrastructure Billing System
Creates comprehensive document packages with proper organization
"""

import os
import zipfile
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from io import BytesIO
import tempfile

try:
    from src.utils import sanitize_filename, get_timestamp
except ImportError:
    try:
        from utils import sanitize_filename, get_timestamp
    except ImportError:
        # Fallback functions
        def sanitize_filename(filename):
            import re
            return re.sub(r'[^\w\-_\.]', '_', filename)
        
        def get_timestamp():
            return datetime.now().strftime('%Y%m%d_%H%M%S')

logger = logging.getLogger(__name__)

class ZipPackager:
    """
    Comprehensive ZIP packager for infrastructure billing documents
    Creates organized packages with proper folder structure
    """
    
    def __init__(self):
        """Initialize ZIP packager"""
        self.base_dir = Path(__file__).parent.parent
        logger.info("ZipPackager initialized")
    
    def create_comprehensive_package(self, 
                                   html_docs: Dict[str, str],
                                   latex_docs: Dict[str, str],
                                   html_pdfs: Dict[str, bytes],
                                   latex_pdfs: Dict[str, bytes],
                                   excel_outputs: Dict[str, bytes],
                                   processed_data: Dict[str, Any],
                                   filename: str = None) -> bytes:
        """
        Create comprehensive document package with all formats
        
        Args:
            html_docs: Dictionary of HTML documents
            latex_docs: Dictionary of LaTeX documents
            html_pdfs: Dictionary of HTML-based PDFs
            latex_pdfs: Dictionary of LaTeX-based PDFs
            excel_outputs: Dictionary of Excel files
            processed_data: Original processed data
            filename: Optional custom filename
            
        Returns:
            ZIP file as bytes
        """
        try:
            # Create ZIP in memory
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add project information file
                self._add_project_info(zip_file, processed_data)
                
                # Add HTML documents
                if html_docs:
                    self._add_html_documents(zip_file, html_docs)
                
                # Add LaTeX documents
                if latex_docs:
                    self._add_latex_documents(zip_file, latex_docs)
                
                # Add HTML-based PDFs
                if html_pdfs:
                    self._add_pdf_documents(zip_file, html_pdfs, "HTML_PDFs")
                
                # Add LaTeX-based PDFs
                if latex_pdfs:
                    self._add_pdf_documents(zip_file, latex_pdfs, "LaTeX_PDFs")
                
                # Add Excel outputs
                if excel_outputs:
                    self._add_excel_documents(zip_file, excel_outputs)
                
                # Add source data (sanitized)
                self._add_source_data(zip_file, processed_data)
                
                # Add readme file
                self._add_readme_file(zip_file, processed_data)
            
            zip_buffer.seek(0)
            zip_bytes = zip_buffer.getvalue()
            
            logger.info(f"Created comprehensive package: {len(zip_bytes) / 1024:.1f} KB")
            return zip_bytes
            
        except Exception as e:
            logger.error(f"Error creating comprehensive package: {str(e)}")
            # Return minimal fallback package
            return self._create_fallback_package(processed_data)
    
    def _add_project_info(self, zip_file: zipfile.ZipFile, processed_data: Dict[str, Any]):
        """Add project information summary"""
        try:
            title_data = processed_data.get('title', {})
            totals = processed_data.get('totals', {})
            
            project_info = f"""# Project Information
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Details
Project Name: {title_data.get('project_name', 'N/A')}
Contractor: {title_data.get('contractor_name', 'N/A')}
Location: {title_data.get('location', 'N/A')}
Agreement No: {title_data.get('agreement_no', 'N/A')}

## Financial Summary
Grand Total: ₹{totals.get('grand_total', 0):,.2f}
GST Amount: ₹{totals.get('gst_amount', 0):,.2f}
Final Amount: ₹{totals.get('total_with_gst', 0):,.2f}

## Document Contents
- HTML Documents: Ready for web viewing and editing
- PDF Documents: Print-ready professional formats
- Excel Files: Data analysis and calculations
- LaTeX Sources: Professional typesetting sources

## Usage Instructions
1. HTML files can be opened in any web browser
2. PDF files are ready for printing and official submission
3. Excel files contain detailed calculations and analysis
4. LaTeX files can be compiled for custom formatting
"""
            
            zip_file.writestr("PROJECT_INFO.md", project_info)
            
        except Exception as e:
            logger.error(f"Error adding project info: {str(e)}")
    
    def _add_html_documents(self, zip_file: zipfile.ZipFile, html_docs: Dict[str, str]):
        """Add HTML documents to ZIP"""
        try:
            for doc_name, html_content in html_docs.items():
                if html_content and len(html_content.strip()) > 100:  # Ensure substantial content
                    filename = f"HTML_Documents/{sanitize_filename(doc_name)}.html"
                    zip_file.writestr(filename, html_content)
                    logger.debug(f"Added HTML document: {filename} ({len(html_content)} chars)")
                else:
                    logger.warning(f"Skipping empty/small HTML document: {doc_name}")
                    
        except Exception as e:
            logger.error(f"Error adding HTML documents: {str(e)}")
    
    def _add_latex_documents(self, zip_file: zipfile.ZipFile, latex_docs: Dict[str, str]):
        """Add LaTeX documents to ZIP"""
        try:
            for doc_name, latex_content in latex_docs.items():
                if latex_content and len(latex_content.strip()) > 100:  # Ensure substantial content
                    filename = f"LaTeX_Sources/{sanitize_filename(doc_name)}.tex"
                    zip_file.writestr(filename, latex_content)
                    logger.debug(f"Added LaTeX document: {filename} ({len(latex_content)} chars)")
                else:
                    logger.warning(f"Skipping empty/small LaTeX document: {doc_name}")
                    
        except Exception as e:
            logger.error(f"Error adding LaTeX documents: {str(e)}")
    
    def _add_pdf_documents(self, zip_file: zipfile.ZipFile, pdf_docs: Dict[str, bytes], folder_name: str):
        """Add PDF documents to ZIP"""
        try:
            for doc_name, pdf_bytes in pdf_docs.items():
                if pdf_bytes and len(pdf_bytes) > 1000:  # Ensure substantial PDF content
                    filename = f"{folder_name}/{sanitize_filename(doc_name)}.pdf"
                    zip_file.writestr(filename, pdf_bytes)
                    logger.debug(f"Added PDF document: {filename} ({len(pdf_bytes)} bytes)")
                else:
                    logger.warning(f"Skipping empty/small PDF document: {doc_name}")
                    
        except Exception as e:
            logger.error(f"Error adding PDF documents to {folder_name}: {str(e)}")
    
    def _add_excel_documents(self, zip_file: zipfile.ZipFile, excel_docs: Dict[str, bytes]):
        """Add Excel documents to ZIP"""
        try:
            for doc_name, excel_bytes in excel_docs.items():
                if excel_bytes and len(excel_bytes) > 1000:  # Ensure substantial content
                    filename = f"Excel_Analysis/{sanitize_filename(doc_name)}.xlsx"
                    zip_file.writestr(filename, excel_bytes)
                    logger.debug(f"Added Excel document: {filename} ({len(excel_bytes)} bytes)")
                else:
                    logger.warning(f"Skipping empty/small Excel document: {doc_name}")
                    
        except Exception as e:
            logger.error(f"Error adding Excel documents: {str(e)}")
    
    def _add_source_data(self, zip_file: zipfile.ZipFile, processed_data: Dict[str, Any]):
        """Add sanitized source data for reference"""
        try:
            import json
            
            # Create sanitized version of processed data
            sanitized_data = {
                'title': processed_data.get('title', {}),
                'totals': processed_data.get('totals', {}),
                'processing_timestamp': datetime.now().isoformat(),
                'data_summary': {
                    'work_order_items': len(processed_data.get('work_order', [])),
                    'bill_quantity_items': len(processed_data.get('bill_quantity', [])),
                    'extra_items': len(processed_data.get('extra_items', [])),
                    'has_financial_totals': bool(processed_data.get('totals'))
                }
            }
            
            # Add as JSON file
            json_content = json.dumps(sanitized_data, indent=2, ensure_ascii=False)
            zip_file.writestr("Source_Data/processing_summary.json", json_content)
            
        except Exception as e:
            logger.error(f"Error adding source data: {str(e)}")
    
    def _add_readme_file(self, zip_file: zipfile.ZipFile, processed_data: Dict[str, Any]):
        """Add comprehensive README file"""
        try:
            title_data = processed_data.get('title', {})
            
            readme_content = f"""# Infrastructure Billing Document Package

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project: {title_data.get('project_name', 'Infrastructure Project')}

## Package Contents

### 📄 HTML_Documents/
Web-ready HTML documents that can be opened in any browser:
- first_page_summary.html - Bill summary and overview
- deviation_statement.html - Work order vs executed comparison
- extra_items_statement.html - Additional work items (if applicable)
- certificate_ii.html - Measurement certificate
- certificate_iii.html - Compliance certificate
- note_sheet.html - Financial summary and notes

### 📑 HTML_PDFs/
PDF versions generated from HTML templates:
- Optimized for general viewing and sharing
- Professional formatting with proper margins
- Suitable for email attachments and digital distribution

### 📐 LaTeX_PDFs/
PDF versions generated from LaTeX sources:
- Government compliant formatting
- Professional typesetting quality
- Recommended for official submissions

### 📊 Excel_Analysis/
Spreadsheet files for detailed analysis:
- bill_summary.xlsx - Project and financial summary
- detailed_analysis.xlsx - Comprehensive comparison and analysis

### 📝 LaTeX_Sources/
LaTeX source files for custom formatting:
- Can be modified and recompiled as needed
- Professional document preparation system
- Maintains government compliance standards

### 📁 Source_Data/
Processing metadata and summary information:
- processing_summary.json - Data processing details

## Usage Instructions

### For General Use:
1. Open HTML documents in any web browser
2. Use HTML PDFs for sharing and basic printing

### For Official Submissions:
1. Use LaTeX PDFs for government submissions
2. Ensure all compliance requirements are met
3. Verify signatures and authorizations

### For Analysis:
1. Open Excel files for detailed calculations
2. Use data for further analysis and reporting

### For Custom Formatting:
1. Modify LaTeX sources as needed
2. Recompile using LaTeX system (pdflatex recommended)

## System Information

- Generated by: Infrastructure Billing System v3.0
- Compliance: Election Commission Standards
- Format Standards: A4 paper, 10mm margins
- Date Format: dd/mm/yyyy
- Currency: Indian Rupees (₹)

## Support

For technical support or questions:
- Developer: Rajkumar Singh
- Organization: PWD, Udaipur
- System: Infrastructure Billing Generator

---

**Important:** Verify all calculations and amounts before official submission.
"""
            
            zip_file.writestr("README.md", readme_content)
            
        except Exception as e:
            logger.error(f"Error adding README file: {str(e)}")
    
    def _create_fallback_package(self, processed_data: Dict[str, Any]) -> bytes:
        """Create minimal fallback package when main packaging fails"""
        try:
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add minimal project info
                title_data = processed_data.get('title', {})
                
                minimal_info = f"""# Infrastructure Billing - Minimal Package

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Information
Project: {title_data.get('project_name', 'N/A')}
Contractor: {title_data.get('contractor_name', 'N/A')}

## Status
This is a minimal package generated due to processing limitations.
Please contact support for assistance with full document generation.

## Available Data
- Title Data: {'✓' if processed_data.get('title') else '✗'}
- Work Order: {'✓' if processed_data.get('work_order') else '✗'}
- Bill Quantity: {'✓' if processed_data.get('bill_quantity') else '✗'}
- Extra Items: {'✓' if processed_data.get('extra_items') else '✗'}
- Financial Totals: {'✓' if processed_data.get('totals') else '✗'}

For full functionality, please ensure all required modules are properly installed.
"""
                
                zip_file.writestr("MINIMAL_PACKAGE_INFO.md", minimal_info)
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating fallback package: {str(e)}")
            # Return empty ZIP as last resort
            return b''
    
    def create_simple_package(self, content_dict: Dict[str, Any], package_name: str = None) -> bytes:
        """Create simple package from content dictionary"""
        try:
            if not package_name:
                package_name = f"bill_package_{get_timestamp()}"
            
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for filename, content in content_dict.items():
                    if isinstance(content, str):
                        zip_file.writestr(filename, content)
                    elif isinstance(content, bytes):
                        zip_file.writestr(filename, content)
                    else:
                        # Convert to string
                        zip_file.writestr(filename, str(content))
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating simple package: {str(e)}")
            return b''
    
    def extract_package_info(self, zip_bytes: bytes) -> Dict[str, Any]:
        """Extract information about package contents"""
        try:
            info = {
                'total_size_bytes': len(zip_bytes),
                'total_size_mb': len(zip_bytes) / (1024 * 1024),
                'files': [],
                'folders': set(),
                'file_types': {},
                'created': datetime.now().isoformat()
            }
            
            with zipfile.ZipFile(BytesIO(zip_bytes), 'r') as zip_file:
                for file_info in zip_file.filelist:
                    filename = file_info.filename
                    
                    # Track files
                    info['files'].append({
                        'name': filename,
                        'size_bytes': file_info.file_size,
                        'compressed_size': file_info.compress_size,
                        'compression_ratio': 1 - (file_info.compress_size / max(file_info.file_size, 1))
                    })
                    
                    # Track folders
                    if '/' in filename:
                        folder = filename.split('/')[0]
                        info['folders'].add(folder)
                    
                    # Track file types
                    if '.' in filename:
                        ext = filename.split('.')[-1].lower()
                        info['file_types'][ext] = info['file_types'].get(ext, 0) + 1
            
            info['folders'] = list(info['folders'])
            info['total_files'] = len(info['files'])
            
            return info
            
        except Exception as e:
            logger.error(f"Error extracting package info: {str(e)}")
            return {'error': str(e), 'total_size_bytes': len(zip_bytes)}