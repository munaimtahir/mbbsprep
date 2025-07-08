// Shared Topics Management URLs and Configuration
window.staffUrls = window.staffUrls || {
    topicCreate: '', // Will be set from template
    topicEdit: '', // Will be set from template
    topicToggleStatus: '', // Will be set from template
    topicDelete: '' // Will be set from template
};

// Shared utility functions for topics management
window.TopicsUtils = {
    // Get CSRF token from meta tag or cookie
    getCSRFToken: function() {
        const token = document.querySelector('meta[name="csrf-token"]');
        if (token) {
            return token.getAttribute('content');
        }
        
        // Fallback to cookie method
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    },
    
    // Escape HTML to prevent XSS
    escapeHtml: function(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },
    
    // Format count numbers
    formatCount: function(count) {
        if (!count || count === 0) return '0';
        if (count >= 1000) {
            return (count / 1000).toFixed(1) + 'k';
        }
        return count.toString();
    },
    
    // Show toast notification
    showToast: function(message, type = 'info', duration = 5000) {
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.toast-notification');
        existingToasts.forEach(toast => toast.remove());
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} toast-notification position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
            opacity: 0;
            transition: opacity 0.3s ease;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        // Add icon based on type
        let icon = 'fas fa-info-circle';
        if (type === 'success') icon = 'fas fa-check-circle';
        else if (type === 'error' || type === 'danger') icon = 'fas fa-exclamation-circle';
        else if (type === 'warning') icon = 'fas fa-exclamation-triangle';
        
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="${icon} me-2"></i>
                <span>${this.escapeHtml(message)}</span>
                <button type="button" class="btn-close ms-auto" aria-label="Close"></button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(toast);
        
        // Show with animation
        setTimeout(() => {
            toast.style.opacity = '1';
        }, 100);
        
        // Auto-remove after duration
        const autoRemove = setTimeout(() => {
            this.removeToast(toast);
        }, duration);
        
        // Manual close button
        const closeBtn = toast.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(autoRemove);
                this.removeToast(toast);
            });
        }
        
        return toast;
    },
    
    // Remove toast notification
    removeToast: function(toast) {
        toast.style.opacity = '0';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    },
    
    // Debounce function for search
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Update URL parameters without page reload
    updateUrlParams: function(params) {
        const url = new URL(window.location);
        
        Object.keys(params).forEach(key => {
            if (params[key]) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        
        window.history.replaceState({}, '', url);
    },
    
    // Get URL parameter
    getUrlParam: function(name) {
        const url = new URL(window.location);
        return url.searchParams.get(name);
    }
};

// Initialize from template data
document.addEventListener('DOMContentLoaded', function() {
    // URLs will be set by individual templates
    // This file provides the shared namespace and utilities
});
