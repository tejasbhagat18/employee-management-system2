/* ============================================================
   Employee Management System — JavaScript Enhancements
   Features: Sidebar toggle, active menu, password show/hide,
   form validation, delete confirmation modal, flash auto-dismiss,
   table search, contact form handling, mobile navigation
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ── Sidebar Toggle (Mobile) ──
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function openSidebar() {
        if (sidebar) {
            sidebar.classList.add('open');
            if (sidebarOverlay) sidebarOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeSidebar() {
        if (sidebar) {
            sidebar.classList.remove('open');
            if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    if (sidebarToggle) sidebarToggle.addEventListener('click', openSidebar);
    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);

    // ── Mobile Nav Toggle (Public Pages) ──
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });

        // Close menu on link click
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('open');
            });
        });
    }

    // ── Active Menu Highlighting ──
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    const publicLinks = document.querySelectorAll('.public-navbar .nav-links a');

    sidebarLinks.forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    publicLinks.forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ── Password Show/Hide Toggle ──
    const passwordToggles = document.querySelectorAll('.password-toggle');

    passwordToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const wrapper = this.closest('.password-wrapper');
            const input = wrapper.querySelector('input');
            const eyeOpen = this.querySelector('.eye-open');
            const eyeClosed = this.querySelector('.eye-closed');

            if (input.type === 'password') {
                input.type = 'text';
                if (eyeOpen) eyeOpen.style.display = 'none';
                if (eyeClosed) eyeClosed.style.display = 'block';
            } else {
                input.type = 'password';
                if (eyeOpen) eyeOpen.style.display = 'block';
                if (eyeClosed) eyeClosed.style.display = 'none';
            }
        });
    });

    // ── Flash Message Auto-Dismiss ──
    const flashAlerts = document.querySelectorAll('.flash-container .alert');

    flashAlerts.forEach(function (alert) {
        // Auto dismiss after 5 seconds
        setTimeout(function () {
            alert.classList.add('fade-out');
            setTimeout(function () {
                alert.remove();
            }, 400);
        }, 5000);
    });

    // Close button for flash messages
    const alertCloseButtons = document.querySelectorAll('.btn-close-alert');
    alertCloseButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const alert = this.closest('.alert');
            alert.classList.add('fade-out');
            setTimeout(function () {
                alert.remove();
            }, 400);
        });
    });

    // ── Delete Confirmation Modal ──
    const deleteButtons = document.querySelectorAll('.btn-delete-confirm');
    const confirmModal = document.getElementById('confirmModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    let deleteUrl = '';

    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            deleteUrl = this.getAttribute('href') || this.dataset.href;
            if (confirmModal) {
                confirmModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', function () {
            confirmModal.classList.remove('active');
            document.body.style.overflow = '';
            deleteUrl = '';
        });
    }

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function () {
            if (deleteUrl) {
                window.location.href = deleteUrl;
            }
        });
    }

    // Close modal on overlay click
    if (confirmModal) {
        confirmModal.addEventListener('click', function (e) {
            if (e.target === confirmModal) {
                confirmModal.classList.remove('active');
                document.body.style.overflow = '';
                deleteUrl = '';
            }
        });
    }

    // ── Table Search / Filter ──
    const tableSearch = document.getElementById('tableSearch');
    const tableBody = document.getElementById('employeeTableBody');

    if (tableSearch && tableBody) {
        tableSearch.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();
            const rows = tableBody.querySelectorAll('tr');

            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // ── Form Validation ──
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required]');

            // Clear previous errors
            form.querySelectorAll('.form-group').forEach(function (group) {
                group.classList.remove('has-error');
            });

            inputs.forEach(function (input) {
                const group = input.closest('.form-group');
                const errorEl = group ? group.querySelector('.input-error') : null;

                if (!input.value.trim()) {
                    if (group) group.classList.add('has-error');
                    if (errorEl) errorEl.textContent = 'This field is required';
                    isValid = false;
                    return;
                }

                // Email validation
                if (input.type === 'email') {
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(input.value)) {
                        if (group) group.classList.add('has-error');
                        if (errorEl) errorEl.textContent = 'Please enter a valid email';
                        isValid = false;
                    }
                }

                // Phone validation
                if (input.name === 'phone') {
                    const phonePattern = /^[0-9+\-\s()]{7,15}$/;
                    if (!phonePattern.test(input.value)) {
                        if (group) group.classList.add('has-error');
                        if (errorEl) errorEl.textContent = 'Please enter a valid phone number';
                        isValid = false;
                    }
                }

                // Salary validation
                if (input.name === 'salary') {
                    if (parseFloat(input.value) <= 0) {
                        if (group) group.classList.add('has-error');
                        if (errorEl) errorEl.textContent = 'Salary must be greater than 0';
                        isValid = false;
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.has-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });

        // Clear error on input
        form.querySelectorAll('input, textarea').forEach(function (input) {
            input.addEventListener('input', function () {
                const group = this.closest('.form-group');
                if (group) group.classList.remove('has-error');
            });
        });
    });

    // ── Contact Form Handling ──
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            showToast('Thank you! Your message has been received.', 'success');
            contactForm.reset();
        });
    }

    // ── Toast Notification ──
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = 'toast' + (type ? ' ' + type : '');
        toast.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' + message;
        document.body.appendChild(toast);

        setTimeout(function () {
            toast.classList.add('fade-out');
            setTimeout(function () {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // ── Escape key to close modals/sidebar ──
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeSidebar();
            if (confirmModal && confirmModal.classList.contains('active')) {
                confirmModal.classList.remove('active');
                document.body.style.overflow = '';
                deleteUrl = '';
            }
        }
    });

});