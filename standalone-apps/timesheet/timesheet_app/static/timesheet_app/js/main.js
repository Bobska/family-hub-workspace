/*
 * Timesheet Standalone App JavaScript
 * Interactive functionality and UI enhancements
 * Following FamilyHub architecture guidelines
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all interactive features
    initializeAnimations();
    initializeFormEnhancements();
    initializeTimeEntryFeatures();
    initializeNavigationFeatures();
    initializeDebugWidget();
    
    console.log('🕐 Timesheet Standalone App initialized successfully');
});

/**
 * Initialize content animations
 */
function initializeAnimations() {
    // Add animated content class to main container
    const mainContent = document.querySelector('main.container');
    if (mainContent) {
        mainContent.classList.add('animated-content');
    }
    
    // Animate cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animated-content');
    });
    
    // Animate time entry rows
    const timeEntries = document.querySelectorAll('.time-entry-row');
    timeEntries.forEach((entry, index) => {
        entry.style.animationDelay = `${index * 0.05}s`;
        entry.classList.add('animated-content');
    });
}

/**
 * Enhance form interactions
 */
function initializeFormEnhancements() {
    // Auto-focus first form field
    const firstInput = document.querySelector('form input[type="text"], form input[type="date"], form input[type="time"], form select');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Add loading state to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = '<i class="fas fa-spinner spinner me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Enhance form validation
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('error-highlight');
            } else {
                this.classList.remove('error-highlight');
                this.classList.add('success-highlight');
            }
        });
    });
}

/**
 * Time entry specific features
 */
function initializeTimeEntryFeatures() {
    // Add click handlers to time entry rows
    const timeEntryRows = document.querySelectorAll('.time-entry-row');
    timeEntryRows.forEach(row => {
        row.addEventListener('click', function() {
            // Add visual feedback
            this.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
            setTimeout(() => {
                this.style.backgroundColor = '';
            }, 300);
        });
    });
    
    // Add hover effects to entry items
    const entryItems = document.querySelectorAll('.entry-item');
    entryItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02) translateX(5px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Auto-calculate time differences
    const startTimeInput = document.querySelector('input[name="start_time"]');
    const endTimeInput = document.querySelector('input[name="end_time"]');
    
    if (startTimeInput && endTimeInput) {
        function calculateDuration() {
            const startTime = startTimeInput.value;
            const endTime = endTimeInput.value;
            
            if (startTime && endTime) {
                const start = new Date(`2000-01-01 ${startTime}`);
                const end = new Date(`2000-01-01 ${endTime}`);
                const diffMs = end - start;
                const diffHours = diffMs / (1000 * 60 * 60);
                
                if (diffHours > 0) {
                    const durationDisplay = document.querySelector('#duration-display');
                    if (durationDisplay) {
                        durationDisplay.textContent = `Duration: ${diffHours.toFixed(2)} hours`;
                        durationDisplay.classList.add('success-highlight');
                    }
                }
            }
        }
        
        startTimeInput.addEventListener('change', calculateDuration);
        endTimeInput.addEventListener('change', calculateDuration);
    }
}

/**
 * Navigation enhancements
 */
function initializeNavigationFeatures() {
    // Add active state management
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
    
    // Enhanced dropdown functionality
    const dropdownToggle = document.querySelector('#navbarDropdown');
    if (dropdownToggle) {
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu) {
                dropdownMenu.classList.toggle('show');
            }
        });
    }
    
    // Mobile menu enhancements
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const targetId = this.getAttribute('data-bs-target');
            const target = document.querySelector(targetId);
            if (target) {
                target.classList.toggle('show');
            }
        });
    }
}

/**
 * Debug widget functionality
 */
function initializeDebugWidget() {
    const debugWidget = document.querySelector('#debug-widget');
    if (debugWidget) {
        // Add close button functionality
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: white;
            padding: 0 5px;
            cursor: pointer;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        `;
        
        closeBtn.addEventListener('click', function() {
            debugWidget.style.display = 'none';
            document.body.style.paddingTop = '0';
        });
        
        closeBtn.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
        });
        
        closeBtn.addEventListener('mouseleave', function() {
            this.style.opacity = '0.8';
        });
        
        // Add close button to debug widget
        const debugContent = debugWidget.querySelector('div');
        if (debugContent) {
            debugContent.appendChild(closeBtn);
        }
        
        // Add body class for debug mode
        document.body.classList.add('debug-mode');
    }
}

/**
 * Alert message auto-dismiss
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        // Auto dismiss success and info alerts after 5 seconds
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

/**
 * Utility function to show toast notifications
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toastElement.setAttribute('role', 'alert');
    toastElement.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.querySelector('.toast-container').appendChild(toastElement);
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove element after hiding
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Time formatting utilities
 */
function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
}

function formatTime(timeString) {
    const time = new Date(`2000-01-01 ${timeString}`);
    return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Date utilities
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getToday() {
    return new Date().toISOString().split('T')[0];
}

/**
 * Local storage helpers
 */
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(`timesheet_${key}`, JSON.stringify(value));
    } catch (e) {
        console.warn('Could not save to localStorage:', e);
    }
}

function getFromLocalStorage(key) {
    try {
        const value = localStorage.getItem(`timesheet_${key}`);
        return value ? JSON.parse(value) : null;
    } catch (e) {
        console.warn('Could not read from localStorage:', e);
        return null;
    }
}

/**
 * Form data persistence
 */
function initializeFormPersistence() {
    const forms = document.querySelectorAll('form[data-persist]');
    forms.forEach(form => {
        const formId = form.getAttribute('data-persist');
        
        // Load saved data
        const savedData = getFromLocalStorage(`form_${formId}`);
        if (savedData) {
            Object.keys(savedData).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && field.type !== 'hidden') {
                    field.value = savedData[key];
                }
            });
        }
        
        // Save data on change
        form.addEventListener('input', function() {
            const formData = new FormData(form);
            const data = {};
            for (const [key, value] of formData.entries()) {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            }
            saveToLocalStorage(`form_${formId}`, data);
        });
        
        // Clear saved data on successful submit
        form.addEventListener('submit', function() {
            setTimeout(() => {
                if (!form.querySelector('.error-highlight')) {
                    localStorage.removeItem(`timesheet_form_${formId}`);
                }
            }, 100);
        });
    });
}

/**
 * Keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Alt + D = Dashboard
        if (e.altKey && e.key === 'd') {
            e.preventDefault();
            window.location.href = document.querySelector('a[href*="dashboard"]')?.href;
        }
        
        // Alt + E = Daily Entry
        if (e.altKey && e.key === 'e') {
            e.preventDefault();
            window.location.href = document.querySelector('a[href*="daily_entry"]')?.href;
        }
        
        // Alt + J = Jobs
        if (e.altKey && e.key === 'j') {
            e.preventDefault();
            window.location.href = document.querySelector('a[href*="job_list"]')?.href;
        }
        
        // Escape = Close modals/dropdowns
        if (e.key === 'Escape') {
            const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
            openDropdowns.forEach(dropdown => dropdown.classList.remove('show'));
        }
    });
}

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAlerts();
    initializeFormPersistence();
    initializeKeyboardShortcuts();
});

// Export functions for external use
window.TimesheetApp = {
    showToast,
    formatDuration,
    formatTime,
    formatDate,
    getToday,
    saveToLocalStorage,
    getFromLocalStorage
};
