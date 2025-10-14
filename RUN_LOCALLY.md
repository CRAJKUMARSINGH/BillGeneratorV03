# 🏗️ Infrastructure Billing System - Local Setup Guide

## 📋 Complete Local Development Setup

This guide provides step-by-step instructions to run the Infrastructure Billing System locally on your Windows machine.

## 🔍 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.8+ (Recommended: 3.9 or 3.10)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free space
- **Internet**: Required for initial setup and dependencies

### Optional (for Enhanced Features)
- **LaTeX Distribution**: MiKTeX or TeX Live (for professional PDF generation)
- **Git**: For version control
- **Visual Studio Code**: Recommended IDE

## 📦 Dependencies Overview

### Core Python Packages
```
streamlit>=1.28.0              # Main web framework
pandas>=2.0.0                  # Data processing
openpyxl>=3.1.0               # Excel file handling
jinja2>=3.1.0                 # Template processing
reportlab>=4.0.0              # PDF generation
PyPDF2>=3.0.0                 # PDF manipulation
python-dateutil>=2.8.0        # Date processing
```

### Additional Dependencies
```
numpy>=1.24.0                 # Numerical computing
xlsxwriter>=3.1.0             # Excel writing
Pillow>=10.0.0                # Image processing
coloredlogs>=15.0             # Enhanced logging
plotly>=5.15.0                # Data visualization
requests>=2.31.0              # HTTP requests
cryptography>=41.0.0          # Security
python-dotenv>=1.0.0          # Environment variables
```

## 🚀 Step-by-Step Installation

### Step 1: Python Environment Setup

1. **Download Python**
   - Visit https://python.org/downloads/
   - Download Python 3.9+ for Windows
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Check "Install pip"

2. **Verify Installation**
   ```powershell
   python --version
   pip --version
   ```

### Step 2: Project Setup

1. **Clone or Download Project**
   ```powershell
   # Option A: Using Git
   git clone https://github.com/CRAJKUMARSINGH/BillGeneratorV03.git
   cd BillGeneratorV03
   
   # Option B: Download ZIP from GitHub and extract
   ```

2. **Navigate to Project Directory**
   ```powershell
   cd c:\Users\Rajkumar\BillGeneratorV03
   ```

### Step 3: Virtual Environment (Recommended)

1. **Create Virtual Environment**
   ```powershell
   python -m venv billgenerator_env
   ```

2. **Activate Virtual Environment**
   ```powershell
   # Windows PowerShell
   .\billgenerator_env\Scripts\Activate.ps1
   
   # Windows CMD
   billgenerator_env\Scripts\activate.bat
   ```

3. **Upgrade pip**
   ```powershell
   python -m pip install --upgrade pip
   ```

### Step 4: Install Dependencies

1. **Install All Requirements**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```powershell
   pip list
   ```

### Step 5: Environment Configuration

1. **Create .env file** (see Environment Setup section)
2. **Configure directories** - Application will auto-create needed folders

## 🔧 Environment Setup

### Required Environment Variables

Create a `.env` file in the project root:

```env
# Application Settings
APP_NAME=Infrastructure Billing System
APP_VERSION=3.0
MAX_FILE_SIZE_MB=50

# Processing Settings
LATEX_ENGINE=pdflatex
LATEX_TIMEOUT=30
LOG_LEVEL=INFO

# PDF Settings
PDF_PAGE_SIZE=A4
PDF_MARGIN=10mm
PDF_ORIENTATION=portrait
PDF_DPI=300

# Security Settings
SESSION_SECRET=your_secure_session_secret_here_change_this
```

## ▶️ Running the Application

### Option 1: Main Streamlit App (Full Features)
```powershell
streamlit run src/app.py
```

### Option 2: Cloud-Compatible Version
```powershell
streamlit run streamlit_app.py
```

### Option 3: Enhanced Version (if available)
```powershell
streamlit run src/enhanced_app.py
```

### Access the Application
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

## 🧪 Testing the Application

### Quick Functionality Test
1. Open the application in your browser
2. Check if the upload interface loads
3. Try uploading a sample Excel file (create one if needed)
4. Verify basic processing works

### Comprehensive Testing
```powershell
# Run test suite
python -m pytest tests/ -v

# Run specific test
python tests/test_comprehensive.py

# Run performance tests
python tests/test_performance.py
```

