"""
Enhanced LaTeX Generator combining features from all versions
Handles professional LaTeX template processing and PDF compilation
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from jinja2 import Environment, BaseLoader, DictLoader
try:
    from src.utils import format_currency, format_date, clean_text, get_timestamp
except ImportError:
    try:
        from utils import format_currency, format_date, clean_text, get_timestamp
    except ImportError:
        # Fallback functions if utils module is not available
        def format_currency(amount):
            return f"₹{amount:,.2f}"
        
        def format_date(date_obj):
            if isinstance(date_obj, str):
                return date_obj
            return date_obj.strftime('%d/%m/%Y') if date_obj else ""
        
        def clean_text(text):
            return str(text).strip() if text is not None else ""
        
        def get_timestamp():
            return datetime.now().strftime('%Y%m%d_%H%M%S')

logger = logging.getLogger(__name__)

class LaTeXGenerator:
    """Enhanced LaTeX generator with comprehensive template support"""
    
    def __init__(self):
        self.template_dir = Path("templates/latex")
        self.setup_template_environment()
        
        # Check if LaTeX is available
        self._check_latex_availability()
        
        # Built-in templates for different document types
        self.builtin_templates = self._load_builtin_templates()
    
    def setup_template_environment(self):
        """Setup Jinja2 environment for LaTeX templates"""
        # Ensure template directory exists
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 with LaTeX-specific settings
        self.jinja_env = Environment(
            loader=DictLoader({}),  # Will be populated with templates
            block_start_string='\\BLOCK{',
            block_end_string='}',
            variable_start_string='\\VAR{',
            variable_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False
        )
        
        # Add custom filters
        self.jinja_env.filters['currency'] = self._format_currency_latex
        self.jinja_env.filters['date'] = format_date
        self.jinja_env.filters['escape_latex'] = self._latex_escape
        self.jinja_env.filters['clean'] = clean_text
    
    def setup_jinja_environment(self):
        """Alias for setup_template_environment for backward compatibility"""
        return self.jinja_env
    
    def _check_latex_availability(self):
        """Check if LaTeX (pdflatex/xelatex) is available"""
        self.latex_available = False
        self.latex_command = None
        
        commands_to_test = ['pdflatex', 'xelatex', 'lualatex']
        
        for cmd in commands_to_test:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.latex_available = True
                    self.latex_command = cmd
                    logger.info(f"LaTeX available: {cmd}")
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        if not self.latex_available:
            logger.warning("LaTeX engine not found. LaTeX documents will be generated but not compiled to PDF")
    
    def _load_builtin_templates(self) -> Dict[str, str]:
        """Load built-in LaTeX templates for different document types"""
        return {
            'first_page_summary': self._get_first_page_template(),
            'deviation_statement': self._get_deviation_template(),
            'bill_scrutiny': self._get_bill_scrutiny_template(),
            'extra_items_statement': self._get_extra_items_template(),
            'certificate_ii': self._get_certificate_ii_template(),
            'certificate_iii': self._get_certificate_iii_template(),
            'note_sheet': self._get_note_sheet_template()
        }
    
    def _get_first_page_template(self) -> str:
        """First page summary LaTeX template with government formatting"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{amsmath}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{FIRST PAGE SUMMARY}\\[0.5cm]
    
\end{center}

\vspace{1cm}

% Project Information
\begin{tabular}{|l|p{10cm}|}
\hline
\textbf{Project Name} & \VAR{title.project_name|escape_latex} \\
\hline
\textbf{Contractor} & \VAR{title.contractor_name|escape_latex} \\
\hline
\textbf{Agreement No.} & \VAR{title.agreement_no|escape_latex} \\
\hline
\textbf{Work Order No.} & \VAR{title.work_order_no|escape_latex} \\
\hline
\end{tabular}

\vspace{1cm}

% Bill Summary Table
\begin{longtable}{|p{1.5cm}|p{7cm}|p{2cm}|p{2cm}|p{2.5cm}|}
\hline
\textbf{S.No.} & \textbf{Item of Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Amount (Rs.)} \\
\hline
\endfirsthead

