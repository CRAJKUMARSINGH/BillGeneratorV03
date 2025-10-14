# 🏗️ BillGeneratorV03 - Infrastructure Billing System

Professional document generation system for infrastructure billing with Excel processing, PDF generation, and compliance-ready outputs.

## 🚀 Quick Deployment

### Deploy to Streamlit Cloud (Recommended)
1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select this repository
5. Set the main file as `streamlit_app.py`
6. Click "Deploy" - Your app will be live in minutes!

For detailed deployment instructions, see [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md).

### Local Deployment
```bash
# Clone the repository
git clone https://github.com/CRAJKUMARSINGH/BillGeneratorV03.git
cd BillGeneratorV03

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

## 📋 Features

- **Excel Processing**: Advanced parsing of infrastructure billing Excel templates
- **PDF Generation**: Professional PDF documents with compliance formatting
- **LaTeX Templates**: High-quality document templating system
- **ZIP Packaging**: Complete document packages for easy distribution
- **Cloud Ready**: Optimized for Streamlit Cloud deployment
- **Responsive UI**: Modern web interface with professional styling

## 🎯 Usage

1. Prepare your infrastructure billing Excel file with the required sheets:
   - Title sheet
   - Work Order sheet
   - Bill Quantity sheet
   - Optional: Extra Items sheet

2. Upload your Excel file using the web interface

3. Process the file to generate professional documentation

4. Download the complete ZIP package with all generated documents

## 🛠️ Technical Details

### Requirements
- Python 3.8+
- Streamlit 1.28+
- See [requirements.txt](requirements.txt) for full dependency list

### Project Structure
```
BillGeneratorV03/
├── streamlit_app.py         # Main Streamlit application
├── requirements.txt         # Python dependencies
├── src/                     # Core processing modules
│   ├── excel_processor.py   # Excel file processing
│   ├── latex_generator.py   # LaTeX document generation
│   └── ...                  # Other utility modules
├── templates/               # Document templates
└── attached_assets/         # CSS and JavaScript assets
```

## 🤝 Support

**Developer**: RAJKUMAR SINGH CHAUHAN  
**Email**: crajkumarsingh@hotmail.com  
**Organization**: Public Works Department (PWD), Udaipur

For issues, feature requests, or contributions, please open an issue on this repository.