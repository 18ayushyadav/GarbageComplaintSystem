/**
 * Smart Garbage Complaint System — Client-Side JavaScript
 *
 * Features:
 * - Image upload preview with clear button
 * - Auto-dismiss flash messages
 * - Form validation feedback
 * - Smooth scroll behavior
 */

document.addEventListener('DOMContentLoaded', function () {
    // ═══════════════════════════════════════════════════════════════════════
    //  IMAGE PREVIEW ON UPLOAD
    // ═══════════════════════════════════════════════════════════════════════
    const imageInput = document.getElementById('complaint-image');
    const previewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const clearImageBtn = document.getElementById('clear-image-btn');

    if (imageInput) {
        imageInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    alert('Please upload a valid image file (JPG, PNG, GIF).');
                    imageInput.value = '';
                    return;
                }

                // Validate file size (max 5MB)
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    alert('Image size must be less than 5MB.');
                    imageInput.value = '';
                    return;
                }

                // Show preview
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    previewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Clear image button
    if (clearImageBtn) {
        clearImageBtn.addEventListener('click', function () {
            imageInput.value = '';
            previewContainer.style.display = 'none';
            imagePreview.src = '';
        });
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  AUTO-DISMISS FLASH MESSAGES
    // ═══════════════════════════════════════════════════════════════════════
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000); // Auto-dismiss after 5 seconds
    });

    // ═══════════════════════════════════════════════════════════════════════
    //  FORM VALIDATION FEEDBACK
    // ═══════════════════════════════════════════════════════════════════════
    const complaintForm = document.getElementById('complaint-form');
    if (complaintForm) {
        complaintForm.addEventListener('submit', function (event) {
            // Check browser validation
            if (!complaintForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Add visual feedback to required fields
            const requiredFields = complaintForm.querySelectorAll('[required]');
            requiredFields.forEach(function (field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
        });

        // Remove error state when user starts typing
        const formInputs = complaintForm.querySelectorAll('.form-control, .form-select');
        formInputs.forEach(function (input) {
            input.addEventListener('input', function () {
                this.classList.remove('is-invalid');
                if (this.value.trim()) {
                    this.classList.add('is-valid');
                }
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  DASHBOARD AUTO-FILTER ON SELECT CHANGE
    // ═══════════════════════════════════════════════════════════════════════
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    const filterForm = document.getElementById('dashboard-filter-form');

    if (statusFilter && filterForm) {
        statusFilter.addEventListener('change', function () {
            filterForm.submit();
        });
    }

    if (priorityFilter && filterForm) {
        priorityFilter.addEventListener('change', function () {
            filterForm.submit();
        });
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  ANIMATE ELEMENTS ON SCROLL (Intersection Observer)
    // ═══════════════════════════════════════════════════════════════════════
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1,
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe stat cards and step cards for scroll animations
    const animatedElements = document.querySelectorAll('.stat-card, .step-card');
    animatedElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // ═══════════════════════════════════════════════════════════════════════
    //  COPY REFERENCE NUMBER ON CLICK
    // ═══════════════════════════════════════════════════════════════════════
    const referenceBadge = document.getElementById('reference-badge');
    if (referenceBadge) {
        referenceBadge.style.cursor = 'pointer';
        referenceBadge.title = 'Click to copy reference number';
        referenceBadge.addEventListener('click', function () {
            const refNumber = referenceBadge.querySelector('.reference-number').textContent;
            navigator.clipboard.writeText(refNumber).then(function () {
                // Show temporary feedback
                const originalText = referenceBadge.querySelector('.reference-label').textContent;
                referenceBadge.querySelector('.reference-label').textContent = '✅ Copied!';
                setTimeout(function () {
                    referenceBadge.querySelector('.reference-label').textContent = originalText;
                }, 2000);
            });
        });
    }
});
