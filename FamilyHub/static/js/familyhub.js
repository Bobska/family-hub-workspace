/**
 * FamilyHub - Global JavaScript
 * Main JavaScript file for the FamilyHub integrated platform
 * Handles global functionality, navigation, and user interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🏠 FamilyHub Global JavaScript loaded');
    
    // Initialize all global functionality
    initializeNavigation();
    initializeDebugWidget();
    initializeAlerts();
    initializeUserPreferences();
    
    console.log('✅ FamilyHub initialization complete');
});

/**
 * Global Navigation Handlers
 * Manages the two-tier navigation system
 */
function initializeNavigation() {
    // Handle active state management for global navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
            link.classList.add('active');
        }
    });
    
    // Handle dropdown menus
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            const menu = this.nextElementSibling;
            menu.classList.toggle('show');
        });
    });
    
    console.log('🧭 Navigation system initialized');
}

/**
 * Debug Widget Functionality
 * Manages debug information display and interactions
 */
function initializeDebugWidget() {
    const debugWidget = document.getElementById('debug-widget');
    
    if (debugWidget) {
        // Add body padding when debug widget is present
        document.body.classList.add('debug-mode');
        
        // Update debug time every second
        const timeElement = debugWidget.querySelector('.debug-time');
        if (timeElement) {
            setInterval(function() {
                const now = new Date();
                const timeString = now.toLocaleTimeString('en-GB', {
                    hour12: false,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                timeElement.textContent = timeString;
            }, 1000);
        }
        
        console.log('🐛 Debug widget initialized');
    }
}

/**
 * Alert Management
 * Handles Django messages and custom alerts
 */
function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });
    
    console.log('🔔 Alert system initialized');
}

/**
 * User Preferences Management
 * Handles theme, layout preferences, etc.
 */
function initializeUserPreferences() {
    // Load saved preferences from localStorage
    const preferences = loadUserPreferences();
    applyUserPreferences(preferences);
    
    console.log('⚙️ User preferences loaded');
}

/**
 * Load user preferences from localStorage
 */
function loadUserPreferences() {
    try {
        const saved = localStorage.getItem('familyhub_preferences');
        return saved ? JSON.parse(saved) : getDefaultPreferences();
    } catch (error) {
        console.warn('Failed to load user preferences:', error);
        return getDefaultPreferences();
    }
}

/**
 * Get default user preferences
 */
function getDefaultPreferences() {
    return {
        theme: 'default',
        sidebarCollapsed: false,
        autoSave: true,
        notifications: true
    };
}

/**
 * Apply user preferences to the interface
 */
function applyUserPreferences(preferences) {
    // Apply theme
    if (preferences.theme && preferences.theme !== 'default') {
        document.body.classList.add(`theme-${preferences.theme}`);
    }
    
    // Apply other preferences as needed
    if (preferences.sidebarCollapsed) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.add('collapsed');
        }
    }
}

/**
 * Save user preferences to localStorage
 */
function saveUserPreferences(preferences) {
    try {
        localStorage.setItem('familyhub_preferences', JSON.stringify(preferences));
        console.log('💾 User preferences saved');
    } catch (error) {
        console.error('Failed to save user preferences:', error);
    }
}

/**
 * Utility Functions
 */

/**
 * Show a toast notification
 */
function showToast(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (toast.parentNode) {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 150);
        }
    }, duration);
}

/**
 * CSRF Token Helper for AJAX requests
 */
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    
    // Fallback to meta tag
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

/**
 * Enhanced fetch wrapper with CSRF support
 */
function familyhubFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'same-origin',
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    };
    
    return fetch(url, mergedOptions);
}

/**
 * Global error handler
 */
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    
    // Only show user-friendly errors in production
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        showToast('An unexpected error occurred. Please refresh the page.', 'danger');
    }
});

/**
 * Export functions for use by other scripts
 */
window.FamilyHub = {
    showToast,
    getCSRFToken,
    fetch: familyhubFetch,
    preferences: {
        load: loadUserPreferences,
        save: saveUserPreferences,
        apply: applyUserPreferences
    }
};

console.log('🚀 FamilyHub global functions exported to window.FamilyHub');