\hline
\textbf{S.No.} & \textbf{Item of Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Amount (Rs.)} \\
\hline
\endhead

\BLOCK{for item in bill_quantity}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.quantity} & \VAR{item.amount|currency} \\
\hline
\BLOCK{endfor}

\BLOCK{if extra_items}
\multicolumn{5}{|c|}{\textbf{Extra Items}} \\
\hline
\BLOCK{for item in extra_items}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.quantity} & \VAR{item.amount|currency} \\
\hline
\BLOCK{endfor}
\BLOCK{endif}

\hline
\multicolumn{4}{|r|}{\textbf{Total Amount:}} & \textbf{\VAR{totals.grand_total|currency}} \\
\hline
\multicolumn{4}{|r|}{\textbf{GST @ \VAR{totals.gst_rate}\%:}} & \textbf{\VAR{totals.gst_amount|currency}} \\
\hline
\multicolumn{4}{|r|}{\textbf{Final Amount:}} & \textbf{\VAR{totals.total_with_gst|currency}} \\
\hline

\end{longtable}

\vspace{1cm}

\begin{center}
}\\

\end{center}

\end{document}
"""
    
    def _get_deviation_template(self) -> str:
        """Deviation statement LaTeX template with landscape format"""
        return r"""
\documentclass[a4paper,10pt,landscape]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{longtable}
\usepackage{array}
\usepackage{booktabs}
\usepackage{fontspec}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{DEVIATION STATEMENT}\\[0.5cm]
    \large\textbf{Comparison of Work Order vs. Executed Quantities}\\[0.3cm]
\end{center}

\vspace{0.5cm}

% Project Details
Project: \VAR{title.project_name|escape_latex}\\
Contractor: \VAR{title.contractor_name|escape_latex}

\vspace{1cm}

% Deviation Table
\begin{longtable}{|p{1cm}|p{6cm}|p{1.5cm}|p{2cm}|p{2cm}|p{2.5cm}|p{2cm}|p{2.5cm}|p{2cm}|p{2.5cm}|}
\hline
\textbf{Item No.} & \textbf{Description} & \textbf{Unit} & \textbf{WO Qty} & \textbf{Rate} & \textbf{WO Amount} & \textbf{Exec Qty} & \textbf{Exec Amount} & \textbf{Dev Qty} & \textbf{Remarks} \\
\hline
\endfirsthead

\hline
\textbf{Item No.} & \textbf{Description} & \textbf{Unit} & \textbf{WO Qty} & \textbf{Rate} & \textbf{WO Amount} & \textbf{Exec Qty} & \textbf{Exec Amount} & \textbf{Dev Qty} & \textbf{Remarks} \\
\hline
\endhead

\BLOCK{for item in bill_quantity}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.wo_quantity|default(0)} & \VAR{item.rate|currency} & \VAR{(item.wo_quantity|default(0) * item.rate)|currency} & \VAR{item.quantity} & \VAR{item.amount|currency} & \VAR{(item.quantity - item.wo_quantity|default(0))} & \VAR{item.remark|escape_latex} \\
\hline
\BLOCK{endfor}

\end{longtable}

\vspace{1cm}

\begin{center}
}
\end{center}

\end{document}
"""

    def _get_bill_scrutiny_template(self) -> str:
        """Bill scrutiny sheet template"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{longtable}
\usepackage{array}
\usepackage{booktabs}
\usepackage{fontspec}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{FINAL BILL SCRUTINY SHEET}\\[0.5cm]
    \large\textbf{Detailed Analysis of Work Executed}\\[0.3cm]
\end{center}

\vspace{1cm}

% Project Information
\textbf{Project:} \VAR{title.project_name|escape_latex}\\
\textbf{Contractor:} \VAR{title.contractor_name|escape_latex}\\
\textbf{Bill Period:} \VAR{bill_period|default('Current')}\\
\textbf{Date:} \VAR{current_date|date}

