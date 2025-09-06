# 🏗️ Infrastructure Billing System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://billgeneratorv03.streamlit.app)

A professional document generation and compliance solution for infrastructure billing, developed for PWD, Udaipur.

## 🎯 Features

- **📊 Advanced Excel Processing**: Intelligent parsing of infrastructure billing data
- **📄 Multi-Format Output**: HTML, PDF, and LaTeX document generation
- **📐 LaTeX Templates**: Professional formatting for Election Commission compliance
- **📦 ZIP Packaging**: Complete document packages with organized structure
- **⚡ Performance Optimized**: Enhanced caching and memory optimization
- **🔒 Secure**: Built-in validation and error handling
- **☁️ Cloud Ready**: Deployed on Streamlit Cloud for easy access

## 🚀 Live Demo

Access the live application: [Infrastructure Billing System](https://billgeneratorv03.streamlit.app)

## 📋 Requirements

### Excel File Format
Your Excel file should contain the following sheets:
- **Title**: Project information and metadata
- **Work Order**: Original planned work items
- **Bill Quantity**: Actual completed work quantities
- **Extra Items** (Optional): Additional work not in original plan

### System Requirements
- Python 3.8+
- Streamlit 1.28+
- See `requirements.txt` for complete dependencies

## 🛠️ Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CRAJKUMARSINGH/BillGeneratorV03.git
   cd BillGeneratorV03
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access locally:**
   Open your browser to `http://localhost:8501`

## ☁️ Cloud Deployment

This application is deployed on Streamlit Cloud for easy access without local installation.

### Deployment Configuration
- **Main App**: `streamlit_app.py`
- **Config**: `.streamlit/config.toml`
- **Dependencies**: `requirements.txt`

## 📖 Usage Guide

1. **Upload Excel File**: 
   - Use the file uploader to select your .xlsx file
   - Maximum file size: 50MB

2. **Processing**: 
   - Click "Process File" to start analysis
   - Progress will be shown in real-time

3. **Download Results**: 
   - Download the complete ZIP package (full version)
   - View analysis results in the cloud version

## 👤 Developer

**Rajkumar Singh**
- GitHub: [@CRAJKUMARSINGH](https://github.com/CRAJKUMARSINGH)
- Email: crajkumarsingh@hotmail.com

## 🏢 Organization

**Public Works Department (PWD), Udaipur**
- Initiative by: Mrs. Premlata Jain, Additional Administrative Officer
- Purpose: Infrastructure billing and compliance documentation

---

**⚡ Powered by Streamlit Cloud**
