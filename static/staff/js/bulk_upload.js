// Bulk Upload Page JavaScript

// Initialize event delegation
document.addEventListener('DOMContentLoaded', function() {
    setupEventDelegation();
});

// Setup event delegation for inline event handlers
function setupEventDelegation() {
    // File upload area click
    document.addEventListener('click', function(e) {
        if (e.target.matches('.file-upload-area') || e.target.closest('.file-upload-area')) {
            e.preventDefault();
            const fileInput = document.getElementById('csvFile');
            if (fileInput) fileInput.click();
        }
    });

    // Format guide toggle
    document.addEventListener('click', function(e) {
        if (e.target.matches('.format-guide-header') || e.target.closest('.format-guide-header')) {
            e.preventDefault();
            toggleFormatGuide();
        }
    });

    // File input change
    const fileInput = document.getElementById('csvFile');
    if (fileInput) {
        fileInput.addEventListener('change', updateFileName);
    }
}

// File upload handling
function updateFileName() {
    const fileInput = document.getElementById('csvFile');
    const selectedFile = document.getElementById('selectedFile');
    const fileName = document.getElementById('fileName');
    
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
        selectedFile.style.display = 'block';
    } else {
        selectedFile.style.display = 'none';
    }
}

// Drag and drop functionality
const uploadArea = document.querySelector('.file-upload-area');
const fileInput = document.getElementById('csvFile');

if (uploadArea && fileInput) {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileName();
        }
    });
}

// Format guide toggle
function toggleFormatGuide() {
    const content = document.getElementById('formatGuideContent');
    const icon = document.getElementById('formatToggleIcon');
    
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

// Form submission with progress
document.addEventListener('DOMContentLoaded', function() {
    const bulkUploadForm = document.getElementById('bulkUploadForm');
    
    if (bulkUploadForm) {
        bulkUploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('csvFile');
            
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Please select a file to upload.');
                return;
            }
            
            // Show loading state
            const submitBtn = document.getElementById('uploadBtn');
            const spinner = submitBtn.querySelector('.loading-spinner');
            const progress = document.getElementById('uploadProgress');
            
            submitBtn.disabled = true;
            if (spinner) {
                spinner.style.display = 'inline-block';
            }
            if (progress) {
                progress.style.display = 'block';
            }
            
            // Simulate progress (since we can't track actual server progress easily)
            let progressValue = 0;
            const progressBar = document.getElementById('progressBar');
            const progressPercent = document.getElementById('progressPercent');
            
            if (progressBar && progressPercent) {
                const progressInterval = setInterval(() => {
                    progressValue += Math.random() * 15;
                    if (progressValue > 90) {
                        progressValue = 90;
                        clearInterval(progressInterval);
                    }
                    
                    progressBar.style.width = progressValue + '%';
                    progressPercent.textContent = Math.round(progressValue) + '%';
                }, 200);
            }
        });
    }
});

// Auto-dismiss alerts after 10 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        if (alert.querySelector('.btn-close')) {
            alert.querySelector('.btn-close').click();
        }
    });
}, 10000);

// Clear session error data on page load (optional)
window.addEventListener('load', function() {
    // You could make an AJAX call here to clear the session data
    // to prevent showing old error data on refresh
});
