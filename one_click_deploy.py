#!/usr/bin/env python3
"""
One-Click Deployment Script for BillGenerator Optimized
Handles Streamlit deployment with full automation and optimization
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil
import json
import time

def print_banner():
    """Print deployment banner"""
    print("🚀" * 35)
    print("🚀 BILLGENERATOR OPTIMIZED - ONE-CLICK DEPLOY 🚀")
    print("🚀" * 35)
    print("📦 Automated Streamlit Deployment System")
    print("👤 Developer: Rajkumar")
    print("📅 Date: September 2024")
    print("🚀" * 35)
    print()

def check_requirements():
    """Check deployment requirements"""
    print("🔍 Checking deployment requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {python_version.major}.{python_version.minor}")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if we're in the right directory
    if not Path('src/app.py').exists():
        print("❌ app.py not found. Please run from the project root directory.")
        return False
    print("✅ Project structure validated")
    
    # Check requirements.txt
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        return False
    print("✅ requirements.txt found")
    
    return True

def install_dependencies():
    """Install all required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      capture_output=True, check=True)
        print("✅ pip upgraded")
        
        # Install requirements
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All dependencies installed successfully")
            return True
        else:
            print("⚠️ Some dependencies failed to install:")
            print(result.stderr)
            
            # Try installing essential packages only
            essential_packages = [
                'streamlit>=1.28.0',
                'pandas>=2.0.0',
                'openpyxl>=3.1.0',
                'jinja2>=3.1.0',
                'reportlab>=4.0.0'
            ]
            
            print("\n🔧 Installing essential packages only...")
            for package in essential_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 capture_output=True, check=True)
                    print(f"✅ {package}")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def optimize_for_deployment():
    """Optimize application for deployment"""
    print("\n⚡ Optimizing for deployment...")
    
    # Create .streamlit directory for configuration
    streamlit_dir = Path('.streamlit')
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create Streamlit configuration
    config_content = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 50

[client]
showErrorDetails = true

[theme]
primaryColor = "#2E7D32"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#333333"

[browser]
gatherUsageStats = false
"""
    
    with open(streamlit_dir / 'config.toml', 'w') as f:
        f.write(config_content.strip())
    print("✅ Streamlit configuration created")
    
    # Create secrets.toml template
    secrets_content = """
# Add any secrets here
# Example:
# [database]
# host = "localhost"
# port = 5432
"""
    
    with open(streamlit_dir / 'secrets.toml', 'w') as f:
        f.write(secrets_content.strip())
    print("✅ Secrets template created")
    
    # Create .gitignore for deployment
    gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Streamlit
.streamlit/secrets.toml

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Output files
output/*.pdf
output/*.html
output/*.tex
output/*.zip

# Log files
logs/*.log

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~
"""
    
    if not Path('.gitignore').exists():
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ .gitignore created")
    
    return True

