/**
 * Timesheet App - JavaScript Functions
 * Standalone Application JS
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTimesheetApp();
});

/**
 * Main initialization function
 */
function initializeTimesheetApp() {
    initializeDebugWidget();
    initializeAlerts();
    initializeFormEnhancements();
    initializeTooltips();
    initializeConfirmations();
}

/**
 * Debug widget functionality
 */
function initializeDebugWidget() {
    const debugWidget = document.getElementById('debug-widget');
    if (debugWidget) {
        // Add debug mode class to body
        document.body.classList.add('debug-mode');
        
        // Update time every second
        const timeElement = debugWidget.querySelector('.debug-time');
        if (timeElement) {
            setInterval(function() {
                const now = new Date();
                timeElement.textContent = now.toLocaleTimeString();
            }, 1000);
        }
    }
}

/**
 * Enhanced alert handling
 */
function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add fade-in animation to alerts
    alerts.forEach(function(alert) {
        alert.classList.add('fade-in');
    });
}

/**
 * Form enhancements
 */
function initializeFormEnhancements() {
    // Add validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-focus first input field
    const firstInput = document.querySelector('form input:not([type="hidden"]):first-of-type');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Add character counter for textarea fields
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        addCharacterCounter(textarea);
    });
}

/**
 * Add character counter to textarea
 */
function addCharacterCounter(textarea) {
    const maxLength = textarea.getAttribute('maxlength');
    if (!maxLength) return;
    
    const counter = document.createElement('small');
    counter.className = 'form-text text-muted character-counter';
    textarea.parentNode.appendChild(counter);
    
    function updateCounter() {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${remaining} characters remaining`;
        counter.className = remaining < 20 ? 'form-text text-warning character-counter' : 'form-text text-muted character-counter';
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize confirmation dialogs
 */
function initializeConfirmations() {
    // Delete confirmations
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
    
    // Form confirmations
    const confirmForms = document.querySelectorAll('[data-confirm-submit]');
    confirmForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const message = this.getAttribute('data-confirm-submit') || 'Are you sure you want to submit this form?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
}

/**
 * Time calculation utilities
 */
const TimesheetUtils = {
    /**
     * Calculate total hours from time entries
     */
    calculateTotalHours: function(startTime, endTime, breakMinutes = 0) {
        if (!startTime || !endTime) return 0;
        
        const start = new Date(`2000-01-01 ${startTime}`);
        const end = new Date(`2000-01-01 ${endTime}`);
        
        if (end <= start) return 0;
        
        const diffMs = end - start;
        const diffHours = diffMs / (1000 * 60 * 60);
        const breakHours = breakMinutes / 60;
        
        return Math.max(0, diffHours - breakHours);
    },
    
    /**
     * Format hours to display format
     */
    formatHours: function(hours) {
        const h = Math.floor(hours);
        const m = Math.round((hours - h) * 60);
        return `${h}h ${m}m`;
    },
    
    /**
     * Validate time overlap
     */
    checkTimeOverlap: function(entries) {
        for (let i = 0; i < entries.length; i++) {
            for (let j = i + 1; j < entries.length; j++) {
                const entry1 = entries[i];
                const entry2 = entries[j];
                
                if (this.timesOverlap(entry1.start, entry1.end, entry2.start, entry2.end)) {
                    return {
                        overlap: true,
                        entries: [entry1, entry2]
                    };
                }
            }
        }
        return { overlap: false };
    },
    
    /**
     * Check if two time ranges overlap
     */
    timesOverlap: function(start1, end1, start2, end2) {
        const s1 = new Date(`2000-01-01 ${start1}`);
        const e1 = new Date(`2000-01-01 ${end1}`);
        const s2 = new Date(`2000-01-01 ${start2}`);
        const e2 = new Date(`2000-01-01 ${end2}`);
        
        return s1 < e2 && s2 < e1;
    }
};

/**
 * Export utilities for global access
 */
window.TimesheetUtils = TimesheetUtils;

/**
 * Loading indicator utilities
 */
const LoadingUtils = {
    show: function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            element.disabled = true;
        }
    },
    
    hide: function(element, originalText = '') {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    }
};

window.LoadingUtils = LoadingUtils;

/**
 * Notification utilities
 */
const NotificationUtils = {
    show: function(message, type = 'info', duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${this.getIcon(type)} ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('main .container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            if (duration > 0) {
                setTimeout(() => {
                    const bsAlert = new bootstrap.Alert(alertDiv);
                    bsAlert.close();
                }, duration);
            }
        }
    },
    
    getIcon: function(type) {
        const icons = {
            success: '<i class="fas fa-check-circle me-2"></i>',
            danger: '<i class="fas fa-exclamation-triangle me-2"></i>',
            warning: '<i class="fas fa-exclamation-circle me-2"></i>',
            info: '<i class="fas fa-info-circle me-2"></i>'
        };
        return icons[type] || icons.info;
    }
};

window.NotificationUtils = NotificationUtils;

/**
 * Mobile responsiveness enhancements
 */
function initializeMobileEnhancements() {
    // Collapse navbar on mobile after clicking a link
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });
}

// Initialize mobile enhancements
document.addEventListener('DOMContentLoaded', initializeMobileEnhancements);
