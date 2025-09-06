/**
 * BillGenerator Optimized - Enhanced UI JavaScript
 * Provides interactive features and animations for better user experience
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeBillGenerator();
});

/**
 * Main initialization function
 */
function initializeBillGenerator() {
    console.log('🚀 BillGenerator Optimized - Initializing UI enhancements...');
    
    // Initialize all components
    initializeProgressTracking();
    initializeFileUpload();
    initializeAnimations();
    initializeTooltips();
    initializeNotifications();
    initializeKeyboardShortcuts();
    
    console.log('✅ BillGenerator UI enhancements loaded successfully');
}

/**
 * Progress tracking and status updates
 */
function initializeProgressTracking() {
    // Create progress tracker if it doesn't exist
    if (!document.getElementById('progressTracker')) {
        const progressTracker = document.createElement('div');
        progressTracker.id = 'progressTracker';
        progressTracker.className = 'progress-tracker';
        progressTracker.style.display = 'none';
        document.body.appendChild(progressTracker);
    }
}

/**
 * Update progress bar with animation
 */
function updateProgress(percentage, message = '') {
    const tracker = document.getElementById('progressTracker');
    if (!tracker) return;
    
    tracker.style.display = 'block';
    tracker.innerHTML = `
        <div class="progress-container">
            <div class="progress-bar" style="width: ${percentage}%"></div>
        </div>
        <div class="progress-text">${message}</div>
    `;
    
    // Auto-hide when complete
    if (percentage >= 100) {
        setTimeout(() => {
            tracker.style.display = 'none';
        }, 2000);
    }
}

/**
 * Enhanced file upload with drag and drop
 */
function initializeFileUpload() {
    // Find Streamlit file uploader and enhance it
    const fileUploaders = document.querySelectorAll('[data-testid="stFileUploader"]');
    
    fileUploaders.forEach(uploader => {
        enhanceFileUploader(uploader);
    });
}

function enhanceFileUploader(uploader) {
    // Add drag and drop styling classes
    uploader.classList.add('enhanced-uploader');
    
    // Drag and drop event handlers
    uploader.addEventListener('dragover', handleDragOver);
    uploader.addEventListener('dragleave', handleDragLeave);
    uploader.addEventListener('drop', handleFileDrop);
    
    // Add upload icon if not present
    if (!uploader.querySelector('.upload-enhancement')) {
        const enhancement = document.createElement('div');
        enhancement.className = 'upload-enhancement';
        enhancement.innerHTML = `
            <div class="upload-icon">📁</div>
            <p class="upload-text">Drop your Excel files here or click to browse</p>
            <p class="upload-subtext">Supports .xlsx and .xls files up to 50MB</p>
        `;
        uploader.insertBefore(enhancement, uploader.firstChild);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        showNotification(`📁 File "${files[0].name}" selected for upload`, 'info');
        
        // Validate file type
        const validTypes = ['.xlsx', '.xls'];
        const fileName = files[0].name.toLowerCase();
        const isValid = validTypes.some(type => fileName.endsWith(type));
        
        if (!isValid) {
            showNotification('❌ Invalid file type. Please select an Excel file (.xlsx or .xls)', 'error');
            return;
        }
        
        // Validate file size (50MB limit)
        if (files[0].size > 50 * 1024 * 1024) {
            showNotification('❌ File too large. Maximum size is 50MB', 'error');
            return;
        }
        
        showNotification('✅ File validated successfully', 'success');
    }
}

/**
 * Initialize smooth animations
 */
function initializeAnimations() {
    // Add fade-in animation to main content
    const mainElements = document.querySelectorAll('.main .block-container > div');
    mainElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // Add hover animations to buttons
    addButtonAnimations();
    
    // Add loading animations
    addLoadingAnimations();
}

function addButtonAnimations() {
    const buttons = document.querySelectorAll('button, .stButton > button');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(46, 125, 50, 0.3)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
}

function addLoadingAnimations() {
    // Monitor for Streamlit's built-in loading indicators
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Check for new loading elements
                const loadingElements = document.querySelectorAll('.stSpinner');
                loadingElements.forEach(enhanceLoadingSpinner);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

function enhanceLoadingSpinner(spinner) {
    if (spinner.classList.contains('enhanced')) return;
    
    spinner.classList.add('enhanced');
    spinner.innerHTML = `
        <div class="custom-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-text">Processing...</div>
        </div>
    `;
}

/**
 * Initialize tooltips for better UX
 */
function initializeTooltips() {
    // Add tooltips to various elements
    const tooltipElements = [
        { selector: '[data-testid="stFileUploader"]', text: 'Upload Excel files (.xlsx, .xls) up to 50MB' },
        { selector: '.stSelectbox', text: 'Choose your preferred options from the dropdown' },
        { selector: '.stButton', text: 'Click to perform the selected action' }
    ];
    
    tooltipElements.forEach(({ selector, text }) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            if (!element.title) {
                element.title = text;
                element.setAttribute('data-tooltip', text);
            }
        });
    });
}

/**
 * Notification system
 */
