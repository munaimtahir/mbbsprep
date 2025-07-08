// Tags Management JavaScript
(function() {
    'use strict';
    
    let currentTagId = null;
    let tagModal = null;
    let subtagModal = null;
    let confirmModal = null;
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Tags.js: DOM ready, initializing...');
        initializeModals();
        bindEventHandlers();
        initializeSearch();
        setupResourceCheckboxes();
        initializeUrlStore();
        console.log('Tags.js: Initialization complete');
    });
    
    // Initialize Bootstrap modals
    function initializeModals() {
        const tagModalEl = document.getElementById('tagModal');
        const subtagModalEl = document.getElementById('subtagModal');
        const confirmModalEl = document.getElementById('confirmModal');
        
        if (tagModalEl) {
            tagModal = new bootstrap.Modal(tagModalEl);
        }
        
        if (subtagModalEl) {
            subtagModal = new bootstrap.Modal(subtagModalEl);
        }
        
        if (confirmModalEl) {
            confirmModal = new bootstrap.Modal(confirmModalEl);
        }
    }
    
    // Initialize URL store for AJAX endpoints
    function initializeUrlStore() {
        window.staffUrls = window.staffUrls || {};
        console.log('Staff URLs initialized:', window.staffUrls);
        // URLs will be populated by Django template
    }
    
    // Bind all event handlers
    function bindEventHandlers() {
        // Add tag buttons
        bindElement('#addTagBtn', 'click', showAddTagModal);
        bindElement('#addFirstTagBtn', 'click', showAddTagModal);
        
        // Save tag button
        bindElement('#saveTagBtn', 'click', saveTag);
        console.log('Save tag button bound:', document.getElementById('saveTagBtn') !== null);
        
        // Tag actions with event delegation
        bindActionButtons();
        
        // Subtag management
        bindElement('#addSubtagBtn', 'click', showAddSubtagForm);
        bindElement('#saveSubtagBtn', 'click', saveSubtag);
        bindElement('#cancelSubtagBtn', 'click', hideAddSubtagForm);
        
        // Modal events
        const tagModalEl = document.getElementById('tagModal');
        if (tagModalEl) {
            tagModalEl.addEventListener('hidden.bs.modal', resetTagForm);
        }
        
        // Form submission
        bindElement('#tagForm', 'submit', function(e) {
            e.preventDefault();
            saveTag();
        });
        
        // Enter key on new subtag input
        bindElement('#newSubtagName', 'keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveSubtag();
            }
        });
        
        // Color picker
        bindElement('#tagColor', 'input', updateColorPreview);
        
        // Bulk actions
        bindElement('#bulkActionSelect', 'change', handleBulkActionChange);
        bindElement('#selectAllTags', 'change', toggleSelectAllTags);
        
        // Tag selection checkboxes
        document.addEventListener('change', function(e) {
            if (e.target.classList.contains('tag-select-checkbox')) {
                updateBulkActionButton();
            }
        });
        
        // Confirm modal actions
        bindElement('#confirmActionBtn', 'click', executeConfirmedAction);
    }
    
    // Utility function to bind elements safely
    function bindElement(selector, event, handler) {
        const element = document.querySelector(selector);
        if (element) {
            element.addEventListener(event, handler);
        }
    }
    
    // Bind action buttons with event delegation
    function bindActionButtons() {
        console.log('Binding action buttons...');
        document.addEventListener('click', function(e) {
            console.log('Click detected on:', e.target, 'Classes:', e.target.classList.toString());
            
            if (e.target.classList.contains('btn-edit-tag') || 
                e.target.closest('.btn-edit-tag') ||
                (e.target.tagName === 'I' && e.target.parentElement.classList.contains('btn-edit-tag'))) {
                e.preventDefault();
                console.log('Edit tag button clicked!');
                handleEditTag(e);
            } else if (e.target.classList.contains('btn-archive-tag') || e.target.closest('.btn-archive-tag')) {
                e.preventDefault();
                handleArchiveTag(e);
            } else if (e.target.classList.contains('btn-restore-tag') || e.target.closest('.btn-restore-tag')) {
                e.preventDefault();
                handleRestoreTag(e);
            } else if (e.target.classList.contains('btn-edit-subtag') || e.target.closest('.btn-edit-subtag')) {
                e.preventDefault();
                handleEditSubtag(e);
            } else if (e.target.classList.contains('btn-archive-subtag') || e.target.closest('.btn-archive-subtag')) {
                e.preventDefault();
                handleArchiveSubtag(e);
            } else if (e.target.classList.contains('btn-restore-subtag') || e.target.closest('.btn-restore-subtag')) {
                e.preventDefault();
                handleRestoreSubtag(e);
            }
        });
        console.log('Action buttons bound successfully');
    }
    
    // Setup resource checkboxes behavior
    function setupResourceCheckboxes() {
        const allResources = document.getElementById('resourceTypeAll');
        const specificResources = document.querySelectorAll('.resource-checkbox:not(#resourceTypeAll)');
        
        if (allResources) {
            allResources.addEventListener('change', function() {
                specificResources.forEach(checkbox => {
                    checkbox.disabled = this.checked;
                    if (this.checked) {
                        checkbox.checked = false;
                    }
                });
            });
        }
        
        specificResources.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked && allResources) {
                    allResources.checked = false;
                }
            });
        });
    }
    
    // Initialize search functionality
    function initializeSearch() {
        const searchInput = document.getElementById('searchInput');
        const statusFilter = document.getElementById('statusFilter');
        const resourceFilter = document.getElementById('resourceFilter');
        
        if (searchInput) {
            searchInput.addEventListener('input', debounce(performSearch, 300));
        }
        
        if (statusFilter) {
            statusFilter.addEventListener('change', performSearch);
        }
        
        if (resourceFilter) {
            resourceFilter.addEventListener('change', performSearch);
        }
    }
    
    // Perform search/filter
    function performSearch() {
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('statusFilter')?.value || '';
        const resourceFilter = document.getElementById('resourceFilter')?.value || '';
        
        const rows = document.querySelectorAll('.tag-row');
        
        rows.forEach(row => {
            const tagName = row.querySelector('.tag-name')?.textContent.toLowerCase() || '';
            const tagStatus = row.getAttribute('data-status') || '';
            const tagResources = row.getAttribute('data-resources') || '';
            
            let showRow = true;
            
            // Search filter
            if (searchTerm && !tagName.includes(searchTerm)) {
                showRow = false;
            }
            
            // Status filter
            if (statusFilter && tagStatus !== statusFilter) {
                showRow = false;
            }
            
            // Resource filter
            if (resourceFilter && !tagResources.includes(resourceFilter)) {
                showRow = false;
            }
            
            row.style.display = showRow ? '' : 'none';
        });
    }
    
    // Show add tag modal
    function showAddTagModal() {
        currentTagId = null;
        resetTagForm();
        document.getElementById('tagModalLabel').textContent = 'Add Tag';
        if (tagModal) {
            tagModal.show();
        }
    }
    
    // Handle edit tag
    function handleEditTag(e) {
        console.log('Edit button clicked', e.target);
        const tagElement = e.target.closest('[data-tag-id]');
        if (!tagElement) {
            console.error('No tag element found with data-tag-id');
            return;
        }
        const tagId = tagElement.getAttribute('data-tag-id');
        console.log('Editing tag ID:', tagId);
        loadTagForEdit(tagId);
    }
    
    // Load tag data for editing
    function loadTagForEdit(tagId) {
        console.log('Loading tag for edit:', tagId);
        if (!window.staffUrls.tagGet) {
            console.error('Tag get URL not defined');
            return;
        }
        
        const url = window.staffUrls.tagGet.replace('{id}', tagId);
        console.log('AJAX URL:', url);
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                populateTagForm(data.tag);
                currentTagId = tagId;
                document.getElementById('tagModalLabel').textContent = 'Edit Tag';
                if (tagModal) {
                    tagModal.show();
                } else {
                    console.error('tagModal is not initialized');
                }
            } else {
                showToast(data.message || 'Error loading tag data', 'error');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            showToast('Error loading tag data', 'error');
        });
    }
    
    // Populate tag form with data
    function populateTagForm(tag) {
        console.log('Populating form with tag data:', tag);
        
        const tagIdField = document.getElementById('tagId');
        const tagNameField = document.getElementById('tagName');
        const tagDescField = document.getElementById('tagDescription');
        const tagColorField = document.getElementById('tagColor');
        
        if (tagIdField) tagIdField.value = tag.id || '';
        if (tagNameField) tagNameField.value = tag.name || '';
        if (tagDescField) tagDescField.value = tag.description || '';
        if (tagColorField) tagColorField.value = tag.color || '#0057A3';
        
        // Update color preview
        updateColorPreview();
        
        // Set resource checkboxes
        const resources = tag.resources || [];
        const allResource = document.getElementById('resourceTypeAll');
        const mcqResource = document.getElementById('resourceTypeMcq');
        const videoResource = document.getElementById('resourceTypeVideo');
        const noteResource = document.getElementById('resourceTypeNote');
        
        if (allResource) allResource.checked = resources.includes('all');
        if (mcqResource) mcqResource.checked = resources.includes('mcq');
        if (videoResource) videoResource.checked = resources.includes('video');
        if (noteResource) noteResource.checked = resources.includes('note');
        
        console.log('Form populated successfully');
        
        // Load subtags if editing
        if (tag.id) {
            loadSubtags(tag.id);
        }
    }
    
    // Reset tag form
    function resetTagForm() {
        document.getElementById('tagForm').reset();
        document.getElementById('tagId').value = '';
        document.getElementById('tagColor').value = '#0057A3';
        updateColorPreview();
        
        // Hide subtags section for new tags
        const subtagsSection = document.getElementById('subtagsSection');
        if (subtagsSection) {
            subtagsSection.style.display = 'none';
        }
        
        hideAddSubtagForm();
    }
    
    // Update color preview
    function updateColorPreview() {
        const colorInput = document.getElementById('tagColor');
        const colorPreview = document.getElementById('colorPreview');
        
        if (colorInput && colorPreview) {
            colorPreview.style.backgroundColor = colorInput.value;
        }
    }
    
    // Save tag (create or update)
    function saveTag() {
        console.log('Save tag function called');
        const form = document.getElementById('tagForm');
        const formData = new FormData(form);
        
        const tagData = {
            name: formData.get('name'),
            description: formData.get('description'),
            color: formData.get('color'),
            is_active: formData.get('is_active') ? true : false,
            apply_to_all_resources: document.getElementById('resourceTypeAll').checked,
            apply_to_mcq: document.getElementById('resourceTypeMcq').checked,
            apply_to_videos: document.getElementById('resourceTypeVideo').checked,
            apply_to_notes: document.getElementById('resourceTypeNote').checked
        };
        
        console.log('Tag data to send:', tagData);
        
        const isEdit = currentTagId !== null;
        const url = isEdit ? 
            window.staffUrls.tagUpdate.replace('{id}', currentTagId) : 
            window.staffUrls.tagAdd;
        
        console.log('Request URL:', url);
        console.log('Is edit mode:', isEdit);
        
        if (!url) {
            console.error('URL is undefined. Check staffUrls configuration.');
            showToast('Configuration error: URL not found', 'error');
            return;
        }
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tagData)
        })
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                showToast(data.message || 'Tag saved successfully', 'success');
                if (tagModal) {
                    tagModal.hide();
                }
                // Refresh page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 500);
            } else {
                console.error('Server returned error:', data);
                showToast(data.message || 'Error saving tag', 'error');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            showToast('Error saving tag', 'error');
        });
    }
    
    // Handle archive tag
    function handleArchiveTag(e) {
        const tagId = e.target.closest('[data-tag-id]').getAttribute('data-tag-id');
        const tagName = e.target.closest('[data-tag-name]').getAttribute('data-tag-name');
        
        if (confirm(`Are you sure you want to archive "${tagName}"?`)) {
            toggleTagStatus(tagId, false);
        }
    }
    
    // Handle restore tag
    function handleRestoreTag(e) {
        const tagId = e.target.closest('[data-tag-id]').getAttribute('data-tag-id');
        const tagName = e.target.closest('[data-tag-name]').getAttribute('data-tag-name');
        
        if (confirm(`Are you sure you want to restore "${tagName}"?`)) {
            toggleTagStatus(tagId, true);
        }
    }
    
    // Toggle tag status
    function toggleTagStatus(tagId, isActive) {
        fetch(window.staffUrls.tagToggleStatus, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tag_id: tagId,
                is_active: isActive
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast(data.message || 'Tag status updated', 'success');
                // Refresh page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 500);
            } else {
                showToast(data.message || 'Error updating tag status', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error updating tag status', 'error');
        });
    }
    
    // Load subtags for a tag
    function loadSubtags(tagId) {
        if (!window.staffUrls.getTagSubtags) {
            return;
        }
        
        const url = window.staffUrls.getTagSubtags.replace('{id}', tagId);
        
        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySubtags(data.subtags);
                document.getElementById('subtagsSection').style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error loading subtags:', error);
        });
    }
    
    // Display subtags in table
    function displaySubtags(subtags) {
        const tbody = document.getElementById('subtagsTableBody');
        if (!tbody) return;
        
        if (subtags && subtags.length > 0) {
            tbody.innerHTML = subtags.map((subtag, index) => `
                <tr data-subtag-id="${subtag.id}">
                    <td>${index + 1}</td>
                    <td>${subtag.name}</td>
                    <td><span class="text-muted small">${subtag.usage_count || 0} items</span></td>
                    <td>
                        <span class="status-badge ${subtag.is_active ? 'status-active' : 'status-archived'}">
                            <i class="fas fa-circle"></i>
                            ${subtag.is_active ? 'Active' : 'Archived'}
                        </span>
                    </td>
                    <td>
                        <button type="button" class="btn-action btn-edit btn-edit-subtag" data-subtag-id="${subtag.id}">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        ${subtag.is_active ? 
                            `<button type="button" class="btn-action btn-archive btn-archive-subtag" data-subtag-id="${subtag.id}" data-subtag-name="${subtag.name}">
                                <i class="fas fa-archive"></i> Archive
                            </button>` :
                            `<button type="button" class="btn-action btn-restore btn-restore-subtag" data-subtag-id="${subtag.id}" data-subtag-name="${subtag.name}">
                                <i class="fas fa-undo"></i> Restore
                            </button>`
                        }
                    </td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        <i class="fas fa-tag me-2"></i>No subtags yet
                    </td>
                </tr>
            `;
        }
    }
    
    // Show add subtag form
    function showAddSubtagForm() {
        const form = document.getElementById('addSubtagForm');
        if (form) {
            form.style.display = 'block';
            document.getElementById('newSubtagName').focus();
        }
    }
    
    // Hide add subtag form
    function hideAddSubtagForm() {
        const form = document.getElementById('addSubtagForm');
        if (form) {
            form.style.display = 'none';
            document.getElementById('newSubtagName').value = '';
        }
    }
    
    // Save subtag
    function saveSubtag() {
        const subtagName = document.getElementById('newSubtagName').value.trim();
        
        if (!subtagName) {
            showToast('Please enter a subtag name', 'error');
            return;
        }
        
        if (!currentTagId) {
            showToast('No parent tag selected', 'error');
            return;
        }
        
        const subtagData = {
            name: subtagName,
            tag: currentTagId,
            is_active: true
        };
        
        fetch(window.staffUrls.subtagAdd, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(subtagData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast(data.message || 'Subtag created successfully', 'success');
                hideAddSubtagForm();
                loadSubtags(currentTagId);
            } else {
                showToast(data.message || 'Error creating subtag', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error creating subtag', 'error');
        });
    }
    
    // Toggle select all tags
    function toggleSelectAllTags() {
        const selectAll = document.getElementById('selectAllTags');
        const checkboxes = document.querySelectorAll('.tag-select-checkbox');
        
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAll.checked;
        });
        
        updateBulkActionButton();
    }
    
    // Update bulk action button state
    function updateBulkActionButton() {
        const selectedCheckboxes = document.querySelectorAll('.tag-select-checkbox:checked');
        const bulkActionBtn = document.getElementById('bulkActionBtn');
        const bulkActionLabel = document.getElementById('bulkActionLabel');
        
        if (selectedCheckboxes.length > 0) {
            bulkActionBtn.disabled = false;
            bulkActionLabel.textContent = `${selectedCheckboxes.length} selected`;
        } else {
            bulkActionBtn.disabled = true;
            bulkActionLabel.textContent = 'Select items';
        }
        
        // Update selectedTagIds hidden input
        const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
        const hiddenInput = document.getElementById('selectedTagIds');
        if (hiddenInput) {
            hiddenInput.value = JSON.stringify(selectedIds);
        }
    }
    
    // Handle bulk action change
    function handleBulkActionChange() {
        const bulkActionSelect = document.getElementById('bulkActionSelect');
        const selectedAction = bulkActionSelect.value;
        
        if (selectedAction) {
            const selectedCheckboxes = document.querySelectorAll('.tag-select-checkbox:checked');
            const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
            
            if (selectedIds.length === 0) {
                showToast('Please select tags first', 'error');
                bulkActionSelect.value = '';
                return;
            }
            
            performBulkAction(selectedAction, selectedIds);
            bulkActionSelect.value = '';
        }
    }
    
    // Perform bulk action
    function performBulkAction(action, tagIds) {
        const actionNames = {
            'archive': 'archive',
            'restore': 'restore',
            'delete': 'delete'
        };
        
        const actionName = actionNames[action] || action;
        
        if (confirm(`Are you sure you want to ${actionName} ${tagIds.length} tag(s)?`)) {
            fetch(window.staffUrls.tagBulkAction, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: action,
                    tag_ids: tagIds
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message || `Bulk ${actionName} completed`, 'success');
                    
                    // Refresh the page to show updated data
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                } else {
                    showToast(data.message || `Error performing bulk ${actionName}`, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast(`Error performing bulk ${actionName}`, 'error');
            });
        }
    }
    
    // Execute confirmed action (placeholder for modal confirmations)
    function executeConfirmedAction() {
        // Implementation depends on what action was confirmed
        if (confirmModal) {
            confirmModal.hide();
        }
    }
    
    // Utility functions
    function getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                     document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
                     document.querySelector('#csrf_token')?.value;
        return token || '';
    }
    
    function showToast(message, type = 'info') {
        // Simple toast implementation - can be enhanced with Bootstrap toast
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Placeholder subtag handlers
    function handleEditSubtag(e) {
        const subtagId = e.target.closest('[data-subtag-id]').getAttribute('data-subtag-id');
        console.log('Edit subtag:', subtagId);
        // Implementation needed
    }
    
    function handleArchiveSubtag(e) {
        const subtagId = e.target.closest('[data-subtag-id]').getAttribute('data-subtag-id');
        const subtagName = e.target.closest('[data-subtag-name]').getAttribute('data-subtag-name');
        console.log('Archive subtag:', subtagId, subtagName);
        // Implementation needed
    }
    
    function handleRestoreSubtag(e) {
        const subtagId = e.target.closest('[data-subtag-id]').getAttribute('data-subtag-id');
        const subtagName = e.target.closest('[data-subtag-name]').getAttribute('data-subtag-name');
        console.log('Restore subtag:', subtagId, subtagName);
        // Implementation needed
    }

})(); // End IIFE
