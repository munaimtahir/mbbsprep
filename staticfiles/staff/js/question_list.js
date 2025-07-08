// MCQ List Page JavaScript

// Initialize tooltips and event delegation
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Event delegation for dynamically added elements
    setupEventDelegation();
});

// Setup event delegation for inline event handlers
function setupEventDelegation() {
    // Bulk action buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.bulk-action-btn[data-action]')) {
            e.preventDefault();
            const action = e.target.getAttribute('data-action');
            bulkAction(action);
        }
    });

    // Toggle status buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.toggle-status-btn[data-question-id]')) {
            e.preventDefault();
            const questionId = e.target.getAttribute('data-question-id');
            toggleStatus(questionId);
        }
    });

    // Delete question buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.delete-question-btn[data-question-id]')) {
            e.preventDefault();
            const questionId = e.target.getAttribute('data-question-id');
            deleteQuestion(questionId);
        }
    });
}

// Bulk selection functionality
document.getElementById('selectAll').addEventListener('change', function() {
    const checkboxes = document.querySelectorAll('.question-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });
    updateBulkActions();
});

document.querySelectorAll('.question-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', updateBulkActions);
});

function updateBulkActions() {
    const selected = document.querySelectorAll('.question-checkbox:checked').length;
    const bulkActions = document.getElementById('bulkActions');
    const selectedCount = document.getElementById('selectedCount');
    
    selectedCount.textContent = selected;
    
    if (selected > 0) {
        bulkActions.classList.add('show');
    } else {
        bulkActions.classList.remove('show');
    }
}

// Subject-Topic filtering
document.getElementById('subjectFilter').addEventListener('change', function() {
    const subjectId = this.value;
    const topicFilter = document.getElementById('topicFilter');
    
    if (subjectId) {
        // Get topics for selected subject via AJAX
        const topicsUrl = window.staffUrls.getTopicsAjax + '?subject_id=' + subjectId;
        fetch(topicsUrl)
            .then(response => response.json())
            .then(data => {
                topicFilter.innerHTML = '<option value="">All Topics</option>';
                data.topics.forEach(topic => {
                    topicFilter.innerHTML += `<option value="${topic.id}">${topic.name}</option>`;
                });
            })
            .catch(error => {
                console.error('Error fetching topics:', error);
                topicFilter.innerHTML = '<option value="">All Topics</option>';
            });
    } else {
        topicFilter.innerHTML = '<option value="">All Topics</option>';
    }
});

// Toggle question status
function toggleStatus(questionId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    fetch(window.staffUrls.questionToggleStatus, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `question_id=${questionId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error toggling status:', error);
        alert('An error occurred while updating the question status.');
    });
}

// Delete question
function deleteQuestion(questionId) {
    if (confirm('Are you sure you want to delete this MCQ? This action cannot be undone.')) {
        window.location.href = window.staffUrls.questionDelete.replace('0', questionId);
    }
}

// Bulk actions
function bulkAction(action) {
    const selected = Array.from(document.querySelectorAll('.question-checkbox:checked')).map(cb => cb.value);
    
    if (selected.length === 0) {
        alert('Please select at least one MCQ.');
        return;
    }
    
    let confirmMessage = '';
    switch(action) {
        case 'delete':
            confirmMessage = `Are you sure you want to delete ${selected.length} MCQ(s)? This action cannot be undone.`;
            break;
        case 'activate':
            confirmMessage = `Activate ${selected.length} MCQ(s)?`;
            break;
        case 'deactivate':
            confirmMessage = `Deactivate ${selected.length} MCQ(s)?`;
            break;
        default:
            confirmMessage = `Apply this action to ${selected.length} MCQ(s)?`;
    }
    
    if (confirm(confirmMessage)) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const formData = new FormData();
        formData.append('action', action);
        formData.append('csrfmiddlewaretoken', csrfToken);
        selected.forEach(id => formData.append('question_ids', id));
        
        fetch(window.staffUrls.questionBulkAction, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error performing bulk action:', error);
            alert('An error occurred while performing the bulk action.');
        });
    }
}

// Auto-submit form on filter change (optional)
document.querySelectorAll('#filterForm select').forEach(select => {
    select.addEventListener('change', function() {
        // Uncomment the line below to auto-submit on filter change
        // document.getElementById('filterForm').submit();
    });
});