function initializeNotifications() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notificationContainer')) {
        const container = document.createElement('div');
        container.id = 'notificationContainer';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    notification.innerHTML = `
        <span class="notification-icon">${icons[type] || icons.info}</span>
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(notification);
    
    // Fade in animation
    setTimeout(() => {
        notification.classList.add('notification-show');
    }, 100);
    
    // Auto remove after duration
    setTimeout(() => {
        notification.classList.remove('notification-show');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, duration);
}

/**
 * Keyboard shortcuts for power users
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + U: Focus on file uploader
        if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
            e.preventDefault();
            const uploader = document.querySelector('[data-testid="stFileUploader"] input');
            if (uploader) {
                uploader.focus();
                showNotification('📁 File uploader focused - you can now select files', 'info', 2000);
            }
        }
        
        // Ctrl/Cmd + Enter: Trigger main processing button
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            const processButton = document.querySelector('button[kind="primary"]');
            if (processButton && !processButton.disabled) {
                processButton.click();
                showNotification('⚙️ Processing started via keyboard shortcut', 'info', 2000);
            }
        }
        
        // Escape: Close notifications
        if (e.key === 'Escape') {
            const notifications = document.querySelectorAll('.notification');
            notifications.forEach(notification => notification.remove());
        }
    });
    
    // Show shortcut help on first load
    setTimeout(() => {
        showNotification('💡 Keyboard shortcuts: Ctrl+U (upload), Ctrl+Enter (process), Esc (close)', 'info', 8000);
    }, 3000);
}

/**
 * Enhanced table interactions
 */
function enhanceDataTables() {
    const tables = document.querySelectorAll('table, [data-testid="stTable"]');
    
    tables.forEach(table => {
        // Add zebra striping if not present
        const rows = table.querySelectorAll('tr');
        rows.forEach((row, index) => {
            if (index > 0 && index % 2 === 0) {
                row.classList.add('even-row');
            }
        });
        
        // Add hover effects
        table.classList.add('enhanced-table');
    });
}

/**
 * Real-time validation feedback
 */
function initializeValidation() {
    // Monitor form inputs and provide real-time feedback
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('change', validateInput);
        input.addEventListener('blur', validateInput);
    });
}

function validateInput(e) {
    const input = e.target;
    const value = input.value;
    
    // Remove existing validation classes
    input.classList.remove('validation-success', 'validation-error');
    
    // Basic validation based on input type
    let isValid = true;
    let message = '';
    
    if (input.type === 'email' && value) {
        isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        message = isValid ? '✅ Valid email' : '❌ Invalid email format';
    }
    
    if (input.type === 'number' && value) {
        isValid = !isNaN(value) && isFinite(value);
        message = isValid ? '✅ Valid number' : '❌ Invalid number';
    }
    
    // Apply validation styling
    input.classList.add(isValid ? 'validation-success' : 'validation-error');
    
    // Show validation message
    if (message && value) {
        showValidationMessage(input, message, isValid ? 'success' : 'error');
    }
}

function showValidationMessage(input, message, type) {
    // Remove existing validation messages
    const existingMessage = input.parentElement.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new validation message
    const messageElement = document.createElement('div');
    messageElement.className = `validation-message validation-${type}`;
    messageElement.textContent = message;
    
    // Insert after input
    input.parentElement.insertBefore(messageElement, input.nextSibling);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (messageElement.parentElement) {
            messageElement.remove();
        }
    }, 3000);
}

/**
 * Performance monitoring
 */
function initializePerformanceMonitoring() {
    // Monitor page load performance
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            const loadTime = Math.round(perfData.loadEventEnd - perfData.loadEventStart);
            
            if (loadTime > 2000) {
                console.warn(`⚠️ Slow page load detected: ${loadTime}ms`);
            } else {
                console.log(`✅ Page loaded in ${loadTime}ms`);
            }
        }, 1000);
    });
}

/**
 * Accessibility enhancements
 */
function initializeAccessibility() {
    // Add ARIA labels where missing
    const buttons = document.querySelectorAll('button:not([aria-label])');
    buttons.forEach(button => {
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', button.textContent || 'Button');
        }
    });
    
    // Add focus indicators
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
}

/**
 * Auto-save functionality for form data
 */
function initializeAutoSave() {
    const formElements = document.querySelectorAll('input, select, textarea');
    
    formElements.forEach(element => {
        element.addEventListener('change', function() {
            const key = `billgen_${this.name || this.id || 'unnamed'}`;
            localStorage.setItem(key, this.value);
        });
        
        // Restore saved values
        const key = `billgen_${element.name || element.id || 'unnamed'}`;
        const savedValue = localStorage.getItem(key);
        if (savedValue && !element.value) {
            element.value = savedValue;
        }
    });
}

/**
 * Export utilities
 */
window.BillGeneratorUI = {
    updateProgress,
    showNotification,
    enhanceDataTables,
    initializeValidation,
    initializePerformanceMonitoring,
    initializeAccessibility,
    initializeAutoSave
};

// Global error handler
window.addEventListener('error', function(e) {
    console.error('🚨 BillGenerator UI Error:', e.error);
    showNotification('An error occurred. Please refresh the page if issues persist.', 'error');
});

// Initialize performance monitoring
initializePerformanceMonitoring();

console.log('🎨 BillGenerator UI enhancements loaded successfully');
