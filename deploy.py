#!/usr/bin/env python3
"""
Deployment script for BillGenerator Optimized
Handles installation, setup, and launch of the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil
import json
from datetime import datetime

def print_banner():
    """Print deployment banner"""
    print("=" * 70)
    print("🚀 BILLGENERATOR OPTIMIZED - DEPLOYMENT SCRIPT")
    print("=" * 70)
    print("📦 Version: 1.0.0 (Production)")
    print("👤 Developer: Rajkumar")
    print("📅 Date: September 2024")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    
    if version < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True

def check_system_requirements():
    """Check system requirements"""
    print("\n🖥️  Checking system requirements...")
    
    # Check OS
    os_name = platform.system()
    print(f"   Operating System: {os_name} {platform.release()}")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"   Available RAM: {memory_gb:.1f} GB")
        
        if memory_gb < 4:
            print("⚠️  Warning: Less than 4GB RAM detected. Performance may be affected.")
    except ImportError:
        print("   Could not check memory (psutil not available)")
    
    # Check disk space
    try:
        disk_usage = shutil.disk_usage('.')
        free_gb = disk_usage.free / (1024**3)
        print(f"   Available disk space: {free_gb:.1f} GB")
        
        if free_gb < 2:
            print("❌ Error: Less than 2GB disk space available")
            return False
    except Exception as e:
        print(f"   Could not check disk space: {e}")
    
    print("✅ System requirements check completed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if requirements.txt exists
        requirements_file = Path('requirements.txt')
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        # Install dependencies
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        'templates',
        'assets',
        'output',
        'logs',
        'tests',
        'Input_Files_for_tests'
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   Created: {directory}")
            except Exception as e:
                print(f"   ❌ Error creating {directory}: {e}")
                return False
        else:
            print(f"   ✅ Exists: {directory}")
    
    return True

def validate_installation():
    """Validate the installation"""
    print("\n🔍 Validating installation...")
    
    try:
        # Add src to path
        sys.path.insert(0, 'src')
        
        # Test imports
        from utils import safe_float_conversion, format_currency
        from config import config
        from excel_processor import ExcelProcessor
        
        # Test basic functionality
        assert safe_float_conversion('1000') == 1000.0
        assert format_currency(1000) == '₹1,000.00'
        assert config.APP_NAME == 'BillGenerator Optimized'
        
        # Test processor initialization
        processor = ExcelProcessor()
        assert processor is not None
        
        print("✅ Installation validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Installation validation failed: {e}")
        return False

def create_launch_scripts():
    """Create platform-specific launch scripts"""
    print("\n🚀 Creating launch scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting BillGenerator Optimized...
cd /d "%~dp0"
python -m streamlit run src/app.py --server.headless false --server.port 8501
pause
"""
    
    try:
        with open('run_billgenerator.bat', 'w') as f:
            f.write(windows_script)
        print("   ✅ Created: run_billgenerator.bat (Windows)")
    except Exception as e:
        print(f"   ❌ Error creating Windows script: {e}")
    
    # Unix/Linux shell script
    unix_script = """#!/bin/bash
echo "Starting BillGenerator Optimized..."
cd "$(dirname "$0")"
python3 -m streamlit run src/app.py --server.headless false --server.port 8501
"""
    
    try:
        with open('run_billgenerator.sh', 'w') as f:
            f.write(unix_script)
        
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod('run_billgenerator.sh', 0o755)
        
        print("   ✅ Created: run_billgenerator.sh (Unix/Linux/macOS)")
    except Exception as e:
        print(f"   ❌ Error creating Unix script: {e}")

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if os.name == 'nt':
        print("\n🖥️  Creating desktop shortcut...")
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "BillGenerator Optimized.lnk")
            target = os.path.join(os.getcwd(), "run_billgenerator.bat")
            wdir = os.getcwd()
            icon = target
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wdir
            shortcut.IconLocation = icon
            shortcut.save()
            
            print("   ✅ Desktop shortcut created")
        except ImportError:
            print("   ⚠️  Could not create desktop shortcut (winshell not available)")
        except Exception as e:
            print(f"   ⚠️  Could not create desktop shortcut: {e}")

def save_deployment_config():
    """Save deployment configuration"""
    print("\n💾 Saving deployment configuration...")
    
    config_data = {
        "app_name": "BillGenerator Optimized",
        "version": "1.0.0",
        "deployment_date": str(datetime.now()),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.platform(),
        "developer": "Rajkumar"
    }
    
    try:
        with open('deployment_config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        print("   ✅ Deployment configuration saved")
    except Exception as e:
        print(f"   ❌ Error saving deployment config: {e}")

def launch_application():
    """Launch the application"""
    print("\n🚀 Launching BillGenerator Optimized...")
    
    try:
        # Change to app directory if needed
        app_path = Path('src/app.py')
        if app_path.exists():
            subprocess.Popen([
                sys.executable, '-m', 'streamlit', 'run', 'src/app.py',
                '--server.headless', 'false',
                '--server.port', '8501'
            ])
            print("✅ Application launched successfully!")
            print("\n🌐 Application will open in your default web browser")
            print("📍 URL: http://localhost:8501")
            print("\n📖 For help and documentation, see README_RAJKUMAR.md")
            return True
        else:
            print("❌ Application file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False

def main():
    """Main deployment function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        return False
    
    if not check_system_requirements():
        return False
    
    # Install and setup
    if not install_dependencies():
        print("\n❌ Deployment failed at dependency installation")
        return False
    
    if not create_directories():
        print("\n❌ Deployment failed at directory creation")
        return False
    
    if not validate_installation():
        print("\n❌ Deployment failed at validation")
        return False
    
    # Create deployment artifacts
    create_launch_scripts()
    create_desktop_shortcut()
    save_deployment_config()
    
    print("\n" + "=" * 70)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    # Ask user if they want to launch the app
    launch_now = input("\n🚀 Launch BillGenerator Optimized now? (y/n): ").lower().strip()
    if launch_now in ['y', 'yes', '1', 'true']:
        launch_application()
    else:
        print("\n📋 To launch later:")
        if os.name == 'nt':
            print("   Windows: Double-click run_billgenerator.bat")
        print("   Or run: python -m streamlit run src/app.py")
    
    print("\n💡 Tips:")
    print("   • Check README_RAJKUMAR.md for complete documentation")
    print("   • Use test files in Input_Files_for_tests/ folder")
    print("   • Generated documents will be saved in output/ folder")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\n❌ Deployment failed. Press Enter to exit...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during deployment: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
