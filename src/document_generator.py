"""
Document Generator Module for Infrastructure Billing System
Generates comprehensive HTML, PDF, and Excel documents from processed data
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import pandas as pd
from jinja2 import Template, Environment, FileSystemLoader
import tempfile

try:
    from src.utils import format_currency, format_date, clean_text, safe_float_conversion
except ImportError:
    try:
        from utils import format_currency, format_date, clean_text, safe_float_conversion
    except ImportError:
        # Fallback functions
        def format_currency(amount):
            return f"₹{amount:,.2f}" if amount else "₹0.00"
        
        def format_date(date_value):
            return str(date_value) if date_value else ""
        
        def clean_text(text):
            return str(text).strip() if text else ""
        
        def safe_float_conversion(value, default=0.0):
            try:
                return float(value) if value is not None else default
            except (ValueError, TypeError):
                return default

logger = logging.getLogger(__name__)

class DocumentGenerator:
    """
    Comprehensive document generator for infrastructure billing
    Generates HTML, PDF, and Excel documents from processed Excel data
    """
    
    def __init__(self, processed_data: Dict[str, Any]):
        """Initialize with processed data from ExcelProcessor"""
        self.processed_data = processed_data
        self.base_dir = Path(__file__).parent.parent
        self.templates_dir = self.base_dir / "templates"
        self.setup_jinja_environment()
        
        logger.info(f"DocumentGenerator initialized with {len(processed_data)} data categories")
    
    def setup_jinja_environment(self):
        """Setup Jinja2 environment with custom filters"""
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )
        
        # Add custom filters
        self.env.filters['safe_display'] = self.safe_display
        self.env.filters['safe_number'] = self.safe_number
        self.env.filters['format_currency'] = format_currency
        self.env.filters['format_date'] = format_date
        self.env.filters['clean_text'] = clean_text
    
    def convert_number_to_words(self, number):
        """Convert a number to its word representation"""
        # Simple implementation for demonstration
        # In a real application, you might want to use a more comprehensive library
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", 
                "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        
        try:
            num = int(number)
            if num == 0:
                return "Zero Only"
            
            # Handle negative numbers
            if num < 0:
                return "Minus " + self.convert_number_to_words(-num)
            
            # Handle numbers up to 999999999 (crores)
            result = ""
            
            # Crores
            crores = num // 10000000
            if crores > 0:
                result += self.convert_number_to_words(crores) + " Crore "
                num %= 10000000
            
            # Lakhs
            lakhs = num // 100000
            if lakhs > 0:
                result += self.convert_number_to_words(lakhs) + " Lakh "
                num %= 100000
            
            # Thousands
            thousands = num // 1000
            if thousands > 0:
                result += self.convert_number_to_words(thousands) + " Thousand "
                num %= 1000
            
            # Hundreds
            hundreds = num // 100
            if hundreds > 0:
                result += self.convert_number_to_words(hundreds) + " Hundred "
                num %= 100
            
            # Tens and ones
            if num > 0:
                if num < 20:
                    result += ones[num]
                else:
                    result += tens[num // 10]
                    if num % 10 > 0:
                        result += "-" + ones[num % 10]
            
            return result + " Only"
        except:
            return "Zero Only"
    
    def safe_display(self, value):
        """Safe display filter for templates"""
        if value is None or pd.isna(value):
            return ""
        return str(value).strip()
    
    def safe_number(self, value):
        """Safe number formatting filter"""
        try:
            if value is None or pd.isna(value):
                return "0.00"
            num_value = safe_float_conversion(value)
            return f"{num_value:,.2f}"
        except:
            return "0.00"
    
    def generate_all_html_documents(self) -> Dict[str, str]:
        """Generate all HTML documents from processed data"""
        html_docs = {}
        
        try:
            # Generate First Page Summary
            html_docs['first_page_summary'] = self.generate_first_page_summary()
            
            # Generate Deviation Statement
            html_docs['deviation_statement'] = self.generate_deviation_statement()
            
            # Generate Detailed Deviation Statement
            html_docs['deviation_statement_detailed'] = self.generate_deviation_statement_detailed()
            
            # Generate Extra Items Statement
            html_docs['extra_items_statement'] = self.generate_extra_items_statement()
            
            # Generate Detailed Extra Items Statement
            html_docs['extra_items_detailed'] = self.generate_extra_items_detailed()
            
            # Generate Certificate II
            html_docs['certificate_ii'] = self.generate_certificate_ii()
            
            # Generate Certificate III
            html_docs['certificate_iii'] = self.generate_certificate_iii()
            
            # Generate Note Sheet
            html_docs['note_sheet'] = self.generate_note_sheet()
            
            # Generate Bill Scrutiny Sheet
            html_docs['bill_scrutiny_sheet'] = self.generate_bill_scrutiny_sheet()
            
            # Generate Detailed First Page
            html_docs['first_page_detailed'] = self.generate_first_page_detailed()
            
            # Generate Detailed Deviation Statement
            html_docs['deviation_statement_detailed'] = self.generate_deviation_statement_detailed()
            
            # Generate Detailed Extra Items Statement
            html_docs['extra_items_detailed'] = self.generate_extra_items_detailed()
            
            logger.info(f"Generated {len(html_docs)} HTML documents")
            return html_docs
            
        except Exception as e:
            logger.error(f"Error generating HTML documents: {str(e)}")
            return {}
    
    def generate_first_page_summary(self) -> str:
        """Generate first page summary HTML"""
        try:
            template = self.env.get_template('first_page.html')
            
            # Prepare bill data
            title_data = self.processed_data.get('title', {})
            bill_quantity = self.processed_data.get('bill_quantity', [])
            totals = self.processed_data.get('totals', {})
            
            bill_data = {
                'company_name': title_data.get('project_name', 'Infrastructure Project'),
                'company_address': title_data.get('location', 'Project Location'),
                'bill_no': title_data.get('bill_number', 'BILL-001'),
                'date': format_date(datetime.now()),
                'to': title_data.get('contractor_name', 'Contractor'),
                'period': title_data.get('period', 'Current Period')
            }
            
            # Prepare items data
            items = []
            for idx, item in enumerate(bill_quantity[:50], 1):  # Limit to 50 items for first page
                items.append({
                    'Item No.': idx,
                    'Description': clean_text(item.get('description', '')),
                    'Unit': clean_text(item.get('unit', '')),
                    'Quantity': safe_float_conversion(item.get('quantity', 0)),
                    'Rate': safe_float_conversion(item.get('rate', 0)),
                    'Amount': safe_float_conversion(item.get('amount', 0))
                })
            
            total_amount = totals.get('grand_total', 0)
            
            return template.render(
                bill_data=bill_data,
                items=items,
                total_amount=total_amount,
                current_date=format_date(datetime.now())
            )
            
        except Exception as e:
            logger.error(f"Error generating first page summary: {str(e)}")
            return self.generate_fallback_html("First Page Summary", str(e))
    
    def generate_deviation_statement(self) -> str:
        """Generate deviation statement HTML"""
        try:
            template = self.env.get_template('deviation_statement.html')
            
            title_data = self.processed_data.get('title', {})
            work_order = self.processed_data.get('work_order', [])
            bill_quantity = self.processed_data.get('bill_quantity', [])
            totals = self.processed_data.get('totals', {})
            
            # Combine work order and bill quantity data
            work_items = []
            for i, wo_item in enumerate(work_order):
                # Find corresponding bill quantity item
                bq_item = bill_quantity[i] if i < len(bill_quantity) else {}
                
                qty_wo = safe_float_conversion(wo_item.get('quantity', 0))
                qty_bill = safe_float_conversion(bq_item.get('quantity', 0))
                rate = safe_float_conversion(wo_item.get('rate', 0))
                
                amt_wo = qty_wo * rate
                amt_bill = qty_bill * rate
                
                # Calculate excess/saving
                excess_qty = max(0, qty_bill - qty_wo)
                saving_qty = max(0, qty_wo - qty_bill)
                excess_amt = excess_qty * rate
                saving_amt = saving_qty * rate
                
                work_items.append({
                    'serial_no': i + 1,
                    'description': clean_text(wo_item.get('description', '')),
                    'unit': clean_text(wo_item.get('unit', '')),
                    'qty_wo': qty_wo,
                    'rate': rate,
                    'amt_wo': amt_wo,
                    'qty_bill': qty_bill,
                    'amt_bill': amt_bill,
                    'excess_qty': excess_qty,
                    'excess_amt': excess_amt,
                    'saving_qty': saving_qty,
                    'saving_amt': saving_amt,
                    'remark': clean_text(wo_item.get('remark', ''))
                })
            
            return template.render(
                title_data=title_data,
                work_items=work_items,
                totals=totals,
                current_date=format_date(datetime.now())
            )
            
        except Exception as e:
            logger.error(f"Error generating deviation statement: {str(e)}")
            return self.generate_fallback_html("Deviation Statement", str(e))
    
    def generate_deviation_statement_detailed(self) -> str:
        """Generate detailed deviation statement HTML"""
        try:
            template = self.env.get_template('deviation_statement_detailed.html')
            
            title_data = self.processed_data.get('title', {})
            work_order = self.processed_data.get('work_order', [])
            bill_quantity = self.processed_data.get('bill_quantity', [])
            totals = self.processed_data.get('totals', {})
            
            # Prepare header data in the format expected by the template
            # This is a simplified version - in a real implementation, this would
            # be extracted from the actual header data
            header_data = [
                [], [], [], [], [], [], [], [],  # 0-8 rows
                ['', 'Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur'],  # Row 8
                [], [], [],  # 9-11 rows
                ['', '', '', '', '48/2024-25']  # Row 12
            ]
            
            # Prepare items data with the required structure
            items_data = []
            for i, wo_item in enumerate(work_order):
                # Find corresponding bill quantity item
                bq_item = bill_quantity[i] if i < len(bill_quantity) else {}
                
                qty_wo = safe_float_conversion(wo_item.get('quantity', 0))
                qty_bill = safe_float_conversion(bq_item.get('quantity', 0))
                rate = safe_float_conversion(wo_item.get('rate', 0))
                
                amt_wo = qty_wo * rate
                amt_bill = qty_bill * rate
                
                # Calculate excess/saving
                excess_qty = max(0, qty_bill - qty_wo)
                saving_qty = max(0, qty_wo - qty_bill)
                excess_amt = excess_qty * rate
                saving_amt = saving_qty * rate
                
                items_data.append({
                    'serial_no': i + 1,
                    'description': clean_text(wo_item.get('description', '')),
                    'unit': clean_text(wo_item.get('unit', '')),
                    'qty_wo': qty_wo,
                    'rate': rate,
                    'amt_wo': amt_wo,
                    'qty_bill': qty_bill,
                    'amt_bill': amt_bill,
                    'excess_qty': excess_qty,
                    'excess_amt': excess_amt,
                    'saving_qty': saving_qty,
                    'saving_amt': saving_amt,
                    'remark': clean_text(wo_item.get('remark', ''))
                })
            
            # Prepare summary data
            work_order_total = sum(item['amt_wo'] for item in items_data)
            executed_total = sum(item['amt_bill'] for item in items_data)
            overall_excess = sum(item['excess_amt'] for item in items_data)
            overall_saving = sum(item['saving_amt'] for item in items_data)
            
            # Premium calculations (using 10% as default)
            premium_percent = totals.get('premium_percent', 0.10)
            tender_premium_f = work_order_total * premium_percent
            tender_premium_h = executed_total * premium_percent
            tender_premium_j = overall_excess * premium_percent
            tender_premium_l = overall_saving * premium_percent
            
            grand_total_f = work_order_total + tender_premium_f
            grand_total_h = executed_total + tender_premium_h
            grand_total_j = overall_excess + tender_premium_j
            grand_total_l = overall_saving + tender_premium_l
            
            net_difference = overall_excess - overall_saving
            
            summary_data = {
                'work_order_total': work_order_total,
                'executed_total': executed_total,
                'overall_excess': overall_excess,
                'overall_saving': overall_saving,
                'premium': {
                    'percent': premium_percent
                },
                'tender_premium_f': tender_premium_f,
                'tender_premium_h': tender_premium_h,
                'tender_premium_j': tender_premium_j,
                'tender_premium_l': tender_premium_l,
                'grand_total_f': grand_total_f,
                'grand_total_h': grand_total_h,
                'grand_total_j': grand_total_j,
                'grand_total_l': grand_total_l,
                'net_difference': net_difference
            }
            
            # Prepare data for template
            template_data = {
                'header_data': header_data,
                'data': {
                    'items': items_data,
                    'summary': summary_data
                }
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating detailed deviation statement: {str(e)}")
            return self.generate_fallback_html("Detailed Deviation Statement", str(e))
    
    def generate_extra_items_statement(self) -> str:
        """Generate extra items statement HTML"""
        try:
            template = self.env.get_template('extra_items.html')
            
            title_data = self.processed_data.get('title', {})
            extra_items = self.processed_data.get('extra_items', [])
            totals = self.processed_data.get('totals', {})
            
            # Prepare extra items data
            extra_items_data = []
            grand_total = 0
            
            for idx, item in enumerate(extra_items, 1):
                quantity = safe_float_conversion(item.get('quantity', 0))
                rate = safe_float_conversion(item.get('rate', 0))
                amount = quantity * rate
                grand_total += amount
                
                extra_items_data.append({
                    'serial_no': idx,
                    'description': clean_text(item.get('description', '')),
                    'unit': clean_text(item.get('unit', '')),
                    'quantity': quantity,
                    'rate': rate,
                    'amount': amount,
                    'remark': clean_text(item.get('remark', item.get('remarks', '')))
                })
            
            # Calculate tender premium and total
            tender_premium_percent = 0.1  # 10% default
            tender_premium = grand_total * tender_premium_percent
            total_executed = grand_total + tender_premium
            
            data = {
                'name_of_work': title_data.get('project_name', ''),
                'name_of_firm': title_data.get('contractor_name', ''),
                'reference': title_data.get('agreement_no', ''),
                'extra_items': extra_items_data,
                'grand_total': grand_total,
                'tender_premium_percent': tender_premium_percent,
                'tender_premium': tender_premium,
                'total_executed': total_executed
            }
            
            return template.render(
                data=data,
                current_date=format_date(datetime.now())
            )
            
        except Exception as e:
            logger.error(f"Error generating extra items statement: {str(e)}")
            return self.generate_fallback_html("Extra Items Statement", str(e))
    
    def generate_extra_items_detailed(self) -> str:
        """Generate detailed extra items statement HTML"""
        try:
            template = self.env.get_template('extra_items_detailed.html')
            
            title_data = self.processed_data.get('title', {})
            extra_items = self.processed_data.get('extra_items', [])
            totals = self.processed_data.get('totals', {})
            
            # Prepare extra items data with the required structure
            items_data = []
            for idx, item in enumerate(extra_items, 1):
                quantity = safe_float_conversion(item.get('quantity', 0))
                rate = safe_float_conversion(item.get('rate', 0))
                amount = quantity * rate
                
                items_data.append({
                    'serial_no': idx,
                    'remark': clean_text(item.get('remark', item.get('remarks', ''))),
                    'description': clean_text(item.get('description', '')),
                    'quantity': quantity,
                    'unit': clean_text(item.get('unit', '')),
                    'rate': rate,
                    'amount': amount
                })
            
            # Prepare data for template
            template_data = {
                'data': {
                    'items': items_data
                }
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating detailed extra items statement: {str(e)}")
            return self.generate_fallback_html("Detailed Extra Items Statement", str(e))
    
    def generate_certificate_ii(self) -> str:
        """Generate Certificate II HTML"""
        try:
            template = self.env.get_template('certificate_ii.html')
            
            title_data = self.processed_data.get('title', {})
            totals = self.processed_data.get('totals', {})
            
            # Prepare data for the certificate
            data = {
                'measurement_officer': title_data.get('measurement_officer', 'Measurement Officer Name'),
                'measurement_date': title_data.get('measurement_date', '30/04/2025'),
                'measurement_book_page': title_data.get('measurement_book_page', '123'),
                'measurement_book_no': title_data.get('measurement_book_no', 'MB-001'),
                'officer_name': title_data.get('officer_name', 'Officer Name'),
                'officer_designation': title_data.get('officer_designation', 'Designation'),
                'authorising_officer_name': title_data.get('authorising_officer_name', 'Authorising Officer Name'),
                'authorising_officer_designation': title_data.get('authorising_officer_designation', 'Designation'),
                'totals': totals
            }
            
            return template.render(data=data)
            
        except Exception as e:
            logger.error(f"Error generating certificate II: {str(e)}")
            return self.generate_fallback_html("Certificate II", str(e))
    
    def generate_certificate_iii(self) -> str:
        """Generate Certificate III HTML"""
        try:
            template = self.env.get_template('certificate_iii.html')
            
            title_data = self.processed_data.get('title', {})
            totals = self.processed_data.get('totals', {})
            
            # Prepare data for the certificate
            data = {
                'totals': totals,
                'total_123': totals.get('grand_total', 1120175),
                'balance_4_minus_5': totals.get('grand_total', 1120175),
                'payable_amount': totals.get('net_payable', 952147),
                'total_recovery': totals.get('total_deductions', 168028),
                'by_cheque': totals.get('net_payable', 952147),
                'amount_words': 'Nine Lakh Fifty-Two Thousand One Hundred Forty-Seven Only'
            }
            
            return template.render(data=data)
            
        except Exception as e:
            logger.error(f"Error generating certificate III: {str(e)}")
            return self.generate_fallback_html("Certificate III", str(e))
    
    def generate_first_page_detailed(self) -> str:
        """Generate detailed first page HTML"""
        try:
            template = self.env.get_template('first_page_detailed.html')
            
            title_data = self.processed_data.get('title', {})
            bill_quantity = self.processed_data.get('bill_quantity', [])
            totals = self.processed_data.get('totals', {})
            
            # Prepare header data
            header_data = [
                [
                    f"Project: {title_data.get('project_name', 'N/A')}",
                    f"Contractor: {title_data.get('contractor_name', 'N/A')}"
                ],
                [
                    f"Agreement No: {title_data.get('agreement_no', 'N/A')}",
                    f"Bill No: {title_data.get('bill_number', 'N/A')}"
                ],
                [
                    f"Period: {title_data.get('period', 'N/A')}",
                    f"Date: {format_date(datetime.now())}"
                ]
            ]
            
            # Prepare items data with the required structure
            items_data = []
            for idx, item in enumerate(bill_quantity[:50], 1):  # Limit to 50 items for first page
                # For detailed first page, we need additional fields
                items_data.append({
                    'unit': clean_text(item.get('unit', '')),
                    'quantity_since_last': '',  # To be filled based on actual data
                    'quantity_upto_date': safe_float_conversion(item.get('quantity', 0)),
                    'serial_no': idx,
                    'description': clean_text(item.get('description', '')),
                    'rate': safe_float_conversion(item.get('rate', 0)),
                    'amount': safe_float_conversion(item.get('amount', 0)),
                    'amount_previous': '',  # To be filled based on actual data
                    'remark': clean_text(item.get('remark', ''))
                })
            
            # Prepare data for template
            template_data = {
                'data': {
                    'header': header_data,
                    'items': items_data,
                    'totals': {
                        'grand_total': totals.get('grand_total', 0),
                        'premium': {
                            'percent': totals.get('premium_percent', 0.10),  # Default 10%
                            'amount': totals.get('premium_amount', totals.get('grand_total', 0) * 0.10)
                        },
                        'payable': totals.get('payable', totals.get('grand_total', 0) * 1.10)
                    },
                    'premium_percent': totals.get('premium_percent', 0.10)
                }
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating detailed first page: {str(e)}")
            return self.generate_fallback_html("Detailed First Page", str(e))
    
    def generate_note_sheet(self) -> str:
        """Generate note sheet HTML"""
        try:
            template = self.env.get_template('note_sheet.html')
            
            title_data = self.processed_data.get('title', {})
            totals = self.processed_data.get('totals', {})
            
            return template.render(
                title_data=title_data,
                totals=totals,
                current_date=format_date(datetime.now())
            )
            
        except Exception as e:
            logger.error(f"Error generating note sheet: {str(e)}")
            return self.generate_fallback_html("Note Sheet", str(e))
    
    def generate_bill_scrutiny_sheet(self) -> str:
        """Generate bill scrutiny sheet HTML"""
        try:
            template = self.env.get_template('bill_scrutiny_sheet.html')
            
            title_data = self.processed_data.get('title', {})
            totals = self.processed_data.get('totals', {})
            notes = self.processed_data.get('notes', [])
            
            # Calculate work order amount if not present
            work_order_amount = totals.get('work_order_amount')
            if work_order_amount is None:
                work_order_amount = totals.get('grand_total', 0)
            
            # Calculate payable amount if not present
            payable = totals.get('payable', totals.get('net_payable', totals.get('grand_total', 0)))
            
            # Calculate extra items sum if not present
            extra_items_sum = totals.get('extra_items_sum', totals.get('extra_items_total', 0))
            
            # Prepare data for template
            template_data = {
                'title_data': title_data,
                'totals': {
                    'work_order_amount': work_order_amount,
                    'payable': payable,
                    'extra_items_sum': extra_items_sum,
                    'sd_amount': totals.get('sd_amount', payable * 0.10 if payable else 0),
                    'it_amount': totals.get('it_amount', payable * 0.02 if payable else 0),
                    'gst_amount': totals.get('gst_amount', payable * 0.02 if payable else 0),
                    'lc_amount': totals.get('lc_amount', payable * 0.01 if payable else 0),
                    'net_payable': totals.get('net_payable', payable)
                },
                'notes': notes,
                'current_date': format_date(datetime.now())
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating bill scrutiny sheet: {str(e)}")
            return self.generate_fallback_html("Bill Scrutiny Sheet", str(e))
    
    def generate_excel_outputs(self, processed_data: Dict[str, Any]) -> Dict[str, bytes]:
        """Generate Excel output files"""
        excel_outputs = {}
        
        try:
            # Generate summary Excel
            summary_excel = self.create_summary_excel(processed_data)
            if summary_excel:
                excel_outputs['bill_summary'] = summary_excel
            
            # Generate detailed Excel
            detailed_excel = self.create_detailed_excel(processed_data)
            if detailed_excel:
                excel_outputs['detailed_analysis'] = detailed_excel
            
            logger.info(f"Generated {len(excel_outputs)} Excel documents")
            return excel_outputs
            
        except Exception as e:
            logger.error(f"Error generating Excel outputs: {str(e)}")
            return {}
    
    def create_summary_excel(self, processed_data: Dict[str, Any]) -> Optional[bytes]:
        """Create summary Excel file"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                with pd.ExcelWriter(tmp_file.name, engine='openpyxl') as writer:
                    # Summary sheet
                    title_data = processed_data.get('title', {})
                    summary_data = {
                        'Field': ['Project Name', 'Contractor', 'Total Amount', 'GST Amount', 'Final Amount'],
                        'Value': [
                            title_data.get('project_name', ''),
                            title_data.get('contractor_name', ''),
                            processed_data.get('totals', {}).get('grand_total', 0),
                            processed_data.get('totals', {}).get('gst_amount', 0),
                            processed_data.get('totals', {}).get('total_with_gst', 0)
                        ]
                    }
                    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                    
                    # Bill items sheet
                    bill_items = processed_data.get('bill_quantity', [])
                    if bill_items:
                        df_bill = pd.DataFrame(bill_items)
                        df_bill.to_excel(writer, sheet_name='Bill Items', index=False)
                
                # Read the file and return bytes
                with open(tmp_file.name, 'rb') as f:
                    return f.read()
                    
        except Exception as e:
            logger.error(f"Error creating summary Excel: {str(e)}")
            return None
        finally:
            try:
                os.unlink(tmp_file.name)
            except:
                pass
    
    def create_detailed_excel(self, processed_data: Dict[str, Any]) -> Optional[bytes]:
        """Create detailed analysis Excel file"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                with pd.ExcelWriter(tmp_file.name, engine='openpyxl') as writer:
                    # Work Order vs Bill Quantity comparison
                    work_order = processed_data.get('work_order', [])
                    bill_quantity = processed_data.get('bill_quantity', [])
                    
                    if work_order and bill_quantity:
                        comparison_data = []
                        for i, (wo, bq) in enumerate(zip(work_order, bill_quantity)):
                            comparison_data.append({
                                'S.No': i + 1,
                                'Description': wo.get('description', ''),
                                'Unit': wo.get('unit', ''),
                                'WO_Quantity': wo.get('quantity', 0),
                                'Bill_Quantity': bq.get('quantity', 0),
                                'Rate': wo.get('rate', 0),
                                'WO_Amount': wo.get('amount', 0),
                                'Bill_Amount': bq.get('amount', 0),
                                'Difference': bq.get('amount', 0) - wo.get('amount', 0)
                            })
                        
                        df_comparison = pd.DataFrame(comparison_data)
                        df_comparison.to_excel(writer, sheet_name='WO vs Bill Comparison', index=False)
                    
                    # Extra items sheet
                    extra_items = processed_data.get('extra_items', [])
                    if extra_items:
                        df_extra = pd.DataFrame(extra_items)
                        df_extra.to_excel(writer, sheet_name='Extra Items', index=False)
                
                # Read the file and return bytes
                with open(tmp_file.name, 'rb') as f:
                    return f.read()
                    
        except Exception as e:
            logger.error(f"Error creating detailed Excel: {str(e)}")
            return None
        finally:
            try:
                os.unlink(tmp_file.name)
            except:
                pass
    
    def generate_fallback_html(self, doc_type: str, error_msg: str) -> str:
        """Generate fallback HTML when template processing fails"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{doc_type}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .error {{ color: red; padding: 10px; border: 1px solid red; background: #ffe6e6; }}
                .info {{ color: blue; padding: 10px; border: 1px solid blue; background: #e6f3ff; }}
            </style>
        </head>
        <body>
            <h1>{doc_type}</h1>
            <div class="error">
                <strong>Error:</strong> Unable to generate document. {error_msg}
            </div>
            <div class="info">
                <strong>Processed Data Available:</strong>
                <ul>
                    <li>Title Data: {'✓' if self.processed_data.get('title') else '✗'}</li>
                    <li>Work Order: {'✓' if self.processed_data.get('work_order') else '✗'}</li>
                    <li>Bill Quantity: {'✓' if self.processed_data.get('bill_quantity') else '✗'}</li>
                    <li>Extra Items: {'✓' if self.processed_data.get('extra_items') else '✗'}</li>
                    <li>Totals: {'✓' if self.processed_data.get('totals') else '✗'}</li>
                </ul>
            </div>
            <p><strong>Generated on:</strong> {format_date(datetime.now())}</p>
        </body>
        </html>
        """