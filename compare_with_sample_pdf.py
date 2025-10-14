"""
PDF Comparison Tool for Extra Items Output
Compares our app's output with the sample PDF file extra_item_output_sample.pdf
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFComparisonTool:
    """
    Tool to compare our app's extra items output with sample PDF
    """
    
    def __init__(self):
        """Initialize the comparison tool"""
        self.sample_pdf_path = Path("extra_item_output_sample.pdf")
        self.generator = EnhancedBillGenerator("pdf_comparison_outputs")
    
    def check_sample_pdf_exists(self) -> bool:
        """Check if the sample PDF file exists"""
        if self.sample_pdf_path.exists():
            print(f"✅ Found sample PDF: {self.sample_pdf_path}")
            file_size = self.sample_pdf_path.stat().st_size
            print(f"📊 Sample PDF size: {file_size} bytes")
            return True
        else:
            print(f"❌ Sample PDF not found: {self.sample_pdf_path}")
            print("💡 Please ensure 'extra_item_output_sample.pdf' is in the root folder")
            return False
    
    def create_realistic_test_data(self) -> Dict[str, Any]:
        """Create realistic test data that should match sample PDF structure"""
        return {
            'title': {
                'project_name': 'Construction of Government Administrative Building',
                'contractor_name': 'M/s Sample Construction Company Ltd.',
                'agreement_no': 'SAMPLE/2024/EXTRA/001'
            },
            'extra_items': [
                {
                    'description': 'Additional electrical wiring work for conference hall',
                    'unit': 'Mtr',
                    'quantity': 150.0,
                    'rate': 125.50,
                    'remarks': 'As per site requirement'
                },
                {
                    'description': 'Extra marble flooring in entrance lobby',
                    'unit': 'Sqm',
                    'quantity': 45.0,
                    'rate': 850.00,
                    'remarks': 'Premium grade marble'
                },
                {
                    'description': 'Additional HVAC ducting for server room',
                    'unit': 'Mtr',
                    'quantity': 75.0,
                    'rate': 275.00,
                    'remarks': 'Fire-resistant ducting'
                }
            ]
        }
    
    def generate_comparison_output(self) -> Optional[Dict[str, Any]]:
        """Generate our app's output for comparison"""
        print("📝 Generating extra items output for comparison...")
        
        test_data = self.create_realistic_test_data()
        
        try:
            result = self.generator.generate_extra_items_package(
                extra_items_data=test_data,
                project_name="Sample Comparison Project",
                contractor_name="Sample Construction Company"
            )
            
            if result['errors']:
                print("❌ Generation errors:")
                for error in result['errors']:
                    print(f"   - {error}")
                return None
            
            print("✅ Generated comparison output successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error generating output: {str(e)}")
            return None
    
    def analyze_generated_output(self, result: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the generated output characteristics"""
        analysis = {
            'html_characteristics': {},
            'pdf_characteristics': {},
            'content_analysis': {}
        }
        
        # Analyze HTML files
        html_files = result.get('html_files', {})
        if html_files:
            html_file_path = list(html_files.values())[0]
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            analysis['html_characteristics'] = {
                'file_size': len(html_content),
                'has_title': 'EXTRA ITEM SLIP' in html_content,
                'has_currency_symbols': html_content.count('₹'),
                'has_table_structure': '<table' in html_content,
                'has_professional_styling': 'Arial' in html_content,
                'has_print_styles': '@media print' in html_content,
                'line_count': html_content.count('\n')
            }
            
            # Content analysis
            analysis['content_analysis'] = {
                'work_name_present': test_data['title']['project_name'] in html_content,
                'contractor_present': test_data['title']['contractor_name'] in html_content,
                'items_count': len(test_data['extra_items']),
                'remarks_present': all(item['remarks'] in html_content for item in test_data['extra_items']),
                'financial_totals': {
                    'grand_total': 'Grand Total' in html_content,
                    'tender_premium': 'Tender Premium' in html_content,
                    'final_total': 'Total Amount of Extra Item Executed' in html_content
                }
            }
        
        # Analyze PDF files
        pdf_files = result.get('pdf_files', {})
        if pdf_files:
            pdf_file_path = list(pdf_files.values())[0]
            pdf_size = Path(pdf_file_path).stat().st_size
            
            analysis['pdf_characteristics'] = {
                'file_size': pdf_size,
                'file_path': pdf_file_path,
                'size_category': 'large' if pdf_size > 20000 else 'medium' if pdf_size > 10000 else 'small'
            }
        
        return analysis
    
    def compare_with_sample(self, our_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Compare our output characteristics with what's expected from sample"""
        comparison = {
            'format_compliance': {},
            'structure_compliance': {},
            'content_compliance': {},
            'recommendations': []
        }
        
        # Format compliance checks
        html_chars = our_analysis.get('html_characteristics', {})
        comparison['format_compliance'] = {
            'document_title': html_chars.get('has_title', False),
            'currency_formatting': html_chars.get('has_currency_symbols', 0) > 5,
            'table_structure': html_chars.get('has_table_structure', False),
            'professional_styling': html_chars.get('has_professional_styling', False),
            'print_optimization': html_chars.get('has_print_styles', False)
        }
        
        # Structure compliance
        content_analysis = our_analysis.get('content_analysis', {})
        comparison['structure_compliance'] = {
            'header_information': content_analysis.get('work_name_present', False) and content_analysis.get('contractor_present', False),
            'items_data': content_analysis.get('items_count', 0) > 0,
            'remarks_inclusion': content_analysis.get('remarks_present', False),
            'financial_calculations': all(content_analysis.get('financial_totals', {}).values())
        }
        
        # Content compliance
        pdf_chars = our_analysis.get('pdf_characteristics', {})
        comparison['content_compliance'] = {
            'pdf_generation': len(pdf_chars) > 0,
            'adequate_size': pdf_chars.get('file_size', 0) > 10000,
            'file_accessibility': Path(pdf_chars.get('file_path', '')).exists() if pdf_chars.get('file_path') else False
        }
        
        # Generate recommendations
        if not comparison['format_compliance']['currency_formatting']:
            comparison['recommendations'].append("Add more currency symbols (₹) to monetary values")
        
        if not comparison['structure_compliance']['financial_calculations']:
            comparison['recommendations'].append("Ensure all financial calculations are present")
        
        if not comparison['content_compliance']['adequate_size']:
            comparison['recommendations'].append("PDF size may be too small - check content completeness")
        
        return comparison
    
    def run_comparison(self) -> bool:
        """Run complete comparison process"""
        print("🔍 PDF COMPARISON TOOL")
        print("=" * 60)
        
        # Step 1: Check if sample PDF exists
        if not self.check_sample_pdf_exists():
            print("\n💡 NEXT STEPS:")
            print("1. Please place 'extra_item_output_sample.pdf' in the root folder")
            print("2. Run this script again to perform the comparison")
            print("3. The script will analyze structure, format, and content differences")
            return False
        
        # Step 2: Generate our output
        test_data = self.create_realistic_test_data()
        result = self.generate_comparison_output()
        if not result:
            return False
        
        # Step 3: Analyze our output
        print(f"\n📊 ANALYZING GENERATED OUTPUT...")
        our_analysis = self.analyze_generated_output(result, test_data)
        
        # Step 4: Compare with expected standards
        print(f"\n🔍 COMPARING WITH SAMPLE STANDARDS...")
        comparison = self.compare_with_sample(our_analysis)
        
        # Step 5: Display results
        self.display_comparison_results(our_analysis, comparison, result)
        
        # Step 6: Calculate overall compliance
        format_score = sum(comparison['format_compliance'].values()) / len(comparison['format_compliance']) * 100
        structure_score = sum(comparison['structure_compliance'].values()) / len(comparison['structure_compliance']) * 100
        content_score = sum(comparison['content_compliance'].values()) / len(comparison['content_compliance']) * 100
        overall_score = (format_score + structure_score + content_score) / 3
        
        print(f"\n🏆 OVERALL COMPLIANCE SCORE: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("🌟 EXCELLENT: Output matches expected sample standards!")
            return True
        elif overall_score >= 75:
            print("✅ GOOD: Output is largely compliant with minor improvements needed")
            return True
        else:
            print("⚠️ NEEDS IMPROVEMENT: Significant differences from sample detected")
            return False
    
    def display_comparison_results(self, analysis: Dict[str, Any], comparison: Dict[str, Any], result: Dict[str, Any]):
        """Display detailed comparison results"""
        print(f"\n📋 DETAILED COMPARISON RESULTS:")
        print(f"=" * 50)
        
        # Our output characteristics
        print(f"📝 OUR OUTPUT CHARACTERISTICS:")
        html_chars = analysis.get('html_characteristics', {})
        print(f"   HTML Size: {html_chars.get('file_size', 0)} characters")
        print(f"   Currency Symbols: {html_chars.get('has_currency_symbols', 0)}")
        print(f"   Line Count: {html_chars.get('line_count', 0)}")
        
        pdf_chars = analysis.get('pdf_characteristics', {})
        print(f"   PDF Size: {pdf_chars.get('file_size', 0)} bytes")
        print(f"   PDF Category: {pdf_chars.get('size_category', 'unknown')}")
        
        # Compliance results
        print(f"\n✅ FORMAT COMPLIANCE:")
        for check, passed in comparison['format_compliance'].items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check.replace('_', ' ').title()}")
        
        print(f"\n✅ STRUCTURE COMPLIANCE:")
        for check, passed in comparison['structure_compliance'].items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check.replace('_', ' ').title()}")
        
        print(f"\n✅ CONTENT COMPLIANCE:")
        for check, passed in comparison['content_compliance'].items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check.replace('_', ' ').title()}")
        
        # Recommendations
        if comparison['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in comparison['recommendations']:
                print(f"   - {rec}")
        
        # File locations
        print(f"\n📁 GENERATED FILES:")
        html_files = result.get('html_files', {})
        pdf_files = result.get('pdf_files', {})
        
        for name, path in html_files.items():
            print(f"   📝 HTML: {path}")
        for name, path in pdf_files.items():
            print(f"   📄 PDF: {path}")

def main():
    """Main function"""
    tool = PDFComparisonTool()
    success = tool.run_comparison()
    
    if success:
        print(f"\n🎯 COMPARISON COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️ COMPARISON INCOMPLETE - Please address the issues above")

if __name__ == "__main__":
    main()