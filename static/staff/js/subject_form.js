// Subject Form JavaScript
(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeForm();
        initializeValidation();
        bindEventHandlers();
    });
    
    // Initialize form functionality
    function initializeForm() {
        // Focus on the first input
        const nameInput = document.getElementById('id_name');
        if (nameInput && !nameInput.value) {
            nameInput.focus();
        }
        
        // Auto-generate code from name if code is empty
        bindAutoCodeGeneration();
        
        // Initialize tooltips if Bootstrap is available
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
    
    // Auto-generate subject code from name
    function bindAutoCodeGeneration() {
        const nameInput = document.getElementById('id_name');
        const codeInput = document.getElementById('id_code');
        
        if (nameInput && codeInput) {
            nameInput.addEventListener('input', function() {
                // Only auto-generate if code field is empty
                if (!codeInput.value.trim()) {
                    const name = this.value.trim();
                    if (name) {
                        // Generate code from first letters of words
                        const code = name
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase())
                            .join('')
                            .substring(0, 10); // Limit to 10 characters
                        
                        codeInput.value = code;
                        
                        // Add visual feedback
                        codeInput.classList.add('auto-generated');
                        setTimeout(() => {
                            codeInput.classList.remove('auto-generated');
                        }, 1000);
                    }
                }
            });
            
            // Clear auto-generation flag when user manually edits code
            codeInput.addEventListener('input', function() {
                this.classList.remove('auto-generated');
            });
        }
    }
    
    // Initialize form validation
    function initializeValidation() {
        const form = document.getElementById('subjectForm');
        if (!form) return;
        
        // Real-time validation
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearFieldError);
        });
        
        // Form submission validation
        form.addEventListener('submit', handleFormSubmission);
    }
    
    // Validate individual field
    function validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        
        // Clear existing validation
        clearFieldError(event);
        
        // Check required fields
        if (field.hasAttribute('required') && !value) {
            showFieldError(field, 'This field is required');
            return false;
        }
        
        // Specific validation based on field type
        switch (field.name) {
            case 'name':
                return validateSubjectName(field, value);
            case 'code':
                return validateSubjectCode(field, value);
            default:
                return true;
        }
    }
    
    // Validate subject name
    function validateSubjectName(field, value) {
        if (value.length < 2) {
            showFieldError(field, 'Subject name must be at least 2 characters long');
            return false;
        }
        
        if (value.length > 100) {
            showFieldError(field, 'Subject name cannot exceed 100 characters');
            return false;
        }
        
        // Check for valid characters (letters, numbers, spaces, hyphens)
        const validPattern = /^[a-zA-Z0-9\s\-&()]+$/;
        if (!validPattern.test(value)) {
            showFieldError(field, 'Subject name contains invalid characters');
            return false;
        }
        
        return true;
    }
    
    // Validate subject code
    function validateSubjectCode(field, value) {
        if (value && value.length > 10) {
            showFieldError(field, 'Subject code cannot exceed 10 characters');
            return false;
        }
        
        if (value) {
            // Check for valid characters (letters and numbers only)
            const validPattern = /^[a-zA-Z0-9]+$/;
            if (!validPattern.test(value)) {
                showFieldError(field, 'Subject code can only contain letters and numbers');
                return false;
            }
        }
        
        return true;
    }
    
    // Show field error
    function showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
    
    // Clear field error
    function clearFieldError(event) {
        const field = event.target;
        field.classList.remove('is-invalid');
        
        const errorMessage = field.parentNode.querySelector('.invalid-feedback');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
    
    // Handle form submission
    function handleFormSubmission(event) {
        const form = event.target;
        let isValid = true;
        
        // Validate all required fields
        const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
        requiredFields.forEach(field => {
            const fieldEvent = { target: field };
            if (!validateField(fieldEvent)) {
                isValid = false;
            }
        });
        
        // If validation fails, prevent submission
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
            
            // Show toast notification
            showToast('Please fix the errors before submitting', 'error');
            
            // Focus on first invalid field
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            return false;
        }
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            showButtonLoading(submitButton);
        }
        
        return true;
    }
    
    // Bind additional event handlers
    function bindEventHandlers() {
        // Handle delete/archive confirmation
        const deleteModal = document.getElementById('deleteModal');
        if (deleteModal) {
            deleteModal.addEventListener('show.bs.modal', function(event) {
                // You could add additional confirmation logic here
            });
        }
        
        // Handle "Manage All Topics" link
        const manageTopicsLink = document.querySelector('a[href*="topic_list"]');
        if (manageTopicsLink) {
            manageTopicsLink.addEventListener('click', function(event) {
                // Could add a confirmation if there are unsaved changes
                if (hasUnsavedChanges()) {
                    if (!confirm('You have unsaved changes. Are you sure you want to leave this page?')) {
                        event.preventDefault();
                    }
                }
            });
        }
        
        // Handle back button
        const backButton = document.querySelector('a[href*="subject_list"]');
        if (backButton) {
            backButton.addEventListener('click', function(event) {
                if (hasUnsavedChanges()) {
                    if (!confirm('You have unsaved changes. Are you sure you want to leave this page?')) {
                        event.preventDefault();
                    }
                }
            });
        }
        
        // Track form changes
        trackFormChanges();
    }
    
    // Track form changes to detect unsaved changes
    function trackFormChanges() {
        const form = document.getElementById('subjectForm');
        if (!form) return;
        
        // Store initial form data
        let initialFormData = new FormData(form);
        let hasChanges = false;
        
        // Monitor form changes
        form.addEventListener('input', function() {
            hasChanges = true;
        });
        
        form.addEventListener('change', function() {
            hasChanges = true;
        });
        
        // Store the function globally so other functions can access it
        window.hasUnsavedChanges = function() {
            return hasChanges;
        };
        
        // Reset changes flag on successful submission
        form.addEventListener('submit', function() {
            hasChanges = false;
        });
        
        // Warn about unsaved changes on page unload
        window.addEventListener('beforeunload', function(event) {
            if (hasChanges) {
                event.preventDefault();
                event.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
                return event.returnValue;
            }
        });
    }
    
    // Check if form has unsaved changes
    function hasUnsavedChanges() {
        return window.hasUnsavedChanges ? window.hasUnsavedChanges() : false;
    }
    
    // Show button loading state
    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.classList.add('loading');
        button.disabled = true;
        
        // Store original text
        button.dataset.originalText = originalText;
        
        // Reset after timeout (fallback)
        setTimeout(() => {
            hideButtonLoading(button);
        }, 30000); // 30 seconds timeout
    }
    
    // Hide button loading state
    function hideButtonLoading(button) {
        button.classList.remove('loading');
        button.disabled = false;
        
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            delete button.dataset.originalText;
        }
    }
    
    // Show toast notification
    function showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        toast.textContent = message;
        
        // Add to page
        document.body.appendChild(toast);
        
        // Show with animation
        setTimeout(() => {
            toast.style.opacity = '1';
        }, 100);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 5000);
    }
    
    // Add CSS for auto-generated field highlight
    const style = document.createElement('style');
    style.textContent = `
        .form-control.auto-generated {
            border-color: #43B284 !important;
            background-color: #E8F5E8 !important;
            transition: all 0.3s ease;
        }
        
        .form-control.auto-generated:focus {
            box-shadow: 0 0 0 0.25rem rgba(67, 178, 132, 0.15) !important;
        }
    `;
    document.head.appendChild(style);
    
})();
