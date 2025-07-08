// Topic Form JavaScript
(function() {
    'use strict';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeForm();
        bindEventHandlers();
    });
    
    // Initialize form
    function initializeForm() {
        // Set focus to first field
        const firstInput = document.querySelector('#id_subject');
        if (firstInput) {
            firstInput.focus();
        }
        
        // Auto-populate subject if passed in URL
        const urlParams = new URLSearchParams(window.location.search);
        const subjectId = urlParams.get('subject');
        if (subjectId) {
            const subjectSelect = document.getElementById('id_subject');
            if (subjectSelect) {
                subjectSelect.value = subjectId;
            }
        }
    }
    
    // Bind event handlers
    function bindEventHandlers() {
        // Form submission
        const form = document.getElementById('topicForm');
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }
        
        // Subject change - update order suggestion
        const subjectSelect = document.getElementById('id_subject');
        if (subjectSelect) {
            subjectSelect.addEventListener('change', updateOrderSuggestion);
        }
        
        // Form validation
        bindFormValidation();
    }
    
    // Handle form submission
    function handleFormSubmit(e) {
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (in case of server errors)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 10000);
        }
    }
    
    // Update order suggestion based on selected subject
    function updateOrderSuggestion() {
        const subjectSelect = document.getElementById('id_subject');
        const orderInput = document.getElementById('id_order');
        
        if (!subjectSelect || !orderInput || orderInput.value !== '0') {
            return;
        }
        
        const subjectId = subjectSelect.value;
        if (!subjectId) {
            return;
        }
        
        // Make AJAX call to get suggested order
        if (window.staffUrls && window.staffUrls.getSubjectTopics) {
            const url = window.staffUrls.getSubjectTopics.replace('0', subjectId);
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.topics) {
                        const maxOrder = Math.max(0, ...data.topics.map(t => t.order || 0));
                        orderInput.value = maxOrder + 1;
                        orderInput.placeholder = `Suggested: ${maxOrder + 1}`;
                    }
                })
                .catch(error => {
                    console.log('Could not get order suggestion:', error);
                });
        }
    }
    
    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Clear previous errors
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
        document.querySelectorAll('.invalid-feedback').forEach(el => {
            el.style.display = 'none';
        });
        
        // Validate subject
        const subjectSelect = document.getElementById('id_subject');
        if (!subjectSelect.value.trim()) {
            showFieldError(subjectSelect, 'Please select a subject');
            isValid = false;
        }
        
        // Validate name
        const nameInput = document.getElementById('id_name');
        if (!nameInput.value.trim()) {
            showFieldError(nameInput, 'Topic name is required');
            isValid = false;
        } else if (nameInput.value.trim().length < 2) {
            showFieldError(nameInput, 'Topic name must be at least 2 characters long');
            isValid = false;
        }
        
        // Validate order
        const orderInput = document.getElementById('id_order');
        const orderValue = parseInt(orderInput.value);
        if (orderInput.value !== '' && (isNaN(orderValue) || orderValue < 0)) {
            showFieldError(orderInput, 'Order must be a non-negative number');
            isValid = false;
        }
        
        return isValid;
    }
    
    // Show field error
    function showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        
        feedback.textContent = message;
        feedback.style.display = 'block';
    }
    
    // Bind real-time form validation
    function bindFormValidation() {
        // Real-time validation for name field
        const nameInput = document.getElementById('id_name');
        if (nameInput) {
            nameInput.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    if (this.value.trim().length >= 2) {
                        this.classList.remove('is-invalid');
                        const feedback = this.parentNode.querySelector('.invalid-feedback');
                        if (feedback) {
                            feedback.style.display = 'none';
                        }
                    }
                }
            });
        }
        
        // Real-time validation for subject
        const subjectSelect = document.getElementById('id_subject');
        if (subjectSelect) {
            subjectSelect.addEventListener('change', function() {
                if (this.classList.contains('is-invalid')) {
                    if (this.value.trim()) {
                        this.classList.remove('is-invalid');
                        const feedback = this.parentNode.querySelector('.invalid-feedback');
                        if (feedback) {
                            feedback.style.display = 'none';
                        }
                    }
                }
            });
        }
        
        // Real-time validation for order
        const orderInput = document.getElementById('id_order');
        if (orderInput) {
            orderInput.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    const value = parseInt(this.value);
                    if (this.value === '' || (!isNaN(value) && value >= 0)) {
                        this.classList.remove('is-invalid');
                        const feedback = this.parentNode.querySelector('.invalid-feedback');
                        if (feedback) {
                            feedback.style.display = 'none';
                        }
                    }
                }
            });
        }
    }
    
})();
