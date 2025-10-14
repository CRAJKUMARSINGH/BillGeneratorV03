"""
Configuration management for BillGenerator Optimized
Centralized configuration with environment-specific settings
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import tempfile

class Config:
    """
    Centralized configuration management
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from environment and defaults"""
        
        # Application Settings
        self.APP_NAME = "BillGenerator Optimized"
        self.APP_VERSION = "1.0.0"
        self.APP_DESCRIPTION = "Professional Infrastructure Billing Document Generator"
        
        # File Processing Settings
        self.MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '50'))
        self.SUPPORTED_FORMATS = ['xlsx', 'xls']
        self.CHUNK_SIZE = 1000
        
        # PDF Generation Settings
        self.PDF_PAGE_SIZE = 'A4'
        self.PDF_MARGIN = '20mm'
        self.PDF_ORIENTATION = 'portrait'
        self.PDF_DPI = 300
        
        # LaTeX Settings
        self.LATEX_ENGINE = os.getenv('LATEX_ENGINE', 'pdflatex')
        self.LATEX_TIMEOUT = int(os.getenv('LATEX_TIMEOUT', '30'))
        self.LATEX_ENABLED = self._check_latex_availability()
        
        # Directory Structure
        self.setup_directories()
        
        # Document Templates
        self.setup_templates()
        
        # UI Settings
        self.setup_ui_config()
        
        # Logging Configuration
        self.setup_logging()
        
        # Processing Settings
        self.setup_processing_config()
        
        # Security Settings
        self.setup_security_config()
    
    def setup_directories(self):
        """Setup directory structure"""
        self.DIRS = {
            'base': self.base_dir,
            'src': self.base_dir / 'src',
            'templates': self.base_dir / 'templates',
            'assets': self.base_dir / 'assets',
            'output': self.base_dir / 'output',
            'temp': Path(tempfile.gettempdir()) / 'billgenerator',
            'logs': self.base_dir / 'logs',
            'tests': self.base_dir / 'tests',
            'input_samples': self.base_dir / 'Input_Files_for_tests'
        }
        
        # Create directories if they don't exist
        for dir_path in self.DIRS.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def setup_templates(self):
        """Setup template configuration"""
        self.TEMPLATES = {
            'latex': {
                'first_page_summary': 'first_page_summary.tex',
                'deviation_statement': 'deviation_statement.tex',
                'bill_scrutiny': 'bill_scrutiny.tex',
                'extra_items_statement': 'extra_items_statement.tex',
                'certificate_ii': 'certificate_ii.tex',
                'certificate_iii': 'certificate_iii.tex'
            },
            'html': {
                'summary_report': 'summary_report.html',
                'detailed_bill': 'detailed_bill.html',
                'progress_report': 'progress_report.html'
            }
        }
    
    def setup_ui_config(self):
        """Setup UI configuration"""
        self.UI = {
            'theme': {
                'primary_color': '#2E7D32',
                'background_color': '#FFFFFF',
                'secondary_background': '#F5F5F5',
                'text_color': '#333333',
                'success_color': '#4CAF50',
                'warning_color': '#FF9800',
                'error_color': '#F44336',
                'info_color': '#2196F3'
            },
            'layout': {
                'sidebar_width': 300,
                'main_width': 800,
                'max_width': 1200,
                'padding': '1rem'
            },
            'fonts': {
                'header_font': 'Arial, sans-serif',
                'body_font': 'Roboto, sans-serif',
                'code_font': 'Courier New, monospace'
            },
            'icons': {
                'upload': '📁',
                'process': '⚙️',
                'download': '💾',
                'success': '✅',
                'warning': '⚠️',
                'error': '❌',
                'info': 'ℹ️'
            }
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        self.LOGGING = {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file_handler': {
                'enabled': True,
                'filename': self.DIRS['logs'] / 'billgenerator.log',
                'max_bytes': 10 * 1024 * 1024,  # 10MB
                'backup_count': 5
            },
            'console_handler': {
                'enabled': True,
                'colored': True
            }
        }
    
    def setup_processing_config(self):
        """Setup data processing configuration"""
        self.PROCESSING = {
            'excel': {
                'sheet_detection': {
                    'title_keywords': ['title', 'cover', 'front', 'project', 'header'],
                    'work_order_keywords': ['work order', 'work_order', 'workorder', 'wo', 'order'],
                    'bill_quantity_keywords': ['bill quantity', 'bill_quantity', 'billquantity', 'bq', 'quantity', 'bill'],
                    'extra_items_keywords': ['extra items', 'extra_items', 'extraitems', 'extra', 'additional']
                },
                'column_mapping': {
                    'flexible_matching': True,
                    'fuzzy_threshold': 0.8,
                    'required_columns': {
                        'item_description': ['description', 'item', 'work description', 'particulars'],
                        'quantity': ['quantity', 'qty', 'nos', 'number'],
                        'unit': ['unit', 'uom', 'unit of measurement'],
                        'rate': ['rate', 'unit rate', 'cost', 'price'],
                        'amount': ['amount', 'total', 'value', 'cost']
                    }
                },
                'validation': {
                    'max_rows': 10000,
                    'min_rows': 1,
                    'required_sheets': ['title', 'work_order', 'bill_quantity'],
                    'numeric_precision': 2
                }
            },
            'calculations': {
                'gst_rate': 18.0,
                'rounding_precision': 2,
                'rounding_method': 'standard',  # 'standard', 'up', 'down', 'even'
                'currency_symbol': '₹',
                'number_format': 'indian'  # 'indian', 'international'
            }
        }
    
    def setup_security_config(self):
        """Setup security configuration"""
        self.SECURITY = {
            'file_validation': {
                'virus_scan': False,  # Requires additional tools
                'file_type_validation': True,
                'content_validation': True,
                'size_limits': True
            },
            'data_sanitization': {
                'remove_scripts': True,
                'escape_html': True,
                'validate_formulas': True
            },
            'temporary_files': {
                'auto_cleanup': True,
                'cleanup_interval': 3600,  # seconds
                'max_age': 86400  # 24 hours in seconds
            }
        }
    
    def _check_latex_availability(self) -> bool:
        """Check if LaTeX is available on the system"""
        try:
            import subprocess
            result = subprocess.run(
                [self.LATEX_ENGINE, '--version'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False
    
    def get_template_path(self, template_type: str, template_name: str) -> Path:
        """Get full path to template file"""
        if template_type in self.TEMPLATES:
            template_file = self.TEMPLATES[template_type].get(template_name)
            if template_file:
                return self.DIRS['templates'] / template_file
        return None
    
    def get_dated_output_path(self, serial_number: Optional[str] = None) -> Path:
        """Get full path for dated output folder with serial number"""
        from datetime import datetime
        date_str = datetime.now().strftime("%d%m%Y")
        
        if serial_number:
            folder_name = f"output_{serial_number}_{date_str}"
        else:
            folder_name = f"output_01_{date_str}"
        
        dated_path = self.DIRS['output'] / folder_name
        dated_path.mkdir(parents=True, exist_ok=True)
        return dated_path
    
    def get_output_path(self, filename: str, serial_number: Optional[str] = None) -> Path:
        """Get full path for output file in dated folder"""
        dated_path = self.get_dated_output_path(serial_number)
        return dated_path / filename
    
    def get_temp_path(self, filename: str) -> Path:
        """Get full path for temporary file"""
        return self.DIRS['temp'] / filename
    
    def update_config(self, section: str, key: str, value: Any) -> bool:
        """Update configuration value"""
        try:
            if hasattr(self, section.upper()):
                config_section = getattr(self, section.upper())
                if isinstance(config_section, dict) and key in config_section:
                    config_section[key] = value
                    return True
            return False
        except Exception as e:
            logging.error(f"Error updating configuration: {str(e)}")
            return False
    
    def get_config(self, section: str, key: str = None, default: Any = None) -> Any:
        """Get configuration value"""
        try:
            if hasattr(self, section.upper()):
                config_section = getattr(self, section.upper())
                if key is None:
                    return config_section
                elif isinstance(config_section, dict):
                    return config_section.get(key, default)
            return default
        except Exception:
            return default
    
    def save_config(self, filepath: str = None) -> bool:
        """Save current configuration to file"""
        try:
            if filepath is None:
                filepath = self.DIRS['base'] / 'config.json'
            
            config_data = {
                'APP_NAME': self.APP_NAME,
                'APP_VERSION': self.APP_VERSION,
                'MAX_FILE_SIZE_MB': self.MAX_FILE_SIZE_MB,
                'LATEX_ENABLED': self.LATEX_ENABLED,
                'UI': self.UI,
                'PROCESSING': self.PROCESSING,
                'SECURITY': self.SECURITY
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            logging.error(f"Error saving configuration: {str(e)}")
            return False
    
    def load_config_file(self, filepath: str) -> bool:
        """Load configuration from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Update configuration with loaded data
            for section, values in config_data.items():
                if hasattr(self, section):
                    if isinstance(values, dict) and hasattr(self, section):
                        current_section = getattr(self, section)
                        if isinstance(current_section, dict):
                            current_section.update(values)
                    else:
                        setattr(self, section, values)
            
            return True
        except Exception as e:
            logging.error(f"Error loading configuration file: {str(e)}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information for diagnostics"""
        try:
            import platform
            import sys
            import psutil
            
            return {
                'platform': platform.platform(),
                'python_version': sys.version,
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'disk_usage': psutil.disk_usage('/').free if os.name != 'nt' else psutil.disk_usage('C:\\').free,
                'latex_available': self.LATEX_ENABLED,
                'app_version': self.APP_VERSION
            }
        except Exception as e:
            logging.error(f"Error getting system info: {str(e)}")
            return {}
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate the current environment"""
        validation = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'info': []
        }
        
        try:
            # Check required directories
            for name, path in self.DIRS.items():
                if not path.exists():
                    validation['warnings'].append(f"Directory missing: {name} ({path})")
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        validation['info'].append(f"Created directory: {name}")
                    except Exception as e:
                        validation['errors'].append(f"Cannot create directory {name}: {str(e)}")
                        validation['valid'] = False
            
            # Check disk space
            try:
                import shutil
                free_space = shutil.disk_usage(self.DIRS['base']).free
                if free_space < 100 * 1024 * 1024:  # Less than 100MB
                    validation['warnings'].append(f"Low disk space: {free_space / 1024 / 1024:.1f}MB available")
            except Exception:
                validation['warnings'].append("Could not check disk space")
            
            # Check memory
            try:
                import psutil
                available_memory = psutil.virtual_memory().available
                if available_memory < 500 * 1024 * 1024:  # Less than 500MB
                    validation['warnings'].append(f"Low memory: {available_memory / 1024 / 1024:.1f}MB available")
            except Exception:
                validation['warnings'].append("Could not check memory usage")
            
            # Check LaTeX installation
            if not self.LATEX_ENABLED:
                validation['info'].append("LaTeX not available - will use fallback PDF generation")
            
        except Exception as e:
            validation['errors'].append(f"Environment validation error: {str(e)}")
            validation['valid'] = False
        
        return validation

# Global configuration instance
config = Config()
