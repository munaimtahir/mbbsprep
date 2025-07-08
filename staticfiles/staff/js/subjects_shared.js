// Shared Subjects Management URLs and Configuration
window.staffUrls = window.staffUrls || {};

// Subject Management URLs - will be set from template
Object.assign(window.staffUrls, {
    subjectCreate: '',
    subjectEdit: '',
    subjectToggleStatus: '',
    topicCreate: '',
    topicEdit: '',
    getSubjectTopics: ''
});

// Common utilities for subjects management
window.SubjectsUtils = {
    // Show toast notification
    showToast: function(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast && toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    },
    
    // Get CSRF token
    getCSRFToken: function() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    },
    
    // Format count badge
    formatCount: function(count) {
        return count || 0;
    },
    
    // Escape HTML
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // URLs will be set by individual templates
    // This file provides the shared namespace and utilities
});
