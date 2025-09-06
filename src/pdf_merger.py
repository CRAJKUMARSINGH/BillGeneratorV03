"""
Enhanced PDF Merger combining features from all versions
Handles both HTML-to-PDF and LaTeX-to-PDF conversion with comprehensive error handling
"""

import os
import tempfile
import subprocess
from typing import Dict, Optional, List
import logging
from io import BytesIO
from pathlib import Path
from datetime import datetime
import streamlit as st

logger = logging.getLogger(__name__)

class PDFMerger:
    """
    Enhanced PDF merger with dual conversion capabilities
    Combines features from V09's PDF merger and V08's weasyprint integration
    """
    
    def __init__(self):
        # Check for available PDF generation tools
        self.weasyprint_available = self._check_weasyprint()
        self.reportlab_available = self._check_reportlab()
        self.latex_available = self._check_latex()
        
        logger.info(f"PDF tools available - WeasyPrint: {self.weasyprint_available}, "
                   f"ReportLab: {self.reportlab_available}, LaTeX: {self.latex_available}")
    
    def _check_weasyprint(self) -> bool:
        """Check if WeasyPrint is available for HTML to PDF conversion"""
        try:
            import weasyprint
            # Test basic functionality
            test_html = "<html><body>Test</body></html>"
            weasyprint.HTML(string=test_html)
            return True
        except ImportError:
            logger.warning("WeasyPrint not available")
            return False
        except Exception as e:
            logger.warning(f"WeasyPrint available but may have issues: {str(e)}")
            return True  # Still try to use it
    
    def _check_reportlab(self) -> bool:
        """Check if ReportLab is available for fallback PDF generation"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            return True
        except ImportError:
            logger.warning("ReportLab not available")
            return False
    
    def _check_latex(self) -> bool:
        """Check if LaTeX is available for LaTeX to PDF conversion"""
        latex_commands = ['pdflatex', 'xelatex', 'lualatex']
        
        for cmd in latex_commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logger.info(f"LaTeX available: {cmd}")
                    self.latex_command = cmd
                    return True
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        logger.warning("LaTeX not available")
        return False
    
    def convert_html_to_pdf(self, html_docs: Dict[str, str]) -> Dict[str, bytes]:
        """
        Convert HTML documents to PDF format with multiple fallback strategies
        
        Args:
            html_docs: Dictionary with document names as keys and HTML content as values
            
        Returns:
            Dictionary with document names as keys and PDF bytes as values
        """
        pdf_docs = {}
        
        if not html_docs:
            logger.warning("No HTML documents provided for conversion")
            return pdf_docs
        
        conversion_stats = {'success': 0, 'failed': 0, 'fallback': 0}
        
        for doc_name, html_content in html_docs.items():
            try:
                logger.info(f"Converting HTML document: {doc_name}")
                pdf_bytes = self._convert_single_html_to_pdf(html_content, doc_name)
                
                if pdf_bytes:
                    pdf_docs[f"{doc_name}_html"] = pdf_bytes
                    conversion_stats['success'] += 1
                    logger.info(f"Successfully converted {doc_name} to PDF")
                else:
                    # Create fallback PDF
                    fallback_pdf = self._create_fallback_pdf(doc_name, "HTML", html_content)
                    if fallback_pdf:
                        pdf_docs[f"{doc_name}_html"] = fallback_pdf
                        conversion_stats['fallback'] += 1
                    else:
                        conversion_stats['failed'] += 1
                        
            except Exception as e:
                logger.error(f"Error converting {doc_name} HTML to PDF: {str(e)}")
                
                # Try fallback
                fallback_pdf = self._create_fallback_pdf(doc_name, "HTML", html_content)
                if fallback_pdf:
                    pdf_docs[f"{doc_name}_html"] = fallback_pdf
                    conversion_stats['fallback'] += 1
                else:
                    conversion_stats['failed'] += 1
        
        # Show conversion summary
        if conversion_stats['success'] > 0:
            st.success(f"✅ Successfully converted {conversion_stats['success']} HTML documents to PDF")
        if conversion_stats['fallback'] > 0:
            st.info(f"ℹ️ Generated {conversion_stats['fallback']} fallback PDFs")
        if conversion_stats['failed'] > 0:
            st.warning(f"⚠️ Failed to convert {conversion_stats['failed']} HTML documents")
        
        logger.info(f"HTML to PDF conversion complete: {len(pdf_docs)} documents generated")
        return pdf_docs
    
    def _convert_single_html_to_pdf(self, html_content: str, doc_name: str) -> Optional[bytes]:
        """Convert single HTML document to PDF using available tools"""
        
        if self.weasyprint_available:
            try:
                import weasyprint
                
                # Enhanced HTML with proper styling for government documents
                enhanced_html = self._enhance_html_for_pdf(html_content)
                
                # Configure WeasyPrint for government document standards
                pdf_bytes = weasyprint.HTML(
                    string=enhanced_html,
                    encoding='utf-8'
                ).write_pdf(
                    stylesheets=[],  # No external stylesheets
                    optimize_images=True,
                    presentational_hints=True
                )
                
                return pdf_bytes
                
            except Exception as e:
                logger.warning(f"WeasyPrint failed for {doc_name}: {str(e)}")
        
        # Fallback: Try alternative HTML to PDF methods
        return self._html_to_pdf_fallback(html_content, doc_name)
    
    def _enhance_html_for_pdf(self, html_content: str) -> str:
        """Enhance HTML content for better PDF conversion"""
        
        # Add comprehensive CSS for government document formatting
        enhanced_css = """
        <style>
        @page {
            size: A4;
            margin: 10mm;
        }
        
        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.4;
            color: #000;
            margin: 0;
            padding: 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1em;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 5pt;
            text-align: left;
            vertical-align: top;
        }
        
        th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2em;
        }
        
        .title {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 0.5em;
        }
        
        .subtitle {
            font-size: 14pt;
            margin-bottom: 0.3em;
        }
        
        .currency {
            text-align: right;
        }
        
        .total-row {
            font-weight: bold;
            background-color: #f9f9f9;
        }
        
        .signature-section {
            margin-top: 3em;
            page-break-inside: avoid;
        }
        </style>
        """
        
        # Insert CSS at the beginning of the HTML
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>{enhanced_css}')
        elif '<html>' in html_content:
            html_content = html_content.replace('<html>', f'<html><head>{enhanced_css}</head>')
        else:
            html_content = f"<html><head>{enhanced_css}</head><body>{html_content}</body></html>"
        
        return html_content
    
    def _html_to_pdf_fallback(self, html_content: str, doc_name: str) -> Optional[bytes]:
        """Fallback HTML to PDF conversion using alternative methods"""
        
        # Try using system wkhtmltopdf if available
        try:
            return self._wkhtmltopdf_convert(html_content, doc_name)
        except Exception as e:
            logger.warning(f"wkhtmltopdf fallback failed: {str(e)}")
        
        # Final fallback: Create basic PDF with ReportLab
        return None
    
    def _wkhtmltopdf_convert(self, html_content: str, doc_name: str) -> Optional[bytes]:
        """Try converting using wkhtmltopdf system command"""
        
        wkhtmltopdf_commands = ['wkhtmltopdf', '/usr/bin/wkhtmltopdf', '/usr/local/bin/wkhtmltopdf']
        
        for cmd in wkhtmltopdf_commands:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    html_file = os.path.join(temp_dir, f"{doc_name}.html")
                    pdf_file = os.path.join(temp_dir, f"{doc_name}.pdf")
                    
                    # Write HTML to file
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Run wkhtmltopdf
                    result = subprocess.run([
                        cmd,
                        '--page-size', 'A4',
                        '--margin-top', '10mm',
                        '--margin-bottom', '10mm',
                        '--margin-left', '10mm',
                        '--margin-right', '10mm',
                        '--encoding', 'UTF-8',
                        html_file,
                        pdf_file
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and os.path.exists(pdf_file):
                        with open(pdf_file, 'rb') as f:
                            return f.read()
                            
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        return None
    
    def convert_latex_to_pdf(self, latex_docs: Dict[str, str]) -> Dict[str, bytes]:
        """
        Convert LaTeX documents to PDF format
        
        Args:
            latex_docs: Dictionary with document names as keys and LaTeX content as values
            
        Returns:
            Dictionary with document names as keys and PDF bytes as values
        """
        pdf_docs = {}
        
        if not latex_docs:
            logger.warning("No LaTeX documents provided for conversion")
            return pdf_docs
        
        if not self.latex_available:
            st.warning("⚠️ LaTeX not available. LaTeX documents will be provided as source files only.")
            # Create placeholder PDFs for LaTeX documents
            for doc_name in latex_docs.keys():
                placeholder_pdf = self._create_fallback_pdf(doc_name, "LaTeX", latex_docs[doc_name])
                if placeholder_pdf:
                    pdf_docs[f"{doc_name}_latex"] = placeholder_pdf
            return pdf_docs
        
        conversion_stats = {'success': 0, 'failed': 0, 'fallback': 0}
        
        for doc_name, latex_content in latex_docs.items():
            try:
                logger.info(f"Converting LaTeX document: {doc_name}")
                pdf_bytes = self._compile_latex_to_pdf(latex_content, doc_name)
                
                if pdf_bytes:
                    pdf_docs[f"{doc_name}_latex"] = pdf_bytes
                    conversion_stats['success'] += 1
                    logger.info(f"Successfully compiled {doc_name} LaTeX to PDF")
                else:
                    # Create fallback PDF
                    fallback_pdf = self._create_fallback_pdf(doc_name, "LaTeX", latex_content)
                    if fallback_pdf:
                        pdf_docs[f"{doc_name}_latex"] = fallback_pdf
                        conversion_stats['fallback'] += 1
                    else:
                        conversion_stats['failed'] += 1
                        
            except Exception as e:
                logger.error(f"Error converting {doc_name} LaTeX to PDF: {str(e)}")
                
                # Try fallback
                fallback_pdf = self._create_fallback_pdf(doc_name, "LaTeX", latex_content)
                if fallback_pdf:
                    pdf_docs[f"{doc_name}_latex"] = fallback_pdf
                    conversion_stats['fallback'] += 1
                else:
                    conversion_stats['failed'] += 1
        
        # Show conversion summary
        if conversion_stats['success'] > 0:
            st.success(f"✅ Successfully compiled {conversion_stats['success']} LaTeX documents to PDF")
        if conversion_stats['fallback'] > 0:
            st.info(f"ℹ️ Generated {conversion_stats['fallback']} fallback PDFs for LaTeX")
        if conversion_stats['failed'] > 0:
            st.warning(f"⚠️ Failed to compile {conversion_stats['failed']} LaTeX documents")
        
        logger.info(f"LaTeX to PDF conversion complete: {len(pdf_docs)} documents generated")
        return pdf_docs
    
    def _compile_latex_to_pdf(self, latex_content: str, doc_name: str) -> Optional[bytes]:
        """Compile LaTeX content to PDF using available LaTeX engine"""
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write LaTeX content to file
                tex_file = temp_path / f"{doc_name}.tex"
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Run LaTeX compilation (twice for proper cross-references)
                for run_num in range(2):
                    try:
                        result = subprocess.run([
                            self.latex_command,
                            '-interaction=nonstopmode',
                            '-output-directory', str(temp_path),
                            str(tex_file)
                        ], capture_output=True, text=True, timeout=60)
                        
                        if result.returncode != 0:
                            if run_num == 0:
                                logger.warning(f"LaTeX compilation warning for {doc_name} (run {run_num + 1})")
                            else:
                                logger.error(f"LaTeX compilation failed for {doc_name}")
                                logger.error(f"LaTeX error output: {result.stdout}")
                                return None
                                
                    except subprocess.TimeoutExpired:
                        logger.error(f"LaTeX compilation timeout for {doc_name}")
                        return None
                
                # Read the generated PDF
                pdf_file = temp_path / f"{doc_name}.pdf"
                if pdf_file.exists():
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                else:
                    logger.error(f"PDF file not generated for {doc_name}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error compiling LaTeX for {doc_name}: {str(e)}")
            return None
    
    def _create_fallback_pdf(self, doc_name: str, format_type: str, content: str = "") -> Optional[bytes]:
        """Create fallback PDF when conversion tools are not available"""
        
        if not self.reportlab_available:
            logger.error("No PDF generation tools available")
            return None
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import mm
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from io import BytesIO
            
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            
            # Set up document
            pdf.setTitle(f"{doc_name} - {format_type} Version")
            
            # Page dimensions
            width, height = A4
            margin = 10 * mm
            
            # Header
            pdf.setFont("Helvetica-Bold", 18)
            text_width = pdf.stringWidth("Infrastructure Billing System", "Helvetica-Bold", 18)
            pdf.drawString((width - text_width) / 2, height - 40*mm, "Infrastructure Billing System")
            
            pdf.setFont("Helvetica-Bold", 14)
            doc_title = f"Document: {doc_name.replace('_', ' ').title()}"
            text_width = pdf.stringWidth(doc_title, "Helvetica-Bold", 14)
            pdf.drawString((width - text_width) / 2, height - 50*mm, doc_title)
            
            pdf.setFont("Helvetica", 12)
            format_text = f"Format: {format_type} to PDF Conversion"
            text_width = pdf.stringWidth(format_text, "Helvetica", 12)
            pdf.drawString((width - text_width) / 2, height - 60*mm, format_text)
            
            # Content area
            y_position = height - 80*mm
            pdf.setFont("Helvetica", 11)
            
            content_lines = [
                f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                "",
                "Document Status:",
                f"• Source Format: {format_type}",
                f"• Target Format: PDF",
                f"• Conversion: Fallback mode",
                "",
                "Note:",
                "This is a fallback PDF generated when full conversion tools",
                "are not available in the current environment.",
                "",
                "In a production environment with proper dependencies:",
                f"• {format_type} documents would be fully converted to PDF",
                "• All formatting and styling would be preserved",
                "• Professional document layout would be maintained",
                "",
                "System Information:",
                f"• WeasyPrint Available: {self.weasyprint_available}",
                f"• LaTeX Available: {self.latex_available}",
                f"• ReportLab Available: {self.reportlab_available}",
            ]
            
            for line in content_lines:
                if line.strip():
                    pdf.drawString(margin, y_position, line)
                y_position -= 15
                
                # Check for page break
                if y_position < margin:
                    pdf.showPage()
                    y_position = height - margin
            
            # Footer
            pdf.setFont("Helvetica-Oblique", 9)
            footer_text = "An Initiative by Mrs. Premlata Jain, Additional Administrative Officer, PWD, Udaipur"
            text_width = pdf.stringWidth(footer_text, "Helvetica-Oblique", 9)
            pdf.drawString((width - text_width) / 2, margin, footer_text)
            
            pdf.save()
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating fallback PDF for {doc_name}: {str(e)}")
            return None
    
    def generate_fallback_pdf(self, content: str, title: str = "Document") -> Optional[bytes]:
        """Public method to generate fallback PDF - alias for _create_fallback_pdf"""
        return self._create_fallback_pdf(title, "Fallback", content)
    
    def merge_pdfs(self, pdf_files: List[bytes]) -> Optional[bytes]:
        """Merge multiple PDF files into one"""
        
        if not pdf_files:
            return None
        
        if len(pdf_files) == 1:
            return pdf_files[0]
        
        try:
            from PyPDF2 import PdfWriter, PdfReader
            
            writer = PdfWriter()
            
            for pdf_bytes in pdf_files:
                reader = PdfReader(BytesIO(pdf_bytes))
                for page in reader.pages:
                    writer.add_page(page)
            
            output = BytesIO()
            writer.write(output)
            output.seek(0)
            return output.getvalue()
            
        except ImportError:
            logger.warning("PyPDF2 not available for PDF merging")
            return pdf_files[0]  # Return first PDF as fallback
        except Exception as e:
            logger.error(f"Error merging PDFs: {str(e)}")
            return pdf_files[0] if pdf_files else None
