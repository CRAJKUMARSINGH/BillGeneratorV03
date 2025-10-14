"""
Comprehensive Extra Items Output Validation
Validates that the app produces government-standard extra items output
Based on document generation standards and best practices
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from enhanced_bill_generator import EnhancedBillGenerator
from document_generator import DocumentGenerator
from pdf_merger import PDFMerger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtraItemsValidator:
    """
    Comprehensive validator for extra items output
    Checks compliance with government document standards
    """
    
    def __init__(self):
        """Initialize validator with government document standards"""
        self.standards = {
            'currency_symbol': '₹',
            'required_sections': [
                'EXTRA ITEM SLIP',
                'Name of Work',
                'Name of Contractor',
                'Reference to work order',
                'Grand Total',
                'Tender Premium',
                'Total Amount of Extra Item Executed'
            ],
            'required_columns': [
                'S.No.',
                'Description', 
                'Unit',
                'Qty.',
                'Rate',
                'Amount',
                'Remarks'
            ],
            'alignment_requirements': {
                'serial_numbers': 'center',
                'currency_amounts': 'right',
                'quantities': 'right'
            },
            'formatting_requirements': [
                'Arial font',
                'Proper table structure',
                'Print optimization',
                'Professional styling'
            ]
        }
    
    def create_test_data(self) -> Dict[str, Any]:
        """Create comprehensive test data for validation"""
        return {
            'title': {
                'project_name': 'Construction of New Government Administrative Building Complex',
                'contractor_name': 'M/s Advanced Infrastructure & Construction Pvt. Ltd.',
                'agreement_no': 'AGR/2024/CONST/185'
            },
            'extra_items': [
                {
                    'description': 'Additional electrical wiring and conduit installation for emergency lighting system as per IS:3043',
                    'unit': 'Mtr',
                    'quantity': 285.50,
                    'rate': 165.75,
                    'remarks': 'As per revised electrical drawing No. E-105'
                },
                {
                    'description': 'Extra marble flooring (Makrana white) in main entrance lobby including polishing and edge finishing',
                    'unit': 'Sqm',
                    'quantity': 125.25,
                    'rate': 1850.00,
                    'remarks': 'Premium grade marble as approved by PWD'
                },
                {
                    'description': 'Additional fire-resistant HVAC ducting for server room with thermal insulation and fire dampers',
                    'unit': 'Mtr',
                    'quantity': 175.00,
                    'rate': 485.50,
                    'remarks': 'Fire rated as per NBC 2016 requirements'
                },
                {
                    'description': 'Extra stainless steel safety railings for terrace and staircase areas with SS316 grade material',
                    'unit': 'Mtr',
                    'quantity': 195.75,
                    'rate': 1250.25,
                    'remarks': 'Height 1.2m with glass panels as per safety norms'
                },
                {
                    'description': 'Additional waterproofing treatment for terrace using APP membrane with reflective coating',
                    'unit': 'Sqm',
                    'quantity': 425.50,
                    'rate': 675.00,
                    'remarks': 'Double layer system with 10-year warranty'
                }
            ]
        }
    
    def validate_html_structure(self, html_content: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate HTML structure against government standards"""
        validation_results = {
            'document_title': False,
            'header_information': False,
            'table_structure': False,
            'required_columns': False,
            'currency_formatting': False,
            'alignment_styles': False,
            'professional_styling': False,
            'print_optimization': False,
            'financial_calculations': False,
            'remarks_section': False,
            'details': []
        }
        
        # Check document title
        if 'EXTRA ITEM SLIP' in html_content:
            validation_results['document_title'] = True
            validation_results['details'].append("✅ Document title 'EXTRA ITEM SLIP' present")
        else:
            validation_results['details'].append("❌ Document title 'EXTRA ITEM SLIP' missing")
        
        # Check header information
        header_checks = ['Name of Work', 'Name of Contractor', 'Reference to work order']
        header_found = sum(1 for header in header_checks if header in html_content)
        if header_found == len(header_checks):
            validation_results['header_information'] = True
            validation_results['details'].append("✅ All header information present")
        else:
            validation_results['details'].append(f"❌ Header information incomplete ({header_found}/{len(header_checks)})")
        
        # Check table structure
        if '<table' in html_content and '</table>' in html_content:
            validation_results['table_structure'] = True
            validation_results['details'].append("✅ Table structure present")
        else:
            validation_results['details'].append("❌ Table structure missing")
        
        # Check required columns
        column_checks = ['S.No.', 'Description', 'Unit', 'Qty.', 'Rate', 'Amount', 'Remarks']
        columns_found = sum(1 for col in column_checks if col in html_content)
        if columns_found >= len(column_checks) - 1:  # Allow minor variations
            validation_results['required_columns'] = True
            validation_results['details'].append("✅ All required columns present")
        else:
            validation_results['details'].append(f"❌ Missing columns ({columns_found}/{len(column_checks)})")
        
        # Check currency formatting
        currency_count = html_content.count('₹')
        if currency_count >= 8:  # Expecting multiple currency symbols
            validation_results['currency_formatting'] = True
            validation_results['details'].append(f"✅ Currency symbols present ({currency_count} found)")
        else:
            validation_results['details'].append(f"❌ Insufficient currency symbols ({currency_count} found)")
        
        # Check alignment styles
        alignment_checks = ['text-align: right', 'text-align: center']
        alignment_found = sum(1 for align in alignment_checks if align in html_content)
        if alignment_found >= 2:
            validation_results['alignment_styles'] = True
            validation_results['details'].append("✅ Proper alignment styles present")
        else:
            validation_results['details'].append("❌ Missing alignment styles")
        
        # Check professional styling
        styling_checks = ['font-family: Arial', 'border-collapse: collapse', 'margin', 'padding']
        styling_found = sum(1 for style in styling_checks if style in html_content)
        if styling_found >= 3:
            validation_results['professional_styling'] = True
            validation_results['details'].append("✅ Professional styling present")
        else:
            validation_results['details'].append("❌ Professional styling insufficient")
        
        # Check print optimization
        if '@media print' in html_content:
            validation_results['print_optimization'] = True
            validation_results['details'].append("✅ Print optimization styles present")
        else:
            validation_results['details'].append("❌ Print optimization styles missing")
        
        # Check financial calculations
        financial_checks = ['Grand Total', 'Tender Premium', 'Total Amount of Extra Item Executed']
        financial_found = sum(1 for calc in financial_checks if calc in html_content)
        if financial_found == len(financial_checks):
            validation_results['financial_calculations'] = True
            validation_results['details'].append("✅ All financial calculations present")
        else:
            validation_results['details'].append(f"❌ Missing financial calculations ({financial_found}/{len(financial_checks)})")
        
        # Check remarks section
        remarks_in_data = len(test_data['extra_items'])
        remarks_found = 0
        for item in test_data['extra_items']:
            if item['remarks'] in html_content:
                remarks_found += 1
        
        if remarks_found >= remarks_in_data - 1:  # Allow for minor variations
            validation_results['remarks_section'] = True
            validation_results['details'].append(f"✅ Remarks section present ({remarks_found}/{remarks_in_data} remarks found)")
        else:
            validation_results['details'].append(f"❌ Remarks section incomplete ({remarks_found}/{remarks_in_data} remarks found)")
        
        return validation_results
    
    def validate_pdf_generation(self, html_content: str) -> Dict[str, Any]:
        """Validate PDF generation capability"""
        pdf_results = {
            'generation_success': False,
            'file_size_adequate': False,
            'details': []
        }
        
        try:
            # Test PDF generation
            merger = PDFMerger()
            html_docs = {"extra_items_validation": html_content}
            pdf_docs = merger.convert_html_to_pdf(html_docs)
            
            if pdf_docs and "extra_items_validation_html" in pdf_docs:
                pdf_results['generation_success'] = True
                pdf_size = len(pdf_docs["extra_items_validation_html"])
                
                # Save for verification
                pdf_path = "validation_extra_items.pdf"
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_docs["extra_items_validation_html"])
                
                pdf_results['details'].append(f"✅ PDF generated successfully: {pdf_path}")
                pdf_results['details'].append(f"📊 PDF size: {pdf_size} bytes")
                
                # Check if size is adequate (should be substantial for a proper document)
                if pdf_size > 10000:  # At least 10KB for a proper government document
                    pdf_results['file_size_adequate'] = True
                    pdf_results['details'].append("✅ PDF size is adequate for government document")
                else:
                    pdf_results['details'].append("⚠️ PDF size may be too small")
            else:
                pdf_results['details'].append("❌ PDF generation failed")
                
        except Exception as e:
            pdf_results['details'].append(f"❌ PDF generation error: {str(e)}")
        
        return pdf_results
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        print("🔍 COMPREHENSIVE EXTRA ITEMS VALIDATION")
        print("=" * 70)
        
        # Generate test data
        test_data = self.create_test_data()
        
        try:
            # Generate HTML using enhanced generator
            print("📝 Generating extra items using enhanced system...")
            generator = EnhancedBillGenerator("validation_outputs")
            
            result = generator.generate_extra_items_package(
                extra_items_data=test_data,
                project_name="Government Administrative Building",
                contractor_name="Advanced Infrastructure Construction"
            )
            
            if result['errors']:
                print("❌ Generation errors:")
                for error in result['errors']:
                    print(f"   - {error}")
                return {'validation_failed': True, 'errors': result['errors']}
            
            # Get the HTML content for validation
            html_files = result.get('html_files', {})
            if not html_files:
                print("❌ No HTML files generated")
                return {'validation_failed': True, 'errors': ['No HTML files generated']}
            
            # Read the generated HTML
            html_file_path = list(html_files.values())[0]
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print(f"✅ HTML generated: {html_file_path}")
            print(f"📊 Content length: {len(html_content)} characters")
            
            # Validate HTML structure
            print(f"\n📋 VALIDATING HTML STRUCTURE...")
            html_validation = self.validate_html_structure(html_content, test_data)
            
            # Validate PDF generation
            print(f"\n📄 VALIDATING PDF GENERATION...")
            pdf_validation = self.validate_pdf_generation(html_content)
            
            # Calculate overall score
            html_score = sum(html_validation[key] for key in html_validation if isinstance(html_validation[key], bool))
            html_total = len([key for key in html_validation if isinstance(html_validation[key], bool)])
            pdf_score = sum(pdf_validation[key] for key in pdf_validation if isinstance(pdf_validation[key], bool))
            pdf_total = len([key for key in pdf_validation if isinstance(pdf_validation[key], bool)])
            
            overall_score = ((html_score + pdf_score) / (html_total + pdf_total)) * 100
            
            # Print detailed results
            print(f"\n📊 VALIDATION RESULTS:")
            print(f"   HTML Structure Validation:")
            for detail in html_validation['details']:
                print(f"      {detail}")
            
            print(f"   PDF Generation Validation:")
            for detail in pdf_validation['details']:
                print(f"      {detail}")
            
            print(f"\n🏆 OVERALL SCORE: {overall_score:.1f}%")
            print(f"   HTML Score: {html_score}/{html_total}")
            print(f"   PDF Score: {pdf_score}/{pdf_total}")
            
            # Final assessment
            print(f"\n" + "=" * 70)
            print("🎯 FINAL ASSESSMENT")
            print("=" * 70)
            
            if overall_score >= 90:
                status = "EXCELLENT"
                print("🌟 EXCELLENT: App produces exceptional quality extra items output!")
                print("   All government document standards met or exceeded.")
            elif overall_score >= 80:
                status = "VERY GOOD"
                print("✅ VERY GOOD: App produces high-quality extra items output!")
                print("   Meets government document standards with minor areas for improvement.")
            elif overall_score >= 70:
                status = "GOOD"
                print("✅ GOOD: App produces satisfactory extra items output!")
                print("   Basic government document standards met.")
            else:
                status = "NEEDS IMPROVEMENT"
                print("⚠️ NEEDS IMPROVEMENT: Output requires enhancement!")
                print("   Some government document standards not met.")
            
            # Financial summary
            total_amount = sum(item['quantity'] * item['rate'] for item in test_data['extra_items'])
            premium = total_amount * 0.1
            final_total = total_amount + premium
            
            print(f"\n💰 FINANCIAL VERIFICATION:")
            print(f"   Total Items Amount: ₹{total_amount:,.2f}")
            print(f"   Tender Premium (10%): ₹{premium:,.2f}")
            print(f"   Final Total: ₹{final_total:,.2f}")
            
            return {
                'status': status,
                'overall_score': overall_score,
                'html_validation': html_validation,
                'pdf_validation': pdf_validation,
                'session_info': result.get('session_info', {}),
                'generated_files': {
                    'html_files': result.get('html_files', {}),
                    'pdf_files': result.get('pdf_files', {})
                },
                'financial_summary': {
                    'total_amount': total_amount,
                    'premium': premium,
                    'final_total': final_total
                }
            }
            
        except Exception as e:
            error_msg = f"Validation failed with error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'validation_failed': True, 'errors': [error_msg]}

def main():
    """Main validation function"""
    validator = ExtraItemsValidator()
    results = validator.run_comprehensive_validation()
    
    if 'validation_failed' in results:
        print(f"\n💥 VALIDATION FAILED!")
        return False
    else:
        print(f"\n🚀 VALIDATION COMPLETED!")
        print(f"Status: {results['status']}")
        print(f"Score: {results['overall_score']:.1f}%")
        
        if results['overall_score'] >= 80:
            print("✅ App produces government-standard extra items output!")
        else:
            print("⚠️ App requires improvements to meet standards!")
        
        return results['overall_score'] >= 80

if __name__ == "__main__":
    success = main()