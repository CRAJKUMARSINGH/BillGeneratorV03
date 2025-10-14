"""
Enhanced Bill Generator with Output Management
Integrates OutputManager with existing DocumentGenerator and PDFMerger
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator
from pdf_merger import PDFMerger
from output_manager import OutputManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedBillGenerator:
    """
    Enhanced Bill Generator with organized output management
    Features:
    - Date-based folder organization
    - Serial numbering for multiple runs per day
    - Comprehensive file management
    - Session tracking and metadata
    """
    
    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize Enhanced Bill Generator
        
        Args:
            base_output_dir: Base directory for organized outputs
        """
        self.output_manager = OutputManager(base_output_dir)
        logger.info("Enhanced Bill Generator initialized")
    
    def generate_complete_bill_package(self, 
                                     processed_data: Dict[str, Any],
                                     project_name: Optional[str] = None,
                                     contractor_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate complete bill package with organized output
        
        Args:
            processed_data: Processed data from Excel files
            project_name: Project name for organization
            contractor_name: Contractor name for organization
            
        Returns:
            Dictionary with generation results and file paths
        """
        logger.info("Starting complete bill package generation")
        
        # Extract project info from processed data if not provided
        if not project_name:
            project_name = processed_data.get('title', {}).get('project_name', 'Unknown Project')
        if not contractor_name:
            contractor_name = processed_data.get('title', {}).get('contractor_name', 'Unknown Contractor')
        
        # Create output session
        session_paths = self.output_manager.create_output_session(project_name, contractor_name)
        
        # Initialize results
        results = {
            'session_info': {
                'session_id': f"{session_paths['date']}_{session_paths['serial_number']:03d}",
                'project_name': project_name,
                'contractor_name': contractor_name,
                'created_at': datetime.now().isoformat(),
                'paths': session_paths
            },
            'html_files': {},
            'pdf_files': {},
            'excel_files': {},
            'errors': []
        }
        
        try:
            # Step 1: Generate HTML documents
            logger.info("Generating HTML documents...")
            generator = DocumentGenerator(processed_data)
            html_docs = generator.generate_all_html_documents()
            
            if html_docs:
                # Save HTML files
                saved_html = self.output_manager.save_html_files(session_paths, html_docs)
                results['html_files'] = saved_html
                logger.info(f"Generated {len(saved_html)} HTML documents")
            else:
                results['errors'].append("No HTML documents generated")
            
            # Step 2: Generate PDF documents
            logger.info("Generating PDF documents...")
            pdf_merger = PDFMerger()
            pdf_docs = pdf_merger.convert_html_to_pdf(html_docs)
            
            if pdf_docs:
                # Save PDF files
                saved_pdf = self.output_manager.save_pdf_files(session_paths, pdf_docs)
                results['pdf_files'] = saved_pdf
                logger.info(f"Generated {len(saved_pdf)} PDF documents")
            else:
                results['errors'].append("No PDF documents generated")
            
            # Step 3: Generate Excel documents
            logger.info("Generating Excel documents...")
            excel_docs = generator.generate_excel_outputs(processed_data)
            
            if excel_docs:
                # Save Excel files
                saved_excel = self.output_manager.save_excel_files(session_paths, excel_docs)
                results['excel_files'] = saved_excel
                logger.info(f"Generated {len(saved_excel)} Excel documents")
            else:
                results['errors'].append("No Excel documents generated")
            
            # Step 4: Generate session summary
            session_summary = self.output_manager.get_session_summary(session_paths)
            results['session_summary'] = session_summary
            
            # Log completion
            total_files = len(results['html_files']) + len(results['pdf_files']) + len(results['excel_files'])
            logger.info(f"Bill package generation completed successfully!")
            logger.info(f"Generated {total_files} files in session {results['session_info']['session_id']}")
            
            return results
            
        except Exception as e:
            error_msg = f"Error in bill package generation: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            return results
    
    def generate_extra_items_package(self,
                                   extra_items_data: Dict[str, Any],
                                   project_name: Optional[str] = None,
                                   contractor_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate extra items package with organized output
        
        Args:
            extra_items_data: Processed extra items data
            project_name: Project name for organization  
            contractor_name: Contractor name for organization
            
        Returns:
            Dictionary with generation results and file paths
        """
        logger.info("Starting extra items package generation")
        
        # Create session for extra items
        session_paths = self.output_manager.create_output_session(
            f"{project_name} - Extra Items" if project_name else "Extra Items",
            contractor_name
        )
        
        results = {
            'session_info': {
                'session_id': f"{session_paths['date']}_{session_paths['serial_number']:03d}",
                'type': 'extra_items',
                'project_name': project_name,
                'contractor_name': contractor_name,
                'created_at': datetime.now().isoformat(),
                'paths': session_paths
            },
            'html_files': {},
            'pdf_files': {},
            'errors': []
        }
        
        try:
            # Generate extra items HTML
            generator = DocumentGenerator(extra_items_data)
            extra_items_html = generator.generate_extra_items_statement()
            
            # Save HTML
            html_docs = {'extra_items_statement': extra_items_html}
            saved_html = self.output_manager.save_html_files(session_paths, html_docs)
            results['html_files'] = saved_html
            
            # Generate PDF
            pdf_merger = PDFMerger()
            pdf_docs = pdf_merger.convert_html_to_pdf(html_docs)
            
            if pdf_docs:
                saved_pdf = self.output_manager.save_pdf_files(session_paths, pdf_docs)
                results['pdf_files'] = saved_pdf
            
            logger.info(f"Extra items package generated: {results['session_info']['session_id']}")
            return results
            
        except Exception as e:
            error_msg = f"Error in extra items generation: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            return results
    
    def list_recent_outputs(self, days_back: int = 30) -> List[Dict]:
        """
        List recent output sessions
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of session information
        """
        return self.output_manager.list_sessions(days_back)
    
    def cleanup_old_outputs(self, days_to_keep: int = 90) -> Dict[str, Any]:
        """
        Clean up old output sessions
        
        Args:
            days_to_keep: Number of days to keep
            
        Returns:
            Cleanup summary
        """
        return self.output_manager.cleanup_old_sessions(days_to_keep)
    
    def get_output_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about output folder usage
        
        Returns:
            Statistics dictionary
        """
        base_dir = self.output_manager.base_dir
        
        if not base_dir.exists():
            return {'error': 'Output directory does not exist'}
        
        stats = {
            'base_directory': str(base_dir),
            'total_sessions': 0,
            'total_files': 0,
            'total_size_mb': 0.0,
            'by_type': {},
            'recent_sessions': []
        }
        
        # Calculate statistics
        total_size = 0
        total_files = 0
        total_sessions = 0
        
        for output_type in ['html', 'pdf', 'excel', 'logs']:
            type_dir = getattr(self.output_manager, f"{output_type}_dir")
            if type_dir.exists():
                type_files = list(type_dir.rglob('*'))
                type_file_count = len([f for f in type_files if f.is_file()])
                type_size = sum(f.stat().st_size for f in type_files if f.is_file())
                
                stats['by_type'][output_type] = {
                    'files': type_file_count,
                    'size_mb': round(type_size / (1024 * 1024), 2)
                }
                
                total_files += type_file_count
                total_size += type_size
                
                # Count sessions (only count once from html)
                if output_type == 'html':
                    for date_folder in type_dir.iterdir():
                        if date_folder.is_dir():
                            session_count = len([d for d in date_folder.iterdir() if d.is_dir() and d.name.startswith("serial_")])
                            total_sessions += session_count
        
        stats['total_sessions'] = total_sessions
        stats['total_files'] = total_files
        stats['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        # Get recent sessions
        stats['recent_sessions'] = self.list_recent_outputs(7)[:10]  # Last 10 sessions from past week
        
        return stats


def demo_enhanced_bill_generator():
    """
    Demo function showing how to use the Enhanced Bill Generator
    """
    print("🚀 ENHANCED BILL GENERATOR DEMO")
    print("=" * 60)
    
    # Initialize enhanced generator
    generator = EnhancedBillGenerator("outputs")
    
    # Sample data for demonstration
    sample_data = {
        'title': {
            'project_name': 'Construction of New Government Office Complex',
            'contractor_name': 'M/s Advanced Construction & Engineering Ltd.',
            'bill_number': 'BILL-2024-001',
            'agreement_no': 'AGR/2024/CONST/125'
        },
        'bill_quantity': [
            {
                'description': 'Excavation for foundation',
                'unit': 'Cum',
                'quantity': 1250.0,
                'rate': 125.50,
                'amount': 156875.0
            },
            {
                'description': 'Concrete work M25 grade',
                'unit': 'Cum',
                'quantity': 850.0,
                'rate': 4500.0,
                'amount': 3825000.0
            }
        ],
        'totals': {
            'grand_total': 3981875.0,
            'gst_amount': 716737.5,
            'total_with_gst': 4698612.5
        }
    }
    
    # Generate complete bill package
    print("📝 Generating complete bill package...")
    results = generator.generate_complete_bill_package(
        processed_data=sample_data,
        project_name="Government Office Complex",
        contractor_name="Advanced Construction Ltd."
    )
    
    # Display results
    if results['errors']:
        print("❌ Errors occurred:")
        for error in results['errors']:
            print(f"   - {error}")
    else:
        print("✅ Bill package generated successfully!")
        print(f"📁 Session ID: {results['session_info']['session_id']}")
        print(f"📊 Files generated:")
        print(f"   - HTML files: {len(results['html_files'])}")
        print(f"   - PDF files: {len(results['pdf_files'])}")
        print(f"   - Excel files: {len(results['excel_files'])}")
    
    # Show output statistics
    print(f"\n📊 OUTPUT STATISTICS:")
    stats = generator.get_output_statistics()
    print(f"   Total Sessions: {stats['total_sessions']}")
    print(f"   Total Files: {stats['total_files']}")
    print(f"   Total Size: {stats['total_size_mb']} MB")
    
    # List recent outputs
    print(f"\n📋 RECENT OUTPUTS:")
    recent = generator.list_recent_outputs(30)
    for session in recent[:5]:  # Show last 5
        print(f"   {session['date']} {session['serial']} - {session.get('project_name', 'Unknown')}")
    
    return results


if __name__ == "__main__":
    demo_enhanced_bill_generator()