\vspace{1cm}

% Detailed Bill Items
\begin{longtable}{|p{1cm}|p{8cm}|p{1.5cm}|p{2cm}|p{2cm}|p{2.5cm}|}
\hline
\textbf{S.No.} & \textbf{Description of Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Rate (Rs.)} & \textbf{Amount (Rs.)} \\
\hline
\endfirsthead

\hline
\textbf{S.No.} & \textbf{Description of Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Rate (Rs.)} & \textbf{Amount (Rs.)} \\
\hline
\endhead

\BLOCK{for item in bill_quantity}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.quantity} & \VAR{item.rate} & \VAR{item.amount|currency} \\
\hline
\BLOCK{endfor}

\hline
\multicolumn{5}{|r|}{\textbf{Sub Total:}} & \textbf{\VAR{totals.bill_quantity_total|currency}} \\
\hline

\BLOCK{if extra_items}
\multicolumn{6}{|c|}{\textbf{EXTRA ITEMS}} \\
\hline
\BLOCK{for item in extra_items}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.quantity} & \VAR{item.rate} & \VAR{item.amount|currency} \\
\hline
\BLOCK{endfor}

\hline
\multicolumn{5}{|r|}{\textbf{Extra Items Total:}} & \textbf{\VAR{totals.extra_items_total|currency}} \\
\hline
\BLOCK{endif}

\multicolumn{5}{|r|}{\textbf{Grand Total:}} & \textbf{\VAR{totals.grand_total|currency}} \\
\hline
\multicolumn{5}{|r|}{\textbf{GST @ \VAR{totals.gst_rate}\%:}} & \textbf{\VAR{totals.gst_amount|currency}} \\
\hline
\multicolumn{5}{|r|}{\textbf{Final Payable Amount:}} & \textbf{\VAR{totals.total_with_gst|currency}} \\
\hline

\end{longtable}

\vspace{1cm}

\textbf{Certification:}\\
I certify that the work described above has been executed as per specifications and is acceptable for payment.

\vspace{2cm}

\begin{tabular}{p{6cm}p{6cm}}
Signature of Executive Engineer & Signature of Contractor \\
& \\
Date: \underline{\hspace{3cm}} & Date: \underline{\hspace{3cm}} \\
\end{tabular}

\end{document}
"""

    def _get_extra_items_template(self) -> str:
        """Extra items statement template"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{longtable}
\usepackage{array}
\usepackage{booktabs}
\usepackage{fontspec}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{EXTRA ITEMS STATEMENT}\\[0.5cm]
    \large\textbf{Additional Work Authorization \& Execution}\\[0.3cm]
\end{center}

\vspace{1cm}

% Project Information
\textbf{Project:} \VAR{title.project_name|escape_latex}\\
\textbf{Contractor:} \VAR{title.contractor_name|escape_latex}\\
\textbf{Date:} \VAR{current_date|date}

\vspace{1cm}

\BLOCK{if extra_items}
\begin{longtable}{|p{1cm}|p{7cm}|p{1.5cm}|p{2cm}|p{2cm}|p{2.5cm}|}
\hline
\textbf{S.No.} & \textbf{Description of Extra Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Rate (Rs.)} & \textbf{Amount (Rs.)} \\
\hline
\endfirsthead

\hline
\textbf{S.No.} & \textbf{Description of Extra Work} & \textbf{Unit} & \textbf{Quantity} & \textbf{Rate (Rs.)} & \textbf{Amount (Rs.)} \\
\hline
\endhead

\BLOCK{for item in extra_items}
\VAR{item.serial_no} & \VAR{item.description|escape_latex} & \VAR{item.unit|escape_latex} & \VAR{item.quantity} & \VAR{item.rate} & \VAR{item.amount|currency} \\
\hline
\BLOCK{endfor}