## 📁 Directory Structure

```
BillGeneratorV03/
├── src/                      # Core application modules
│   ├── app.py               # Main Streamlit application
│   ├── excel_processor.py   # Excel file processing
│   ├── latex_generator.py   # LaTeX document generation
│   ├── pdf_merger.py        # PDF processing
│   ├── utils.py             # Utility functions
│   └── config.py            # Configuration management
├── templates/               # Document templates
│   ├── *.html              # HTML templates
│   └── *.tex               # LaTeX templates
├── tests/                   # Test files
├── assets/                  # Static assets
├── output/                  # Generated documents (auto-created)
├── logs/                    # Application logs (auto-created)
├── requirements.txt         # Python dependencies
├── streamlit_app.py        # Cloud-compatible version
├── .env                    # Environment variables (create this)
└── .gitignore              # Git ignore file (create this)
```

## 🔧 Configuration Options

### Streamlit Configuration
Create `.streamlit/config.toml` for custom Streamlit settings:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 📊 Input File Requirements

### Excel File Structure
Your Excel file must contain these sheets:

1. **Title Sheet**
   - Project name, contractor details
   - Agreement information
   - Dates and locations

2. **Work Order Sheet**
   - Original planned work items
   - Quantities and rates
   - Item descriptions

3. **Bill Quantity Sheet**
   - Actual completed work
   - Final quantities and amounts
   - Bill calculations

4. **Extra Items Sheet** (Optional)
   - Additional work not in original plan
   - Extra quantities and rates

### Sample Input Files
- Check `Input_Files_for_tests/` directory for sample files
- Use these for testing and understanding format requirements

## ⚡ Performance Optimization

### For Large Files
- Increase memory allocation: `set STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200`
- Use chunked processing for files >20MB
- Enable caching in Streamlit

### For Better Performance
- Close other applications while processing
- Use SSD storage for faster file I/O
- Ensure good internet connection for cloud features

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'streamlit'
   ```
   **Solution**: Ensure virtual environment is activated and dependencies installed

2. **Port Already in Use**
   ```
   OSError: [Errno 48] Address already in use
   ```
   **Solution**: Use different port: `streamlit run app.py --server.port 8502`

3. **File Upload Issues**
   ```
   File size exceeds maximum allowed
   ```
   **Solution**: Check `.env` file for `MAX_FILE_SIZE_MB` setting

4. **LaTeX Not Found**
   ```
   LaTeX engine not available
   ```
   **Solution**: Install MiKTeX or set `LATEX_ENABLED=false` in `.env`

### Debug Mode
```powershell
# Run with debug logging
set LOG_LEVEL=DEBUG
streamlit run src/app.py
```

### Log Files
- Check `logs/billgenerator.log` for detailed error information
- Enable console logging for real-time debugging

## 🔐 Security Considerations

### File Security
- Only upload trusted Excel files
- Application validates file types and content
- Temporary files are automatically cleaned

### Environment Security
- Keep `.env` file secure and never commit to version control
- Use strong session secrets
- Regular security updates

## 📞 Support & Help

### Getting Help
- Check logs in `logs/` directory
- Review error messages in browser console
- Test with sample files first

### Contact Information
- **Developer**: Rajkumar Singh
- **Email**: crajkumarsingh@hotmail.com
- **GitHub**: [@CRAJKUMARSINGH](https://github.com/CRAJKUMARSINGH)

### Project Information
- **Organization**: Public Works Department (PWD), Udaipur
- **Initiative**: Mrs. Premlata Jain, Additional Administrative Officer

## 🎯 Next Steps

After successful setup:
1. ✅ Test with sample Excel files
2. ✅ Verify PDF generation works
3. ✅ Check output quality and formatting
4. ✅ Configure any additional settings
5. ✅ Create backup of working configuration

## 📝 Development Notes

### For Developers
- Main entry point: `src/app.py`
- Configuration: `src/config.py`
- Core processing: `src/excel_processor.py`
- Templates: `templates/` directory

### Adding Features
- Follow existing code patterns
- Add tests in `tests/` directory
- Update documentation
- Test with various Excel file formats

---

**🎉 You're now ready to run the Infrastructure Billing System locally!**

For any issues or questions, refer to the troubleshooting section or contact support.