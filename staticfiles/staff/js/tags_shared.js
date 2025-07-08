// Tags Shared Utilities
window.TagsUtils = {
    // Get CSRF token from meta tag
    getCSRFToken: function() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    },
    
    // Show toast notification
    showToast: function(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed`;
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.style.minWidth = '300px';
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        document.body.appendChild(toast);
        
        // Auto close after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    },
    
    // Escape HTML for safe insertion
    escapeHtml: function(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },
    
    // Format count with appropriate styling
    formatCount: function(count) {
        return count > 0 ? count : '<span class="text-muted">0</span>';
    }
};