\hline
\multicolumn{5}{|r|}{\textbf{Total Extra Items Amount:}} & \textbf{\VAR{totals.extra_items_total|currency}} \\
\hline

\end{longtable}

\vspace{1cm}

\textbf{Authorization Details:}\\
All extra items listed above have been duly authorized by competent authority and executed as per approved specifications.

\vspace{2cm}

\textbf{Approving Authority Signature:} \underline{\hspace{5cm}}\\
\textbf{Date:} \underline{\hspace{3cm}}

\BLOCK{else}
\begin{center}
\Large\textit{No Extra Items in this Bill}
\end{center}
\BLOCK{endif}

\end{document}
"""

    def _get_certificate_ii_template(self) -> str:
        """Certificate II template"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{fontspec}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{CERTIFICATE - II}\\[0.5cm]
    \large\textbf{Work Completion \& Quality Certification}\\[0.3cm]
\end{center}

\vspace{2cm}

\textbf{Project:} \VAR{title.project_name|escape_latex}\\
\textbf{Contractor:} \VAR{title.contractor_name|escape_latex}\\
\textbf{Agreement No.:} \VAR{title.agreement_no|escape_latex}\\
\textbf{Date:} \VAR{current_date|date}

\vspace{2cm}

I hereby certify that:

\begin{enumerate}
    \item The work described in the attached bill has been completed satisfactorily.
    \item The work has been executed as per approved drawings, specifications, and contract conditions.
    \item The quantities claimed are correct and have been verified by measurement.
    \item The rates applied are as per the contract agreement.
    \item All materials used are of approved quality and conform to specifications.
    \item The work is acceptable for payment.
\end{enumerate}

\vspace{3cm}

\textbf{Total Bill Amount:} \VAR{totals.total_with_gst|currency}\\
\textbf{Amount in Words:} \VAR{totals.total_with_gst|currency} Only

\vspace{3cm}

\begin{tabular}{p{8cm}p{6cm}}
& \\
& Signature of Executive Engineer \\
& \\
& Name: \underline{\hspace{4cm}} \\
& \\
& Date: \underline{\hspace{3cm}} \\
& \\
& Seal: \\
\end{tabular}

\end{document}
"""

    def _get_certificate_iii_template(self) -> str:
        """Certificate III template"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{fontspec}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{CERTIFICATE - III}\\[0.5cm]
    \large\textbf{Payment Authorization Certificate}\\[0.3cm]
\end{center}

\vspace{2cm}

\textbf{Project:} \VAR{title.project_name|escape_latex}\\
\textbf{Contractor:} \VAR{title.contractor_name|escape_latex}\\
\textbf{Bill No.:} \VAR{bill_number|default('Current')}\\
\textbf{Date:} \VAR{current_date|date}

\vspace{2cm}

I hereby certify and authorize the payment of \textbf{\VAR{totals.total_with_gst|currency}} to the above-mentioned contractor for the work satisfactorily completed as detailed in the attached bill.

\vspace{1cm}

\textbf{Payment Details:}
\begin{itemize}
    \item Gross Amount: \VAR{totals.grand_total|currency}
    \item GST @ \VAR{totals.gst_rate}\%: \VAR{totals.gst_amount|currency}
    \item Net Payable: \VAR{totals.total_with_gst|currency}
\end{itemize}

\vspace{2cm}

\textbf{Recovery Details (if any):}\\
TDS: As applicable\\
Performance Guarantee: As per contract\\
Other Recoveries: As applicable

\vspace{3cm}

\begin{tabular}{p{8cm}p{6cm}}
& \\
& Signature of Divisional Engineer \\
& \\
& Name: \underline{\hspace{4cm}} \\
& \\
& Date: \underline{\hspace{3cm}} \\
& \\
& Office Seal: \\
\end{tabular}

