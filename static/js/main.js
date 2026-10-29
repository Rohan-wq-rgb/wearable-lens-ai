// WearableLens AI Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    if (window.WearableLensTheme) {
        window.WearableLensTheme.applyTheme(localStorage.getItem('theme') || 'system');
        window.WearableLensTheme.updateToggleIcon(localStorage.getItem('theme') || 'system');
    }

    // Mobile navigation toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('mobile-open');
            mobileMenuToggle.classList.toggle('open');
        });
    }

    // Image upload handling
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', function() {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelection(files);
            }
        });
        
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFileSelection(e.target.files);
            }
        });
    }
});

function handleFileSelection(files) {
    const file = files[0];
    
    if (!file) {
        showError('Please select a file');
        return;
    }
    
    // Check file type
    const validTypes = ['image/png', 'image/jpeg', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload PNG, JPG, JPEG, or WEBP images.');
        return;
    }
    
    // Check file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
        showError('File is too large. Maximum size is 10MB.');
        return;
    }
    
    const uploadArea = document.querySelector('.upload-area');
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            if (uploadArea) {
                uploadArea.style.backgroundImage = `url(${e.target.result})`;
                uploadArea.style.backgroundSize = 'cover';
                uploadArea.style.backgroundPosition = 'center';
                uploadArea.style.backgroundColor = 'transparent';
                uploadArea.innerHTML = `<div style="position: relative; z-index: 1;">
                    <img src="${e.target.result}" alt="Uploaded device" style="max-width: 100%; max-height: 300px; border-radius: 8px; margin: 0 auto;">
                    <button type="button" class="btn-remove" style="position: absolute; top: 10px; right: 10px; background: rgba(220, 53, 69, 0.8); color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; font-size: 20px;">&times;</button>
                </div>`;
            }
        };
        img.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
}

function showError(message) {
    alert(message);
}

function showSuccess(message) {
    alert(message);
}

// Form submission handling
function handleIdentificationSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const file = formData.get('device_image');
    
    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="loading-spinner"></span> Analyzing...';
    }
    
    fetch('/identify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show results
            if (window.WearableLensAI && window.WearableLensAI.displayResults) {
                window.WearableLensAI.displayResults(data.analysis);
            }
        } else {
            showError(data.error || 'Analysis failed');
        }
    })
    .catch(error => {
        console.error('Analysis error:', error);
        showError('Analysis failed. Please try again.');
    })
    .finally(() => {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Analyze Device';
        }
    });
}

// Expose API for other scripts
window.WearableLensAI = {
    displayResults: function(analysis) {
        console.log('Analysis results:', analysis);
        // This would update the UI with results
    },
    showError: showError,
    showSuccess: showSuccess,
    handleFileSelection: handleFileSelection,
    handleIdentificationSubmit: handleIdentificationSubmit
};

// Flash message auto-dismiss
setTimeout(function() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function(flash) {
        setTimeout(function() {
            flash.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
}, 100);
