// Edit MCQ Page JavaScript

// Initialize optionCount from template data or default
let optionCount = 4; // Will be set from template

// Initialize form and event delegation
document.addEventListener('DOMContentLoaded', function() {
    // Get initial data from template
    if (window.mcqEditData) {
        optionCount = window.mcqEditData.optionCount || 4;
    }
    
    // Set up subject-topic relationship
    const subjectSelect = document.getElementById('id_subject');
    const topicSelect = document.getElementById('id_topic');
    
    if (subjectSelect && topicSelect) {
        subjectSelect.addEventListener('change', function() {
            const subjectId = this.value;
            if (subjectId) {
                fetchTopics(subjectId);
            } else {
                topicSelect.innerHTML = '<option value="">Select Topic (choose subject first)</option>';
            }
        });
    }
    
    // Update option labels and count actual options
    const existingOptions = document.querySelectorAll('.option-row');
    optionCount = existingOptions.length;
    updateOptionLabels();

    // Setup event delegation for inline event handlers
    setupEventDelegation();
    
    // Setup tag preview functionality
    setupTagPreview();
});

// Setup event delegation for inline event handlers
function setupEventDelegation() {
    // Add option button
    document.addEventListener('click', function(e) {
        if (e.target.matches('#addOptionBtn') || e.target.closest('#addOptionBtn')) {
            e.preventDefault();
            addOption();
        }
    });

    // Remove option buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.remove-option') || e.target.closest('.remove-option')) {
            e.preventDefault();
            const button = e.target.closest('.remove-option');
            removeOption(button);
        }
    });

    // Delete MCQ button
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn-delete-mcq') || e.target.closest('.btn-delete-mcq')) {
            e.preventDefault();
            confirmDelete();
        }
    });

    // Toggle revision log
    document.addEventListener('click', function(e) {
        if (e.target.matches('.revision-header') || e.target.closest('.revision-header')) {
            e.preventDefault();
            toggleRevisionLog();
        }
    });
}

// Fetch topics based on selected subject
function fetchTopics(subjectId) {
    const topicSelect = document.getElementById('id_topic');
    const currentTopicId = window.mcqEditData ? window.mcqEditData.currentTopicId : null;
    
    topicSelect.innerHTML = '<option value="">Loading topics...</option>';
    
    const topicsUrl = window.staffUrls.getTopicsAjax + '?subject_id=' + subjectId;
    fetch(topicsUrl)
        .then(response => response.json())
        .then(data => {
            topicSelect.innerHTML = '<option value="">Select Topic</option>';
            data.topics.forEach(topic => {
                const selected = topic.id == currentTopicId ? 'selected' : '';
                topicSelect.innerHTML += `<option value="${topic.id}" ${selected}>${topic.name}</option>`;
            });
        })
        .catch(error => {
            console.error('Error fetching topics:', error);
            topicSelect.innerHTML = '<option value="">Error loading topics</option>';
        });
}

