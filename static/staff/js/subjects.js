// Subjects Management JavaScript
(function() {
    'use strict';
    
    let currentSubjectId = null;
    let subjectModal = null;
    let confirmModal = null;
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeModals();
        bindEventHandlers();
        initializeSearch();
    });
    
    // Initialize Bootstrap modals
    function initializeModals() {
        const subjectModalEl = document.getElementById('subjectModal');
        const confirmModalEl = document.getElementById('confirmModal');
        
        if (subjectModalEl) {
            subjectModal = new bootstrap.Modal(subjectModalEl);
        }
        
        if (confirmModalEl) {
            confirmModal = new bootstrap.Modal(confirmModalEl);
        }
    }
    
    // Bind all event handlers
    function bindEventHandlers() {
        // Add subject buttons
        bindElement('#addSubjectBtn', 'click', showAddSubjectModal);
        bindElement('#addFirstSubjectBtn', 'click', showAddSubjectModal);
        
        // Save subject button
        bindElement('#saveSubjectBtn', 'click', saveSubject);
        
        // Subject actions (edit, archive, restore) - with delegation
        bindActionButtons();
        
        // Topic management
        bindElement('#addTopicBtn', 'click', showAddTopicForm);
        bindElement('#saveTopicBtn', 'click', saveTopic);
        bindElement('#cancelTopicBtn', 'click', hideAddTopicForm);
        
        // Modal events
        const subjectModalEl = document.getElementById('subjectModal');
        if (subjectModalEl) {
            subjectModalEl.addEventListener('hidden.bs.modal', resetSubjectForm);
        }
        
        // Form submission
        bindElement('#subjectForm', 'submit', function(e) {
            e.preventDefault();
            saveSubject();
        });
        
        // Enter key on new topic input
        bindElement('#newTopicName', 'keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveTopic();
            }
        });
    }
    
    // Utility function to bind events with optional delegation
    function bindElement(selector, event, handler, delegate = false) {
        if (delegate) {
            document.addEventListener(event, function(e) {
                if (e.target.matches(selector)) {
                    handler(e);
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
        const statusFilter = document.getElementById('statusFilter');
        
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(performSearch, 300);
            });
        }
        
        if (statusFilter) {
            statusFilter.addEventListener('change', performSearch);
        }
    }
    
    // Perform search and filter
    function performSearch() {
        const searchValue = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const statusValue = document.getElementById('statusFilter')?.value || '';
        
        const rows = document.querySelectorAll('.subject-row');
        
        rows.forEach(row => {
            const subjectName = row.querySelector('.subject-name')?.textContent.toLowerCase() || '';
            const subjectStatus = row.getAttribute('data-status') || '';
            
            const matchesSearch = !searchValue || subjectName.includes(searchValue);
            const matchesStatus = !statusValue || subjectStatus === statusValue;
            
            if (matchesSearch && matchesStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update row numbers
        updateRowNumbers();
    }
    
    // Update row numbers after filtering
    function updateRowNumbers() {
        const visibleRows = document.querySelectorAll('.subject-row[style=""], .subject-row:not([style])');
        visibleRows.forEach((row, index) => {
            const numberCell = row.querySelector('.subject-number');
            if (numberCell) {
                numberCell.textContent = index + 1;
            }
        });
    }
    
    // Show add subject modal
    function showAddSubjectModal() {
        resetSubjectForm();
        document.getElementById('subjectModalLabel').textContent = 'Add Subject';
        document.getElementById('saveSubjectBtn').innerHTML = '<i class="fas fa-save me-2"></i>Save Subject';
        document.getElementById('topicsSection').style.display = 'none';
        subjectModal.show();
    }
    
    // Handle edit subject
    function handleEditSubject(e) {
        const subjectId = e.target.closest('[data-subject-id]').getAttribute('data-subject-id');
        loadSubjectForEdit(subjectId);
    }
    
    // Load subject data for editing
    function loadSubjectForEdit(subjectId) {
        const url = window.staffUrls.subjectEdit.replace('0', subjectId);
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateSubjectForm(data.subject);
                document.getElementById('subjectModalLabel').textContent = 'Edit Subject';
                document.getElementById('saveSubjectBtn').innerHTML = '<i class="fas fa-save me-2"></i>Update Subject';
                document.getElementById('topicsSection').style.display = 'block';
                loadSubjectTopics(subjectId);
                subjectModal.show();
            } else {
                SubjectsUtils.showToast(data.message || 'Error loading subject', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            SubjectsUtils.showToast('Error loading subject data', 'error');
        });
    }
    
    // Populate subject form with data
    function populateSubjectForm(subject) {
        currentSubjectId = subject.id;
        document.getElementById('subjectId').value = subject.id;
        document.getElementById('subjectName').value = subject.name;
        document.getElementById('subjectCode').value = subject.code || '';
        document.getElementById('subjectDescription').value = subject.description || '';
        document.getElementById('subjectStatus').value = subject.is_active ? 'true' : 'false';
    }
    
    // Load topics for a subject
    function loadSubjectTopics(subjectId) {
        const url = window.staffUrls.getSubjectTopics.replace('0', subjectId);
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateTopicsTable(data.topics);
            } else {
                console.error('Error loading topics:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading topics:', error);
        });
    }
    
    // Populate topics table
    function populateTopicsTable(topics) {
        const tbody = document.getElementById('topicsTableBody');
        tbody.innerHTML = '';
        
        if (topics.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-muted">
                        <i class="fas fa-list me-2"></i>No topics yet
                    </td>
                </tr>
            `;
            return;
        }
        
        topics.forEach((topic, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>
                    <span class="topic-name" data-topic-id="${topic.id}">${SubjectsUtils.escapeHtml(topic.name)}</span>
                    <input type="text" class="form-control form-control-sm topic-edit-input" 
                           value="${SubjectsUtils.escapeHtml(topic.name)}" style="display: none;">
                </td>
                <td>
                    <span class="count-badge">${SubjectsUtils.formatCount(topic.question_count)}</span>
                </td>
                <td>
                    <button type="button" class="btn btn-sm btn-outline-primary topic-edit-btn" 
                            data-topic-id="${topic.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-success topic-save-btn" 
                            data-topic-id="${topic.id}" style="display: none;">
                        <i class="fas fa-check"></i>
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-secondary topic-cancel-btn" 
                            data-topic-id="${topic.id}" style="display: none;">
                        <i class="fas fa-times"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
        
        // Bind topic edit handlers
        bindTopicEditHandlers();
    }
    
    // Bind topic edit handlers
    function bindTopicEditHandlers() {
        document.querySelectorAll('.topic-edit-btn').forEach(btn => {
            btn.addEventListener('click', handleTopicEdit);
        });
        
        document.querySelectorAll('.topic-save-btn').forEach(btn => {
            btn.addEventListener('click', handleTopicSave);
        });
        
        document.querySelectorAll('.topic-cancel-btn').forEach(btn => {
            btn.addEventListener('click', handleTopicCancel);
        });
        
        document.querySelectorAll('.topic-edit-input').forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const topicId = this.closest('tr').querySelector('.topic-save-btn').getAttribute('data-topic-id');
                    handleTopicSave({ target: { getAttribute: () => topicId } });
                }
            });
        });
    }
    
    // Handle topic edit
    function handleTopicEdit(e) {
        const topicId = e.target.closest('[data-topic-id]').getAttribute('data-topic-id');
        const row = e.target.closest('tr');
        
        const nameSpan = row.querySelector('.topic-name');
        const nameInput = row.querySelector('.topic-edit-input');
        const editBtn = row.querySelector('.topic-edit-btn');
        const saveBtn = row.querySelector('.topic-save-btn');
        const cancelBtn = row.querySelector('.topic-cancel-btn');
        
        nameSpan.style.display = 'none';
        nameInput.style.display = 'block';
        editBtn.style.display = 'none';
        saveBtn.style.display = 'inline-block';
        cancelBtn.style.display = 'inline-block';
        
        nameInput.focus();
        nameInput.select();
    }
    
    // Handle topic save
    function handleTopicSave(e) {
        const topicId = e.target.getAttribute('data-topic-id');
        const row = e.target.closest('tr');
        const nameInput = row.querySelector('.topic-edit-input');
        const newName = nameInput.value.trim();
        
        if (!newName) {
            SubjectsUtils.showToast('Topic name is required', 'error');
            nameInput.focus();
            return;
        }
        
        const url = window.staffUrls.topicEdit.replace('0', topicId);
        const formData = new FormData();
        formData.append('name', newName);
        formData.append('csrfmiddlewaretoken', SubjectsUtils.getCSRFToken());
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const nameSpan = row.querySelector('.topic-name');
                nameSpan.textContent = newName;
                handleTopicCancel(e); // Reset to view mode
                SubjectsUtils.showToast(data.message, 'success');
            } else {
                SubjectsUtils.showToast(data.message || 'Error updating topic', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            SubjectsUtils.showToast('Error updating topic', 'error');
        });
    }
    
    // Handle topic cancel
    function handleTopicCancel(e) {
        const row = e.target.closest('tr');
        
        const nameSpan = row.querySelector('.topic-name');
        const nameInput = row.querySelector('.topic-edit-input');
        const editBtn = row.querySelector('.topic-edit-btn');
        const saveBtn = row.querySelector('.topic-save-btn');
        const cancelBtn = row.querySelector('.topic-cancel-btn');
        
        // Reset input value
        nameInput.value = nameSpan.textContent;
        
        nameSpan.style.display = 'block';
        nameInput.style.display = 'none';
        editBtn.style.display = 'inline-block';
        saveBtn.style.display = 'none';
        cancelBtn.style.display = 'none';
    }
    
    // Show add topic form
    function showAddTopicForm() {
        document.getElementById('addTopicForm').style.display = 'block';
        document.getElementById('newTopicName').focus();
    }
    
    // Hide add topic form
    function hideAddTopicForm() {
        document.getElementById('addTopicForm').style.display = 'none';
        document.getElementById('newTopicName').value = '';
    }
    
    // Save new topic
    function saveTopic() {
        const topicName = document.getElementById('newTopicName').value.trim();
        
        if (!topicName) {
            SubjectsUtils.showToast('Topic name is required', 'error');
            document.getElementById('newTopicName').focus();
            return;
        }
        
        if (!currentSubjectId) {
            SubjectsUtils.showToast('No subject selected', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('subject_id', currentSubjectId);
        formData.append('name', topicName);
        formData.append('csrfmiddlewaretoken', SubjectsUtils.getCSRFToken());
        
        fetch(window.staffUrls.topicCreate, {
            method: 'POST',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                hideAddTopicForm();
                loadSubjectTopics(currentSubjectId); // Reload topics
                SubjectsUtils.showToast(data.message, 'success');
            } else {
                SubjectsUtils.showToast(data.message || 'Error creating topic', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            SubjectsUtils.showToast('Error creating topic', 'error');
        });
    }
    
    // Save subject
    function saveSubject() {
        const form = document.getElementById('subjectForm');
        const formData = new FormData(form);
        
        // Validation
        const name = formData.get('name').trim();
        if (!name) {
            SubjectsUtils.showToast('Subject name is required', 'error');
            document.getElementById('subjectName').focus();
            return;
        }
        
        // Determine if it's create or update
        const isEdit = currentSubjectId !== null;
        const url = isEdit ? 
            window.staffUrls.subjectEdit.replace('0', currentSubjectId) : 
            window.staffUrls.subjectCreate;
        
        formData.append('csrfmiddlewaretoken', SubjectsUtils.getCSRFToken());
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                subjectModal.hide();
                SubjectsUtils.showToast(data.message, 'success');
                
                // Reload the page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                SubjectsUtils.showToast(data.message || 'Error saving subject', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            SubjectsUtils.showToast('Error saving subject', 'error');
        });
    }
    
    // Handle archive subject
    function handleArchiveSubject(e) {
        const subjectId = e.target.closest('[data-subject-id]').getAttribute('data-subject-id');
        const subjectName = e.target.closest('tr').querySelector('.subject-name').textContent;
        
        showConfirmDialog(
            'Archive Subject',
            `Are you sure you want to archive "${subjectName}"? This will hide it from active lists but preserve all data.`,
            'Archive',
            () => toggleSubjectStatus(subjectId, 'archive')
        );
    }
    
    // Handle restore subject
    function handleRestoreSubject(e) {
        const subjectId = e.target.closest('[data-subject-id]').getAttribute('data-subject-id');
        const subjectName = e.target.closest('tr').querySelector('.subject-name').textContent;
        
        showConfirmDialog(
            'Restore Subject',
            `Are you sure you want to restore "${subjectName}"? This will make it active again.`,
            'Restore',
            () => toggleSubjectStatus(subjectId, 'restore')
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
    
    // Toggle subject status (archive/restore)
    function toggleSubjectStatus(subjectId, action) {
        const formData = new FormData();
        formData.append('subject_id', subjectId);
        formData.append('action', action);
        formData.append('csrfmiddlewaretoken', SubjectsUtils.getCSRFToken());
        
        fetch(window.staffUrls.subjectToggleStatus, {
            method: 'POST',
            headers: {
                'X-CSRFToken': SubjectsUtils.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                SubjectsUtils.showToast(data.message, 'success');
                
                // Update the row in place
                updateSubjectRow(data.subject_id, data.is_active);
            } else {
                SubjectsUtils.showToast(data.message || 'Error updating subject status', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            SubjectsUtils.showToast('Error updating subject status', 'error');
        });
    }
    
    // Update subject row after status change
    function updateSubjectRow(subjectId, isActive) {
        const row = document.querySelector(`[data-subject-id="${subjectId}"]`);
        if (!row) return;
        
        // Update data attribute
        row.setAttribute('data-status', isActive ? 'active' : 'archived');
        
        // Update status badge
        const statusCell = row.querySelector('.subject-status');
        const statusBadge = statusCell.querySelector('.status-badge');
        
        if (isActive) {
            statusBadge.className = 'status-badge status-active';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Active';
        } else {
            statusBadge.className = 'status-badge status-archived';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Archived';
        }
        
        // Update actions - Replace the button completely
        const actionsCell = row.querySelector('.subject-actions');
        
        if (isActive) {
            // Replace restore button with archive button
            const restoreBtn = actionsCell.querySelector('.btn-restore');
            if (restoreBtn) {
                restoreBtn.className = 'btn-action btn-archive';
                restoreBtn.innerHTML = '<i class="fas fa-archive"></i> Archive';
                restoreBtn.setAttribute('data-subject-id', subjectId);
            }
        } else {
            // Replace archive button with restore button
            const archiveBtn = actionsCell.querySelector('.btn-archive');
            if (archiveBtn) {
                archiveBtn.className = 'btn-action btn-restore';
                archiveBtn.innerHTML = '<i class="fas fa-undo"></i> Restore';
                archiveBtn.setAttribute('data-subject-id', subjectId);
            }
        }
    }
    
    // Bind action buttons with delegation (can be called to rebind after updates)
    function bindActionButtons() {
        // Remove existing delegated listeners by using a flag
        if (window.subjectActionsBound) {
            return;
        }
        window.subjectActionsBound = true;
        
        // Subject actions (edit, archive, restore) - with delegation
        document.addEventListener('click', function(e) {
            if (e.target.matches('.btn-edit') || e.target.closest('.btn-edit')) {
                const target = e.target.matches('.btn-edit') ? e.target : e.target.closest('.btn-edit');
                handleEditSubject({ target });
            } else if (e.target.matches('.btn-archive') || e.target.closest('.btn-archive')) {
                const target = e.target.matches('.btn-archive') ? e.target : e.target.closest('.btn-archive');
                handleArchiveSubject({ target });
            } else if (e.target.matches('.btn-restore') || e.target.closest('.btn-restore')) {
                const target = e.target.matches('.btn-restore') ? e.target : e.target.closest('.btn-restore');
                handleRestoreSubject({ target });
            }
        });
    }

    // Reset subject form
    function resetSubjectForm() {
        currentSubjectId = null;
        document.getElementById('subjectForm').reset();
        document.getElementById('subjectId').value = '';
        hideAddTopicForm();
    }
    
})();
