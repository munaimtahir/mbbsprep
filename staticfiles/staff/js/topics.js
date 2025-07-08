// Topics Management JavaScript
(function() {
    'use strict';
    
    let currentTopicId = null;
    let topicModal = null;
    let confirmModal = null;
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Debug URLs
        console.log('Topics page loaded, URLs:', window.staffUrls);
        
        initializeModals();
        bindEventHandlers();
        initializeSearch();
        initializeFilters();
    });
    
    // Initialize Bootstrap modals
    function initializeModals() {
        const topicModalEl = document.getElementById('topicModal');
        const confirmModalEl = document.getElementById('confirmModal');
        
        if (topicModalEl) {
            topicModal = new bootstrap.Modal(topicModalEl);
        }
        
        if (confirmModalEl) {
            confirmModal = new bootstrap.Modal(confirmModalEl);
        }
    }
    
    // Bind all event handlers
    function bindEventHandlers() {
        // Add topic buttons
        bindElement('#addTopicBtn', 'click', showAddTopicModal);
        bindElement('#addFirstTopicBtn', 'click', showAddTopicModal);
        
        // Save topic button
        bindElement('#saveTopicBtn', 'click', saveTopic);
        
        // Topic actions (edit, archive, restore) - use event delegation
        document.addEventListener('click', function(e) {
            const target = e.target.closest('.btn-edit, .btn-archive, .btn-restore');
            if (!target) return;
            
            if (target.classList.contains('btn-edit')) {
                handleEditTopic(e);
            } else if (target.classList.contains('btn-archive')) {
                handleArchiveTopic(e);
            } else if (target.classList.contains('btn-restore')) {
                handleRestoreTopic(e);
            }
        });
        
        // Modal events
        const topicModalEl = document.getElementById('topicModal');
        if (topicModalEl) {
            topicModalEl.addEventListener('hidden.bs.modal', resetTopicForm);
        }
        
        // Form submission
        bindElement('#topicForm', 'submit', function(e) {
            e.preventDefault();
            saveTopic();
        });
    }
    
    // Utility function to bind events with optional delegation
    function bindElement(selector, event, handler, delegate = false) {
        if (delegate) {
            document.addEventListener(event, function(e) {
                if (e.target.matches(selector) || e.target.closest(selector)) {
                    const target = e.target.matches(selector) ? e.target : e.target.closest(selector);
                    const newEvent = Object.create(e);
                    newEvent.target = target;
                    handler(newEvent);
                }
            });
        } else {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.addEventListener(event, handler));
        }
    }
    
    // Initialize search functionality
    function initializeSearch() {
        const searchInput = document.getElementById('searchInput');
        
        if (searchInput) {
            const debouncedSearch = TopicsUtils.debounce(performSearch, 300);
            searchInput.addEventListener('input', debouncedSearch);
        }
    }
    
    // Initialize filters
    function initializeFilters() {
        const subjectFilter = document.getElementById('subjectFilter');
        const statusFilter = document.getElementById('statusFilter');
        
        if (subjectFilter) {
            subjectFilter.addEventListener('change', performSearch);
        }
        
        if (statusFilter) {
            statusFilter.addEventListener('change', performSearch);
        }
    }
    
    // Perform search and filter
    function performSearch() {
        const searchValue = document.getElementById('searchInput')?.value || '';
        const subjectValue = document.getElementById('subjectFilter')?.value || '';
        const statusValue = document.getElementById('statusFilter')?.value || '';
        
        // Update URL parameters
        TopicsUtils.updateUrlParams({
            search: searchValue,
            subject: subjectValue,
            status: statusValue,
            page: '' // Reset to first page
        });
        
        // Reload page with new parameters
        window.location.reload();
    }
    
    // Show add topic modal
    function showAddTopicModal() {
        resetTopicForm();
        document.getElementById('topicModalLabel').textContent = 'Add Topic';
        document.getElementById('saveTopicBtn').innerHTML = '<i class="fas fa-save me-2"></i>Save Topic';
        
        // Pre-select subject if filtering by one
        const subjectFilter = document.getElementById('subjectFilter');
        const topicSubject = document.getElementById('topicSubject');
        if (subjectFilter && topicSubject && subjectFilter.value) {
            topicSubject.value = subjectFilter.value;
        }
        
        topicModal.show();
    }
    
    // Handle edit topic
    function handleEditTopic(e) {
        const topicId = e.target.closest('[data-topic-id]').getAttribute('data-topic-id');
        loadTopicForEdit(topicId);
    }
    
    // Load topic data for editing
    function loadTopicForEdit(topicId) {
        const url = window.staffUrls.topicEdit.replace('0', topicId);
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': TopicsUtils.getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateTopicForm(data.topic);
                document.getElementById('topicModalLabel').textContent = 'Edit Topic';
                document.getElementById('saveTopicBtn').innerHTML = '<i class="fas fa-save me-2"></i>Update Topic';
                topicModal.show();
            } else {
                TopicsUtils.showToast(data.message || 'Error loading topic', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            TopicsUtils.showToast('Error loading topic data', 'error');
        });
    }
    
    // Populate topic form with data
    function populateTopicForm(topic) {
        currentTopicId = topic.id;
        document.getElementById('topicId').value = topic.id;
        document.getElementById('topicName').value = topic.name;
        document.getElementById('topicSubject').value = topic.subject_id;
        document.getElementById('topicDescription').value = topic.description || '';
        document.getElementById('topicOrder').value = topic.order || 0;
        document.getElementById('topicStatus').value = topic.is_active ? 'true' : 'false';
    }
    
    // Save topic
    function saveTopic() {
        const form = document.getElementById('topicForm');
        const formData = new FormData(form);
        
        // Validation
        const name = formData.get('name').trim();
        const subjectId = formData.get('subject_id');
        
        if (!name) {
            TopicsUtils.showToast('Topic name is required', 'error');
            document.getElementById('topicName').focus();
            return;
        }
        
        if (!subjectId) {
            TopicsUtils.showToast('Subject is required', 'error');
            document.getElementById('topicSubject').focus();
            return;
        }
        
        // Determine if it's create or update
        const isEdit = currentTopicId !== null;
        const url = isEdit ? 
            window.staffUrls.topicEdit.replace('0', currentTopicId) : 
            window.staffUrls.topicCreate;
        
        formData.append('csrfmiddlewaretoken', TopicsUtils.getCSRFToken());
        
        // Show loading state
        const saveBtn = document.getElementById('saveTopicBtn');
        showButtonLoading(saveBtn);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': TopicsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideButtonLoading(saveBtn);
            
            if (data.success) {
                topicModal.hide();
                TopicsUtils.showToast(data.message, 'success');
                
                // Reload the page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                TopicsUtils.showToast(data.message || 'Error saving topic', 'error');
            }
        })
        .catch(error => {
            hideButtonLoading(saveBtn);
            console.error('Error:', error);
            TopicsUtils.showToast('Error saving topic', 'error');
        });
    }
    
    // Handle archive topic
    function handleArchiveTopic(e) {
        const topicId = e.target.closest('[data-topic-id]').getAttribute('data-topic-id');
        const topicName = e.target.closest('tr').querySelector('.topic-name').textContent;
        
        showConfirmDialog(
            'Archive Topic',
            `Are you sure you want to archive "${topicName}"? This will hide it from active lists but preserve all MCQs.`,
            'Archive',
            () => toggleTopicStatus(topicId, 'archive')
        );
    }
    
    // Handle restore topic
    function handleRestoreTopic(e) {
        const topicId = e.target.closest('[data-topic-id]').getAttribute('data-topic-id');
        const topicName = e.target.closest('tr').querySelector('.topic-name').textContent;
        
        showConfirmDialog(
            'Restore Topic',
            `Are you sure you want to restore "${topicName}"? This will make it active again.`,
            'Restore',
            () => toggleTopicStatus(topicId, 'restore')
        );
    }
    
    // Show confirmation dialog
    function showConfirmDialog(title, message, actionText, callback) {
        document.getElementById('confirmModalLabel').textContent = title;
        document.getElementById('confirmModalBody').textContent = message;
        
        const confirmBtn = document.getElementById('confirmActionBtn');
        confirmBtn.textContent = actionText;
        confirmBtn.className = actionText === 'Archive' ? 'btn btn-danger' : 'btn btn-primary';
        
        // Remove existing listeners and add new one
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        newConfirmBtn.addEventListener('click', () => {
            confirmModal.hide();
            callback();
        });
        
        confirmModal.show();
    }
    
    // Toggle topic status (archive/restore)
    function toggleTopicStatus(topicId, action) {
        const formData = new FormData();
        formData.append('topic_id', topicId);
        formData.append('action', action);
        formData.append('csrfmiddlewaretoken', TopicsUtils.getCSRFToken());
        
        fetch(window.staffUrls.topicToggleStatus, {
            method: 'POST',
            headers: {
                'X-CSRFToken': TopicsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                TopicsUtils.showToast(data.message, 'success');
                
                // Update the row in place
                updateTopicRow(data.topic_id, data.is_active);
            } else {
                TopicsUtils.showToast(data.message || 'Error updating topic status', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            TopicsUtils.showToast('Error updating topic status', 'error');
        });
    }
    
    // Update topic row after status change
    function updateTopicRow(topicId, isActive) {
        const row = document.querySelector(`[data-topic-id="${topicId}"]`);
        if (!row) return;
        
        // Update data attribute
        row.setAttribute('data-status', isActive ? 'active' : 'archived');
        
        // Update status badge
        const statusCell = row.querySelector('.topic-status');
        const statusBadge = statusCell.querySelector('.status-badge');
        
        if (isActive) {
            statusBadge.className = 'status-badge status-active';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Active';
        } else {
            statusBadge.className = 'status-badge status-archived';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Archived';
        }
        
        // Update actions
        const actionsCell = row.querySelector('.topic-actions');
        
        if (isActive) {
            // Show archive button
            const restoreBtn = actionsCell.querySelector('.btn-restore');
            if (restoreBtn) {
                restoreBtn.className = 'btn-action btn-archive';
                restoreBtn.innerHTML = '<i class="fas fa-archive"></i> Archive';
                restoreBtn.setAttribute('data-topic-id', topicId);
            }
        } else {
            // Show restore button
            const archiveBtn = actionsCell.querySelector('.btn-archive');
            if (archiveBtn) {
                archiveBtn.className = 'btn-action btn-restore';
                archiveBtn.innerHTML = '<i class="fas fa-undo"></i> Restore';
                archiveBtn.setAttribute('data-topic-id', topicId);
            }
        }
    }
    
    // Reset topic form
    function resetTopicForm() {
        currentTopicId = null;
        document.getElementById('topicForm').reset();
        document.getElementById('topicId').value = '';
    }
    
    // Show button loading state
    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.classList.add('loading');
        button.disabled = true;
        
        // Store original text
        button.dataset.originalText = originalText;
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
    
})();
