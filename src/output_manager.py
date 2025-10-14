"""
Output Manager for Bill Generator
Creates organized folder structure with date-based directories and serial numbering
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import shutil

logger = logging.getLogger(__name__)

class OutputManager:
    """
    Manages output file organization with date-based folder structure
    Features:
    - Date-based folder creation (YYYY-MM-DD format)
    - Serial numbering for multiple outputs on same date
    - Metadata tracking for each output session
    - Automatic cleanup of old outputs (configurable)
    """
    
    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize OutputManager
        
        Args:
            base_output_dir: Base directory for all outputs (default: "outputs")
        """
        self.base_dir = Path(base_output_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.html_dir = self.base_dir / "html"
        self.pdf_dir = self.base_dir / "pdf"
        self.excel_dir = self.base_dir / "excel"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure all directories exist
        for directory in [self.html_dir, self.pdf_dir, self.excel_dir, self.logs_dir]:
            directory.mkdir(exist_ok=True)
        
        logger.info(f"OutputManager initialized with base directory: {self.base_dir}")
    
    def get_date_folder(self, output_type: str, date: Optional[datetime] = None) -> Path:
        """
        Get or create date-based folder for specified output type
        
        Args:
            output_type: Type of output ('html', 'pdf', 'excel', 'logs')
            date: Date for folder (default: today)
            
        Returns:
            Path to date folder
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y-%m-%d")
        
        # Map output type to base directory
        type_mapping = {
            'html': self.html_dir,
            'pdf': self.pdf_dir,
            'excel': self.excel_dir,
            'logs': self.logs_dir
        }
        
        if output_type not in type_mapping:
            raise ValueError(f"Invalid output type: {output_type}")
        
        date_folder = type_mapping[output_type] / date_str
        date_folder.mkdir(exist_ok=True)
        
        return date_folder
    
    def get_next_serial_number(self, date_folder: Path) -> int:
        """
        Get next available serial number for the date folder
        
        Args:
            date_folder: Path to date folder
            
        Returns:
            Next serial number
        """
        if not date_folder.exists():
            return 1
        
        # Find existing serial numbers
        existing_serials = []
        for item in date_folder.iterdir():
            if item.is_dir() and item.name.startswith("serial_"):
                try:
                    serial_num = int(item.name.split("_")[1])
                    existing_serials.append(serial_num)
                except (IndexError, ValueError):
                    continue
        
        return max(existing_serials, default=0) + 1
    
    def create_output_session(self, project_name: Optional[str] = None, contractor_name: Optional[str] = None) -> Dict[str, Path]:
        """
        Create a new output session with organized folder structure
        
        Args:
            project_name: Name of the project (for metadata)
            contractor_name: Name of contractor (for metadata)
            
        Returns:
            Dictionary with paths for each output type
        """
        current_time = datetime.now()
        
        # Create date folders for each output type
        html_date_folder = self.get_date_folder('html', current_time)
        pdf_date_folder = self.get_date_folder('pdf', current_time)
        excel_date_folder = self.get_date_folder('excel', current_time)
        logs_date_folder = self.get_date_folder('logs', current_time)
        
        # Get serial numbers (use same serial for all types in one session)
        serial_number = self.get_next_serial_number(html_date_folder)
        serial_folder_name = f"serial_{serial_number:03d}"
        
        # Create serial folders
        session_paths = {
            'html': html_date_folder / serial_folder_name,
            'pdf': pdf_date_folder / serial_folder_name,
            'excel': excel_date_folder / serial_folder_name,
            'logs': logs_date_folder / serial_folder_name,
            'serial_number': serial_number,
            'date': current_time.strftime("%Y-%m-%d"),
            'time': current_time.strftime("%H-%M-%S")
        }
        
        # Create all session directories
        for output_type in ['html', 'pdf', 'excel', 'logs']:
            session_paths[output_type].mkdir(exist_ok=True)
        
        # Create session metadata
        metadata = {
            'session_id': f"{current_time.strftime('%Y%m%d')}_{serial_number:03d}",
            'created_at': current_time.isoformat(),
            'project_name': project_name or "Unknown Project",
            'contractor_name': contractor_name or "Unknown Contractor",
            'serial_number': serial_number,
            'folder_structure': {
                'html': str(session_paths['html']),
                'pdf': str(session_paths['pdf']),
                'excel': str(session_paths['excel']),
                'logs': str(session_paths['logs'])
            }
        }
        
        # Save metadata
        metadata_file = session_paths['logs'] / "session_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created output session: {metadata['session_id']}")
        logger.info(f"Project: {project_name}, Contractor: {contractor_name}")
        
        return session_paths
    
    def save_html_files(self, session_paths: Dict[str, Path], html_docs: Dict[str, str]) -> Dict[str, str]:
        """
        Save HTML files to session folder
        
        Args:
            session_paths: Session paths from create_output_session
            html_docs: Dictionary of HTML documents {name: content}
            
        Returns:
            Dictionary of saved file paths
        """
        saved_files = {}
        html_folder = session_paths['html']
        
        for doc_name, html_content in html_docs.items():
            # Sanitize filename
            safe_filename = self._sanitize_filename(doc_name)
            file_path = html_folder / f"{safe_filename}.html"
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                saved_files[doc_name] = str(file_path)
                logger.info(f"Saved HTML: {file_path}")
                
            except Exception as e:
                logger.error(f"Error saving HTML file {doc_name}: {str(e)}")
        
        return saved_files
    
    def save_pdf_files(self, session_paths: Dict[str, Path], pdf_docs: Dict[str, bytes]) -> Dict[str, str]:
        """
        Save PDF files to session folder
        
        Args:
            session_paths: Session paths from create_output_session
            pdf_docs: Dictionary of PDF documents {name: bytes}
            
        Returns:
            Dictionary of saved file paths
        """
        saved_files = {}
        pdf_folder = session_paths['pdf']
        
        for doc_name, pdf_content in pdf_docs.items():
            # Sanitize filename
            safe_filename = self._sanitize_filename(doc_name)
            file_path = pdf_folder / f"{safe_filename}.pdf"
            
            try:
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                
                saved_files[doc_name] = str(file_path)
                logger.info(f"Saved PDF: {file_path}")
                
            except Exception as e:
                logger.error(f"Error saving PDF file {doc_name}: {str(e)}")
        
        return saved_files
    
    def save_excel_files(self, session_paths: Dict[str, Path], excel_docs: Dict[str, bytes]) -> Dict[str, str]:
        """
        Save Excel files to session folder
        
        Args:
            session_paths: Session paths from create_output_session
            excel_docs: Dictionary of Excel documents {name: bytes}
            
        Returns:
            Dictionary of saved file paths
        """
        saved_files = {}
        excel_folder = session_paths['excel']
        
        for doc_name, excel_content in excel_docs.items():
            # Sanitize filename
            safe_filename = self._sanitize_filename(doc_name)
            file_path = excel_folder / f"{safe_filename}.xlsx"
            
            try:
                with open(file_path, 'wb') as f:
                    f.write(excel_content)
                
                saved_files[doc_name] = str(file_path)
                logger.info(f"Saved Excel: {file_path}")
                
            except Exception as e:
                logger.error(f"Error saving Excel file {doc_name}: {str(e)}")
        
        return saved_files
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to remove invalid characters
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove multiple consecutive underscores
        while '__' in filename:
            filename = filename.replace('__', '_')
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        return filename
    
    def get_session_summary(self, session_paths: Dict[str, Path]) -> Dict:
        """
        Get summary information about a session
        
        Args:
            session_paths: Session paths from create_output_session
            
        Returns:
            Session summary dictionary
        """
        summary = {
            'session_info': {},
            'file_counts': {},
            'file_sizes': {},
            'total_files': 0,
            'total_size_mb': 0
        }
        
        # Load metadata if available
        metadata_file = session_paths['logs'] / "session_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    summary['session_info'] = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load session metadata: {str(e)}")
        
        # Count files and calculate sizes
        total_size = 0
        total_files = 0
        
        for output_type in ['html', 'pdf', 'excel']:
            folder = session_paths[output_type]
            if folder.exists():
                files = list(folder.glob('*'))
                file_count = len([f for f in files if f.is_file()])
                folder_size = sum(f.stat().st_size for f in files if f.is_file())
                
                summary['file_counts'][output_type] = file_count
                summary['file_sizes'][output_type] = folder_size
                
                total_files += file_count
                total_size += folder_size
        
        summary['total_files'] = total_files
        summary['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return summary
    
    def list_sessions(self, days_back: int = 30) -> List[Dict]:
        """
        List recent sessions within specified days
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of session information
        """
        sessions = []
        current_date = datetime.now()
        
        # Search through date folders
        for output_type in ['html']:  # Use html as reference since all types should have same sessions
            type_folder = getattr(self, f"{output_type}_dir")
            
            for date_folder in type_folder.iterdir():
                if not date_folder.is_dir():
                    continue
                
                try:
                    # Parse date from folder name
                    folder_date = datetime.strptime(date_folder.name, "%Y-%m-%d")
                    days_diff = (current_date - folder_date).days
                    
                    if days_diff <= days_back:
                        # Find serial folders
                        for serial_folder in date_folder.iterdir():
                            if serial_folder.is_dir() and serial_folder.name.startswith("serial_"):
                                # Look for metadata
                                metadata_file = self.logs_dir / date_folder.name / serial_folder.name / "session_metadata.json"
                                
                                session_info = {
                                    'date': date_folder.name,
                                    'serial': serial_folder.name,
                                    'path': str(serial_folder),
                                    'days_ago': days_diff
                                }
                                
                                if metadata_file.exists():
                                    try:
                                        with open(metadata_file, 'r', encoding='utf-8') as f:
                                            metadata = json.load(f)
                                            session_info.update(metadata)
                                    except Exception as e:
                                        logger.warning(f"Could not load metadata for {serial_folder}: {str(e)}")
                                
                                sessions.append(session_info)
                
                except ValueError:
                    # Skip folders that don't match date format
                    continue
        
        # Sort by date and serial number (newest first)
        sessions.sort(key=lambda x: (x['date'], x.get('serial_number', 0)), reverse=True)
        
        return sessions
    
    def cleanup_old_sessions(self, days_to_keep: int = 90) -> Dict[str, int]:
        """
        Clean up old sessions beyond specified days
        
        Args:
            days_to_keep: Number of days to keep (default: 90)
            
        Returns:
            Cleanup summary
        """
        cleanup_summary = {
            'sessions_removed': 0,
            'files_removed': 0,
            'space_freed_mb': 0.0
        }
        
        current_date = datetime.now()
        
        # Clean up each output type
        for output_type in ['html', 'pdf', 'excel', 'logs']:
            type_folder = getattr(self, f"{output_type}_dir")
            
            for date_folder in type_folder.iterdir():
                if not date_folder.is_dir():
                    continue
                
                try:
                    # Parse date from folder name
                    folder_date = datetime.strptime(date_folder.name, "%Y-%m-%d")
                    days_diff = (current_date - folder_date).days
                    
                    if days_diff > days_to_keep:
                        # Calculate size before deletion
                        folder_size = sum(f.stat().st_size for f in date_folder.rglob('*') if f.is_file())
                        file_count = len([f for f in date_folder.rglob('*') if f.is_file()])
                        
                        # Remove the entire date folder
                        shutil.rmtree(date_folder)
                        
                        cleanup_summary['files_removed'] += file_count
                        cleanup_summary['space_freed_mb'] += float(folder_size) / (1024 * 1024)
                        
                        if output_type == 'html':  # Count sessions only once
                            cleanup_summary['sessions_removed'] += len([d for d in date_folder.iterdir() if d.is_dir() and d.name.startswith("serial_")])
                        
                        logger.info(f"Cleaned up old {output_type} folder: {date_folder}")
                
                except ValueError:
                    # Skip folders that don't match date format
                    continue
        
        cleanup_summary['space_freed_mb'] = round(float(cleanup_summary['space_freed_mb']), 2)
        
        logger.info(f"Cleanup completed: {cleanup_summary}")
        return cleanup_summary