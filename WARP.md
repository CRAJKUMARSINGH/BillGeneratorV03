# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

BillGenerator Optimized is a professional infrastructure billing document generator built with Streamlit. It processes Excel files containing project data and generates multiple document formats (HTML, LaTeX, PDF) with comprehensive packaging. This is a Python-based application designed for government compliance, specifically Election Commission requirements.

## Quick Start Commands

### Development Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Run the main application
streamlit run src/app.py

# Run enhanced performance version
streamlit run src/enhanced_app.py

# Run tests
pytest tests/ -v

# Run comprehensive test suite
python -m pytest tests/test_comprehensive.py -v
```

### One-Click Deployment
```powershell
# Full automated deployment
python one_click_deploy.py

# Traditional deployment with validation
python deploy.py
```

### Testing & Quality Assurance
```powershell
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run performance tests specifically
python -m pytest tests/test_performance.py -v

# Test specific module
pytest tests/test_comprehensive.py::TestExcelProcessor -v
```

### Production Operations
```powershell
# Start production server
streamlit run src/app.py --server.headless true --server.port 8501

# With custom configuration
streamlit run src/app.py --server.headless true --server.port 8501 --server.address 0.0.0.0

# Check system configuration
python -c "from src.config import config; print(config.validate_environment())"
```

## High-Level Architecture

### Core Components
The application follows a modular architecture with clear separation of concerns:

1. **Application Layer** (`src/app.py`, `src/enhanced_app.py`)
   - Main Streamlit interface and user interactions
   - Two versions: standard and performance-enhanced
   - Handles file uploads, progress tracking, and result presentation

2. **Processing Layer** 
   - `src/excel_processor.py`: Excel file parsing and data extraction
   - `src/document_generator.py`: HTML document generation (referenced but not in current src/)
   - `src/latex_generator.py`: LaTeX template processing
   - `src/pdf_merger.py`: PDF generation from HTML and LaTeX sources

3. **Configuration & Utilities**
   - `src/config.py`: Centralized configuration management with environment validation
   - `src/utils.py`: Common utilities for data validation, formatting, and file handling

4. **Performance & Optimization**
   - `src/enhanced_cache.py`: Multi-level caching system (memory, file, Redis)
   - `src/performance_optimizer.py`: Memory management and processing optimization

### Data Flow Architecture
```
Excel Upload → Validation → Sheet Processing → Document Generation → PDF Conversion → ZIP Packaging → Download
```

**Key Processing Stages:**
1. **File Validation**: Structure and format verification
2. **Sheet Detection**: Intelligent identification of Title, Work Order, Bill Quantity, and Extra Items sheets
3. **Data Processing**: Extraction with fuzzy column matching and data cleaning
4. **Multi-Format Generation**: Simultaneous HTML and LaTeX document creation
5. **Dual PDF Generation**: Both HTML-based and LaTeX-based PDF outputs
6. **Professional Packaging**: Organized ZIP files with proper directory structure

### Template System
- **Location**: `templates/` directory
- **Types**: HTML templates (`.html`) and LaTeX templates (`.tex`)
- **Key Templates**:
  - `first_page_summary.tex`: Project summary and totals
  - `deviation_statement.html`: Work order vs actual comparison
  - `certificate_ii.html` & `certificate_iii.html`: Compliance certificates
  - Dynamic template selection based on data availability

### Configuration Architecture
The `src/config.py` module provides:
- **Environment Detection**: LaTeX availability, system resources
- **Directory Management**: Automatic creation of required folders
- **Processing Settings**: Column mapping, validation rules, GST rates
- **UI Theming**: Colors, fonts, and layout parameters
- **Security Settings**: File validation, sanitization rules

## Key Development Patterns

### Error Handling Strategy
- **Graceful Degradation**: Falls back to HTML-only PDF generation if LaTeX unavailable
- **Comprehensive Validation**: File structure, data types, and business rules
- **User-Friendly Messages**: Clear error descriptions with troubleshooting guides
- **Logging**: Structured logging with rotation and different levels

### Performance Optimization
- **Intelligent Caching**: Multi-level caching with TTL and tag-based invalidation
- **Memory Management**: Automatic cleanup and optimization
- **Batch Processing**: Large dataset handling with progress tracking
- **Lazy Loading**: Deferred loading of heavy modules and resources

### Testing Architecture
- **Comprehensive Test Suite**: `tests/test_comprehensive.py` covers all major functionality
- **Performance Testing**: `tests/test_performance.py` for optimization validation
- **Mock Testing**: Extensive use of mocks for external dependencies
- **Edge Case Coverage**: Testing invalid inputs, boundary conditions, and error scenarios

## Development Workflow

### File Processing Development
When working with Excel processing features:
1. Test with `Input_Files_for_tests/` sample files
2. Use `src/utils.py` validation functions
3. Check `src/config.py` for column mapping and sheet detection rules
4. Consider fuzzy matching for column headers

### Template Development  
For document template modifications:
1. HTML templates use Jinja2 syntax
2. LaTeX templates require proper escaping for special characters
3. Test both rendering paths (HTML→PDF and LaTeX→PDF)
4. Maintain Election Commission compliance requirements

### Performance Optimization
When optimizing performance:
1. Use `@monitor_performance` decorator for timing
2. Implement caching with `@cached_operation` decorator
3. Check memory usage with performance monitoring tools
4. Test with large datasets to validate optimizations

### Deployment Considerations
- **Environment Variables**: Use for sensitive configuration
- **LaTeX Dependency**: Optional but recommended for professional output
- **Memory Requirements**: Minimum 4GB RAM, 8GB+ recommended
- **File Size Limits**: Default 50MB upload limit (configurable)

## Common Development Patterns

### Adding New Document Types
1. Create template in `templates/` directory
2. Add generation logic to appropriate processor
3. Update `src/config.py` template configuration
4. Add to ZIP packaging in `ZipPackager`
5. Update UI progress tracking

### Adding New Data Validations
1. Implement in `src/utils.py` 
2. Add to `src/config.py` validation rules
3. Update error messages for user clarity
4. Add comprehensive test cases

### Performance Enhancement
1. Profile with `performance_optimizer.py` tools
2. Implement caching where appropriate
3. Consider batch processing for large operations
4. Monitor memory usage and cleanup

## Environment & Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **pandas + openpyxl**: Excel file processing
- **Jinja2**: Template rendering
- **reportlab + weasyprint**: PDF generation
- **psutil**: System monitoring

### Optional Dependencies  
- **LaTeX**: For professional PDF generation
- **Redis**: For distributed caching (enhanced version)
- **pytest**: For testing and development

### Development Tools
- **Performance Monitoring**: Built-in with `performance_optimizer.py`
- **Logging**: Configurable levels with file rotation
- **Configuration Validation**: Automatic environment checking
- **Error Reporting**: Detailed traceback with troubleshooting guides

## Specific Implementation Notes

### Excel Sheet Detection
The system uses intelligent fuzzy matching to detect sheet types:
- Configurable keywords in `config.py`
- Flexible column header matching
- Graceful handling of missing or renamed sheets

### Multi-Format PDF Generation
Two parallel PDF generation paths:
1. **HTML→PDF**: Fast, reliable, good for data tables
2. **LaTeX→PDF**: Professional typography, government compliance
Both outputs packaged together for user choice

### Government Compliance Features
- Election Commission format requirements
- Professional certificate templates
- Audit trail preservation
- Data integrity validation

This architecture ensures maintainable, scalable, and robust document processing while maintaining flexibility for future enhancements.