def validate_deployment():
    """Validate the deployment setup"""
    print("\n🧪 Validating deployment setup...")
    
    try:
        # Import Streamlit to verify it's installed
        import streamlit as st
        print("✅ Streamlit import successful")
        
        # Check if app.py can be imported
        sys.path.insert(0, 'src')
        
        # Test core imports
        from utils import safe_float_conversion
        from config import config
        from excel_processor import ExcelProcessor
        print("✅ Core modules import successful")
        
        # Validate configuration
        validation = config.validate_environment()
        if validation.get('valid', False):
            print("✅ Environment validation passed")
        else:
            print("⚠️ Environment validation warnings (non-critical)")
            if validation.get('warnings'):
                for warning in validation['warnings'][:3]:
                    print(f"   • {warning}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def create_deployment_files():
    """Create additional deployment files"""
    print("\n📄 Creating deployment files...")
    
    # Create Procfile for cloud deployment
    procfile_content = "web: streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0\n"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    print("✅ Procfile created for Heroku/cloud deployment")
    
    # Create runtime.txt for Python version specification
    python_version = f"python-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    with open('runtime.txt', 'w') as f:
        f.write(python_version)
    print(f"✅ runtime.txt created ({python_version})")
    
    # Create packages.txt for system dependencies
    packages_content = """
libgl1-mesa-glx
libglib2.0-0
libsm6
libxext6
libfontconfig1
libxrender1
libgomp1
"""
    with open('packages.txt', 'w') as f:
        f.write(packages_content.strip())
    print("✅ packages.txt created for system dependencies")
    
    # Create setup.sh for Streamlit Cloud
    setup_content = """#!/bin/bash

mkdir -p ~/.streamlit/

echo "\\
[general]\\n\\
email = \\"crajkumarsingh@hotmail.com\\"\\n\\
" > ~/.streamlit/credentials.toml

echo "\\
[server]\\n\\
headless = true\\n\\
enableCORS=false\\n\\
port = \\$PORT\\n\\
" > ~/.streamlit/config.toml
"""
    
    with open('setup.sh', 'w') as f:
        f.write(setup_content)
    
    # Make setup.sh executable on Unix systems
    if os.name != 'nt':
        os.chmod('setup.sh', 0o755)
    print("✅ setup.sh created for Streamlit Cloud")
    
    return True

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting BillGenerator Optimized...")
    
    try:
        # Check if port 8501 is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        
        if result == 0:
            print("⚠️ Port 8501 is already in use. Trying port 8502...")
            port = 8502
        else:
            port = 8501
        
        print(f"🌐 Starting on http://localhost:{port}")
        print("📖 Press Ctrl+C to stop the application")
        print("🎯 Upload an Excel file to test the system!")
        print()
        
        # Start Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'src/app.py',
            '--server.port', str(port),
            '--server.headless', 'false'
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Try running manually: streamlit run src/app.py")

def show_deployment_instructions():
    """Show deployment instructions for various platforms"""
    print("\n📚 DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    print("\n🔥 STREAMLIT CLOUD (Recommended):")
    print("1. Push this repository to GitHub")
    print("2. Go to https://share.streamlit.io")
    print("3. Connect your GitHub account")
    print("4. Select this repository")
    print("5. Set main file path: src/app.py")
    print("6. Deploy!")
    
    print("\n☁️ HEROKU DEPLOYMENT:")
    print("1. Install Heroku CLI")
    print("2. heroku create your-app-name")
    print("3. git push heroku main")
    print("4. heroku open")
    
    print("\n🐳 DOCKER DEPLOYMENT:")
    print("1. Create Dockerfile (template ready)")
    print("2. docker build -t billgenerator .")
    print("3. docker run -p 8501:8501 billgenerator")
    
    print("\n📱 LOCAL SHARING:")
    print("1. Run: streamlit run src/app.py --server.address 0.0.0.0")
    print("2. Share your local IP address")
    print("3. Others can access via http://YOUR_IP:8501")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment requirements not met!")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies!")
        return False
    
    # Optimize for deployment
    if not optimize_for_deployment():
        print("\n❌ Failed to optimize for deployment!")
        return False
    
    # Validate deployment
    if not validate_deployment():
        print("\n❌ Deployment validation failed!")
        return False
    
    # Create deployment files
    if not create_deployment_files():
        print("\n❌ Failed to create deployment files!")
        return False
    
    print("\n" + "🎉" * 25)
    print("🎉 DEPLOYMENT SETUP COMPLETE! 🎉")
    print("🎉" * 25)
    
    # Ask user what they want to do
    print("\n🤔 What would you like to do?")
    print("1. Start the application locally")
    print("2. Show deployment instructions")
    print("3. Exit")
    
    choice = input("\n👉 Enter your choice (1-3): ").strip()
    
    if choice == '1':
        start_application()
    elif choice == '2':
        show_deployment_instructions()
    else:
        print("\n👋 Deployment setup complete! Ready for production.")
        print("💡 Run 'streamlit run src/app.py' to start the application")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Deployment setup failed!")
            input("Press Enter to exit...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