\end{document}
"""

    def _get_note_sheet_template(self) -> str:
        """Note sheet LaTeX template with government formatting"""
        return r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=10mm]{geometry}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{amsmath}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}

\setmainfont{Times New Roman}

\begin{document}

\begin{center}
    \Large\textbf{FINAL BILL SCRUTINY SHEET}\\[0.5cm]
\end{center}

\vspace{1cm}

% Project Information Table
\begin{tabularx}{\textwidth}{|l|X|}
\hline
\textbf{Chargeable Head} & 8443-00-108-00-00 \\
\hline
\textbf{Agreement No.} & \VAR{title.agreement_no|escape_latex} \\
\hline
\textbf{Adm. Section} & Udaipur Electrical Division \\
\hline
\textbf{Tech. Section} & Ambamata Sub-Division \\
\hline
\textbf{MB No.} & 887/Pg. No. 04-20 \\
\hline
\textbf{Name of Sub Dn} & Ambamata Sub-Division \\
\hline
\textbf{Name of Work} & \VAR{title.project_name|escape_latex} \\
\hline
\textbf{Name of Firm} & \VAR{title.contractor_name|escape_latex} \\
\hline
\textbf{Original/Deposit} & Deposit \\
\hline
\textbf{Date of Commencement} & \VAR{title.start_date|date} \\
\hline
\textbf{Date of Completion} & \VAR{title.completion_date|date} \\
\hline
\textbf{Actual Date of Completion} & \VAR{title.completion_date|date} \\
\hline
\textbf{In case of delay weather, Provisional Extension Granted} & Work completed within stipulated time \\
\hline
\textbf{Whether any notice issued} & No \\
\hline
\textbf{Amount of Work Order Rs.} & \VAR{totals.grand_total|currency} \\
\hline
\textbf{Actual Expenditure up to this Bill Rs.} & \VAR{totals.grand_total|currency} \\
\hline
\textbf{Balance to be done Rs.} & NIL \\
\hline
\textbf{Net Amount of This Bill Rs.} & \VAR{totals.net_payable|currency} \\
\hline
\textbf{Prorata Progress on the Work maintained by the Firm} & Till date 100\% Work is executed \\
\hline
\textbf{Date on Which record Measurement taken by JEN AC} & \VAR{title.measurement_date|date if title.measurement_date else 'N/A'} \\
\hline
\textbf{Date of Checking and \% on the Checked By AEN} & 100\% checked \\
\hline
\textbf{No. Of selection item checked by the EE} & All items checked \\
\hline
\textbf{Other Inputs} &  \\
\hline
\textbf{(A) Is It a Repair / Maintenance Work} & No \\
\hline
\textbf{(B) Extra Item} & \VAR{'Yes' if extra_items and extra_items|length > 0 else 'No'} \\
\hline
\textbf{Amount of Extra Items Rs.} & \VAR{totals.extra_items_total|currency if totals.extra_items_total > 0 else ''} \\
\hline
\textbf{(C) Any Excess Item Executed?} & No \\
\hline
\textbf{(D) Any Inadvertent Delay in Bill Submission?} & No \\
\hline
\end{tabularx}

\vspace{1cm}

% Deductions Table
\begin{tabularx}{\textwidth}{|l|X|}
\hline
\textbf{Deductions:-} &  \\
\hline
\textbf{S.D.II} & \VAR{totals.sd_amount|currency if totals.sd_amount else '0'} \\
\hline
\textbf{I.T.} & \VAR{totals.it_amount|currency if totals.it_amount else '0'} \\
\hline
\textbf{GST} & \VAR{totals.gst_amount|currency if totals.gst_amount else '0'} \\
\hline
\textbf{L.C.} & \VAR{totals.lc_amount|currency if totals.lc_amount else '0'} \\
\hline
\textbf{Liquidated Damages (Recovery)} & NIL \\
\hline
\textbf{Cheque} & \VAR{totals.net_payable|currency if totals.net_payable else '0'} \\
\hline
\textbf{Total} & \VAR{totals.grand_total|currency if totals.grand_total else '0'} \\
\hline
\end{tabularx}

\vspace{1cm}

% Notes Section
\begin{center}
\textbf{Notes:}
\end{center}

\begin{verbatim}
\VAR{note_sheet_content|escape_latex}
\end{verbatim}

\vspace{2cm}

\begin{center}
                                Premlata Jain\\
                               AAO- As Auditor
\end{center}

\end{document}
"""

    def _format_currency_latex(self, amount):
        """Format currency for LaTeX output"""
        if amount == 0:
            return "0.00"
        return f"{amount:,.2f}".replace(",", "\\,")
    
    def _latex_escape(self, text):
        """Escape special LaTeX characters"""
        if not isinstance(text, str):
            text = str(text)
        
        escape_map = {
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '\\': '\\textbackslash{}'
        }
        
        for char, escaped in escape_map.items():
            text = text.replace(char, escaped)
        
        return text
    
    def generate_all_documents(self, processed_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all LaTeX documents"""
        try:
            latex_docs = {}
            
            # Prepare template context
            context = self._prepare_template_context(processed_data)
            
            # Generate each document type
            for doc_type, template_content in self.builtin_templates.items():
                try:
                    template = self.jinja_env.from_string(template_content)
                    latex_content = template.render(context)
                    latex_docs[doc_type] = latex_content
                    logger.info(f"Generated LaTeX document: {doc_type}")
                except Exception as e:
                    logger.error(f"Error generating {doc_type}: {str(e)}")
                    # Create fallback content
                    latex_docs[doc_type] = self._create_fallback_document(doc_type, context)
            
            logger.info(f"Generated {len(latex_docs)} LaTeX documents")
            return latex_docs
            
        except Exception as e:
            logger.error(f"Error generating LaTeX documents: {str(e)}")
            return {}
    
    def _prepare_template_context(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template context with all required data"""
        context = {
            'current_date': datetime.now(),
            'timestamp': get_timestamp(),
            'bill_number': f"BILL_{get_timestamp()}",
            'bill_period': datetime.now().strftime("%B %Y")
        }
        
        # Add processed data
        context.update(processed_data)
        
        # Ensure all required sections exist with defaults
        context.setdefault('title', {})
        context.setdefault('work_order', [])
        context.setdefault('bill_quantity', [])
        context.setdefault('extra_items', [])
        context.setdefault('totals', {})
        
        return context
    
    def _create_fallback_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        """Create fallback LaTeX document when template fails"""
        title = doc_type.replace('_', ' ').title()
        
        return f"""
\\documentclass[a4paper,10pt]{{article}}
\\usepackage[margin=10mm]{{geometry}}
\\usepackage{{fontspec}}

\\setmainfont{{Times New Roman}}

\\begin{{document}}

\\begin{{center}}
    \\Large\\textbf{{{title}}}\\\\[0.5cm]
    \\large\\textbf{{Infrastructure Billing System}}\\\\[0.3cm]
\\end{{center}}

\\vspace{{2cm}}

This document could not be generated due to template processing error.\\\\
Document type: {doc_type}\\\\
Generated on: {context.get('current_date', datetime.now())}

\\vspace{{2cm}}

Please contact system administrator for assistance.

\\end{{document}}
"""

    def compile_latex_to_pdf(self, latex_content: str, doc_name: str) -> Optional[bytes]:
        """Compile LaTeX content to PDF"""
        if not self.latex_available:
            logger.warning(f"LaTeX not available, cannot compile {doc_name} to PDF")
            return None
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write LaTeX content
                tex_file = temp_path / f"{doc_name}.tex"
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile LaTeX (run twice for references)
                for _ in range(2):
                    result = subprocess.run([
                        self.latex_command,
                        '-interaction=nonstopmode',
                        '-output-directory', str(temp_path),
                        str(tex_file)
                    ], capture_output=True, text=True, timeout=60)
                    
                    if result.returncode != 0:
                        logger.error(f"LaTeX compilation failed for {doc_name}")
                        logger.error(f"LaTeX output: {result.stdout}")
                        return None
                
                # Read generated PDF
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
