// Add MCQ Page JavaScript

let optionCount = 4; // Start with 4 options (A, B, C, D)

// Initialize form and event delegation
document.addEventListener('DOMContentLoaded', function() {
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

    // Setup event delegation for inline event handlers
    setupEventDelegation();
    
    // Setup tag preview functionality
    setupTagPreview();
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

    // Reset form button
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn-reset') || e.target.closest('.btn-reset')) {
            e.preventDefault();
            resetForm();
        }
    });
}

// Fetch topics based on selected subject
function fetchTopics(subjectId) {
    const topicSelect = document.getElementById('id_topic');
    
    topicSelect.innerHTML = '<option value="">Loading topics...</option>';
    
    const topicsUrl = window.staffUrls.getTopicsAjax + '?subject_id=' + subjectId;
    fetch(topicsUrl)
        .then(response => response.json())
        .then(data => {
            topicSelect.innerHTML = '<option value="">Select Topic</option>';
            data.topics.forEach(topic => {
                topicSelect.innerHTML += `<option value="${topic.id}">${topic.name}</option>`;
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
    
    const optionSection = document.querySelector('.option-section');
    const addButton = document.getElementById('addOptionBtn');
    
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
    const optionHtml = `
        <div class="option-row" data-option-index="${optionCount}">
            <div class="option-label">${letters[optionCount]}</div>
            <div class="option-input">
                <input type="text" name="option_${optionCount}_text" 
                       class="form-control form-control-lg option-input" 
                       placeholder="Enter option ${letters[optionCount]} text..." required>
            </div>
            <div class="correct-radio">
                <input type="radio" name="correct_answer" value="${optionCount}" 
                       class="form-check-input" id="correct_${optionCount}">
                <label for="correct_${optionCount}" class="correct-indicator">
                    <i class="fas fa-check-circle"></i> Correct
                </label>
            </div>
            <button type="button" class="remove-option">
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
        
        label.textContent = letters[index];
        radio.value = index;
        radio.id = `correct_${index}`;
        radioLabel.setAttribute('for', `correct_${index}`);
        textInput.name = `option_${index}_text`;
        textInput.placeholder = `Enter option ${letters[index]} text...`;
        row.setAttribute('data-option-index', index);
    });
    
    // Update optionCount to match actual count
    optionCount = optionRows.length;
}

// Reset form
function resetForm() {
    if (confirm('Are you sure you want to reset the form? All entered data will be lost.')) {
        document.getElementById('mcqForm').reset();
        
        // Reset to 4 options
        const optionSection = document.querySelector('.option-section');
        const optionRows = optionSection.querySelectorAll('.option-row');
        
        // Remove extra options beyond 4
        optionRows.forEach((row, index) => {
            if (index >= 4) {
                row.remove();
            }
        });
        
        optionCount = 4;
        document.getElementById('addOptionBtn').style.display = 'block';
        
        // Clear topic dropdown
        const topicSelect = document.getElementById('id_topic');
        if (topicSelect) {
            topicSelect.innerHTML = '<option value="">Select Topic (choose subject first)</option>';
        }
    }
}

// Form submission with validation and loading state
document.getElementById('mcqForm').addEventListener('submit', function(e) {
    const submitBtn = document.querySelector('.btn-add-mcq');
    const spinner = submitBtn.querySelector('.loading-spinner');
    
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
    submitBtn.disabled = true;
    if (spinner) {
        spinner.style.display = 'inline-block';
    }
});

// Real-time validation feedback
document.addEventListener('input', function(e) {
    if (e.target.matches('input, select, textarea')) {
        if (e.target.value.trim()) {
            e.target.style.borderColor = '#E3E7ED';
        }
    }
});

// Auto-save functionality (optional)
setInterval(function() {
    const formData = new FormData(document.getElementById('mcqForm'));
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    localStorage.setItem('mcq_draft_' + Date.now(), JSON.stringify(data));
}, 30000); // Save every 30 seconds

// Load draft on page load
window.addEventListener('load', function() {
    const drafts = Object.keys(localStorage).filter(key => key.startsWith('mcq_draft_'));
    if (drafts.length > 0 && confirm('Would you like to load your last saved draft?')) {
        const latestDraft = drafts.sort().pop();
        const data = JSON.parse(localStorage.getItem(latestDraft));
        
        Object.keys(data).forEach(key => {
            const input = document.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
                if (input.type === 'radio' && input.value === data[key]) {
                    input.checked = true;
                }
            }
        });
        
        // Clean up old drafts
        drafts.forEach(draft => localStorage.removeItem(draft));
    }
});

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