// Add new option
function addOption() {
    if (optionCount >= 6) {
        alert('Maximum 6 options allowed');
        return;
    }
    
    const optionSection = document.getElementById('optionsSection');
    const addButton = document.getElementById('addOptionBtn');
    
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
    const optionHtml = `
        <div class="option-row" data-option-index="${optionCount}">
            <div class="option-label">${letters[optionCount]}</div>
            <div class="option-input">
                <input type="text" name="option_${optionCount}_text" 
                       class="form-control form-control-lg" 
                       placeholder="Enter option ${letters[optionCount]} text..." required>
            </div>
            <div class="correct-radio">
                <input type="radio" name="correct_answer" value="${optionCount}" 
                       class="form-check-input" id="correct_${optionCount}">
                <label for="correct_${optionCount}" class="correct-indicator">
                    <i class="fas fa-check-circle"></i> Correct
                </label>
            </div>
            <button type="button" class="btn btn-outline-danger btn-sm remove-option">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    addButton.insertAdjacentHTML('beforebegin', optionHtml);
    optionCount++;
    
    if (optionCount >= 6) {
        addButton.style.display = 'none';
    }
}

// Remove option
function removeOption(button) {
    if (optionCount <= 2) {
        alert('Minimum 2 options required');
        return;
    }
    
    const optionRow = button.closest('.option-row');
    optionRow.remove();
    optionCount--;
    
    // Show add button if hidden
    const addButton = document.getElementById('addOptionBtn');
    if (optionCount < 6) {
        addButton.style.display = 'block';
    }
    
    // Update option labels and indices
    updateOptionLabels();
}

// Update option labels after removal
function updateOptionLabels() {
    const optionRows = document.querySelectorAll('.option-row');
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
    
    optionRows.forEach((row, index) => {
        const label = row.querySelector('.option-label');
        const radio = row.querySelector('input[type="radio"]');
        const radioLabel = row.querySelector('label[for^="correct_"]');
        const textInput = row.querySelector('input[type="text"]');
        
        if (label) label.textContent = letters[index];
        if (radio) {
            radio.value = index;
            radio.id = `correct_${index}`;
        }
        if (radioLabel) {
            radioLabel.setAttribute('for', `correct_${index}`);
        }
        if (textInput) {
            textInput.name = `option_${index}_text`;
            textInput.placeholder = `Enter option ${letters[index]} text...`;
        }
        row.setAttribute('data-option-index', index);
        
        // Update correct option styling
        if (radio && radio.checked) {
            row.classList.add('correct-option');
        } else {
            row.classList.remove('correct-option');
        }
    });
    
    // Update optionCount to match actual count
    optionCount = optionRows.length;
}

// Handle correct answer selection
document.addEventListener('change', function(e) {
    if (e.target.name === 'correct_answer') {
        // Remove correct styling from all options
        document.querySelectorAll('.option-row').forEach(row => {
            row.classList.remove('correct-option');
        });
        
        // Add correct styling to selected option
        const selectedRow = e.target.closest('.option-row');
        if (selectedRow) {
            selectedRow.classList.add('correct-option');
        }
    }
});

// Confirm delete function
function confirmDelete() {
    const modal = document.getElementById('deleteModal');
    if (modal && typeof bootstrap !== 'undefined') {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    } else {
        // Fallback if Bootstrap modal is not available
        if (confirm('Are you sure you want to delete this MCQ? This action cannot be undone.')) {
            const deleteForm = document.querySelector('form[action*="delete"]');
            if (deleteForm) {
                deleteForm.submit();
            }
        }
    }
}

// Form submission with validation and loading state
document.addEventListener('DOMContentLoaded', function() {
    const mcqEditForm = document.getElementById('mcqEditForm');
    
    if (mcqEditForm) {
        mcqEditForm.addEventListener('submit', function(e) {
            const submitBtn = document.querySelector('.btn-save-mcq');
            const spinner = submitBtn && submitBtn.querySelector('.loading-spinner');
            
            // Validate required fields
            let isValid = true;
            const requiredFields = ['id_subject', 'id_topic', 'id_question_text', 'id_difficulty'];
            
            requiredFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field && !field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#FF7043';
                } else if (field) {
                    field.style.borderColor = '#E3E7ED';
                }
            });
            
            // Validate options
            const optionInputs = document.querySelectorAll('input[name*="_text"]');
            let filledOptions = 0;
            
            optionInputs.forEach(input => {
                if (input.value.trim()) {
                    filledOptions++;
                    input.style.borderColor = '#E3E7ED';
                } else {
                    input.style.borderColor = '#FF7043';
                }
            });
            
            if (filledOptions < 2) {
                isValid = false;
                alert('Please provide at least 2 answer options.');
                e.preventDefault();
                return;
            }
            
            // Check if at least one correct answer is selected
            const correctAnswers = document.querySelectorAll('input[name="correct_answer"]:checked');
            if (correctAnswers.length === 0) {
                isValid = false;
                alert('Please select the correct answer option.');
                e.preventDefault();
                return;
            }
            
            if (!isValid) {
                alert('Please fill in all required fields.');
                e.preventDefault();
                return;
            }
            
            // Show loading state
            if (e.target.matches('button[name="save_changes"]') || (e.submitter && e.submitter.name === 'save_changes')) {
                if (submitBtn) submitBtn.disabled = true;
                if (spinner) {
                    spinner.style.display = 'inline-block';
                }
            }
        });
    }
});

// Revision log toggle (for future implementation)
function toggleRevisionLog() {
    const content = document.getElementById('revisionContent');
    const icon = document.getElementById('revisionToggleIcon');
    
    if (content && icon) {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            content.style.display = 'none';
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    }
}

// Real-time validation feedback
document.addEventListener('input', function(e) {
    if (e.target.matches('input, select, textarea')) {
        if (e.target.value.trim()) {
            e.target.style.borderColor = '#E3E7ED';
        }
    }
});

// Auto-dismiss alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        if (alert.querySelector('.btn-close')) {
            alert.querySelector('.btn-close').click();
        }
    });
}, 5000);

// Tag preview functionality
function setupTagPreview() {
    const newTagsInput = document.getElementById('id_new_tags');
    const tagPreview = document.getElementById('tagPreview');
    const tagPreviewContainer = document.getElementById('tagPreviewContainer');
    
    if (newTagsInput && tagPreview && tagPreviewContainer) {
        newTagsInput.addEventListener('input', function() {
            const value = this.value.trim();
            
            if (value) {
                // Split by comma and create preview chips
                const tagNames = value.split(',').map(name => name.trim()).filter(name => name);
                
                if (tagNames.length > 0) {
                    tagPreviewContainer.innerHTML = '';
                    tagNames.forEach(tagName => {
                        const chip = document.createElement('span');
                        chip.className = 'tag-preview-chip';
                        chip.textContent = tagName;
                        tagPreviewContainer.appendChild(chip);
                    });
                    tagPreview.style.display = 'block';
                } else {
                    tagPreview.style.display = 'none';
                }
            } else {
                tagPreview.style.display = 'none';
            }
        });
    }
}
