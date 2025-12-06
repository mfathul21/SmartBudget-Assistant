// Professional Admin Panel: User Management with OCR control on edit
document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('users-tbody');
    const emptyState = document.getElementById('empty-state');
    const searchInput = document.getElementById('search-input');
    const roleFilter = document.getElementById('role-filter');
    const addBtn = document.getElementById('add-user-btn');
    const modal = document.getElementById('user-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalName = document.getElementById('modal-name');
    const modalEmail = document.getElementById('modal-email');
    const modalPassword = document.getElementById('modal-password');
    const passwordGroup = document.getElementById('password-group');
    const passwordHint = document.getElementById('password-hint');
    const modalRole = document.getElementById('modal-role');
    const ocrSection = document.getElementById('ocr-section');
    const modalOcrEnabled = document.getElementById('modal-ocr-enabled');
    const modalSave = document.getElementById('modal-save');
    const toast = document.getElementById('toast');

    let users = [];
    let filtered = [];
    let page = 1;
    const pageSize = 10;
    let editingUserId = null;

    function showToast(msg, type = 'info') {
        if (!toast) return;
        toast.textContent = msg;
        toast.className = `toast show ${type}`;
        setTimeout(() => toast.classList.remove('show'), 2500);
    }

    function openModal(title, isEdit = false) {
        modalTitle.textContent = title;
        
        // Show OCR section only in EDIT mode
        if (ocrSection) {
            ocrSection.style.display = isEdit ? 'flex' : 'none';
        }

        // Show/hide password field based on mode
        if (passwordGroup) {
            passwordGroup.style.display = isEdit ? 'none' : 'block';
            if (passwordHint) {
                passwordHint.style.display = isEdit ? 'none' : 'block';
            }
        }

        modal.classList.add('active');
        setTimeout(() => modalName?.focus(), 50);
    }

    function closeModal() {
        modal.classList.remove('active');
        editingUserId = null;
        modalName.value = '';
        modalEmail.value = '';
        modalPassword.value = '';
        modalRole.value = 'user';
        if (modalOcrEnabled) modalOcrEnabled.checked = false;
    }

    function renderTable() {
        tbody.innerHTML = '';
        
        if (filtered.length === 0) {
            emptyState.style.display = '';
            return;
        }
        emptyState.style.display = 'none';

        const start = (page - 1) * pageSize;
        const rows = filtered.slice(start, start + pageSize);

        for (const u of rows) {
            const tr = document.createElement('tr');
            
            const ocrBadge = u.ocr_enabled 
                ? '<span class="badge badge-ocr-yes"><i class="fas fa-check-circle"></i> Yes</span>'
                : '<span class="badge badge-ocr-no"><i class="fas fa-times-circle"></i> No</span>';
            
            const roleBadge = u.role === 'admin' 
                ? '<span class="badge badge-admin"><i class="fas fa-shield-alt"></i> Admin</span>'
                : '<span class="badge badge-user"><i class="fas fa-user"></i> User</span>';

            tr.innerHTML = `
                <td>${u.id}</td>
                <td>
                    <div style="font-weight: 600; color: #111827;">${u.name}</div>
                    <div style="font-size: 12px; color: #9ca3af;">${u.email}</div>
                </td>
                <td>${roleBadge}</td>
                <td>${ocrBadge}</td>
                <td>
                    <div class="actions-cell">
                        <button class="action-btn action-btn-edit" data-edit-id="${u.id}" title="Edit User">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn action-btn-delete" data-delete-id="${u.id}" title="Delete User">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        }

        renderPagination();
        attachEventListeners();
    }

    function renderPagination() {
        const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
        const pageInfo = document.getElementById('page-info');
        if (pageInfo) pageInfo.textContent = `${page} / ${totalPages}`;

        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        if (prevBtn) prevBtn.disabled = page <= 1;
        if (nextBtn) nextBtn.disabled = page >= totalPages;
    }

    function renderStats() {
        const total = users.length;
        const admins = users.filter(u => u.role === 'admin').length;
        const standard = total - admins;
        document.getElementById('statUsers').textContent = String(total);
        document.getElementById('statAdmins').textContent = String(admins);
        document.getElementById('statStandard').textContent = String(standard);
    }

    function attachEventListeners() {
        // Edit buttons
        tbody.querySelectorAll('[data-edit-id]').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = Number(btn.getAttribute('data-edit-id'));
                const user = users.find(x => x.id === id);
                if (!user) return;

                editingUserId = id;
                modalName.value = user.name || '';
                modalEmail.value = user.email || '';
                modalPassword.value = '';
                modalRole.value = user.role || 'user';
                
                if (modalOcrEnabled) {
                    modalOcrEnabled.checked = user.ocr_enabled || false;
                }

                openModal('Edit User', true); // true = edit mode
            });
        });

        // Delete buttons
        tbody.querySelectorAll('[data-delete-id]').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = Number(btn.getAttribute('data-delete-id'));
                const user = users.find(x => x.id === id);
                if (!confirm(`Delete user "${user.name}"?`)) return;

                try {
                    const res = await apiFetch(`/api/admin/users/${id}`, { method: 'DELETE' });
                    if (!res.ok) throw new Error('Failed to delete user');
                    showToast('User deleted successfully', 'success');
                    await loadUsers();
                } catch (e) {
                    showToast(e.message, 'error');
                }
            });
        });
    }

    function applyFilter() {
        const q = (searchInput.value || '').toLowerCase();
        const role = roleFilter.value || '';

        filtered = users.filter(u => {
            const matchText = (u.name || '').toLowerCase().includes(q) || 
                            (u.email || '').toLowerCase().includes(q);
            const matchRole = role ? u.role === role : true;
            return matchText && matchRole;
        });

        page = 1;
        renderTable();
    }

    async function loadUsers() {
        try {
            const res = await apiFetch('/api/admin/users');
            if (!res.ok) throw new Error('Failed to load users');
            users = await res.json();
            filtered = users.slice();
            renderStats();
            renderTable();
        } catch (e) {
            showToast(e.message, 'error');
            users = [];
            filtered = [];
            renderStats();
            renderTable();
        }
    }

    // Events
    addBtn?.addEventListener('click', () => {
        editingUserId = null;
        modalName.value = '';
        modalEmail.value = '';
        modalPassword.value = '';
        modalRole.value = 'user';
        if (modalOcrEnabled) modalOcrEnabled.checked = false;
        openModal('Add New User', false); // false = create mode
    });

    modal.querySelectorAll('[data-modal-close]').forEach(el => {
        el.addEventListener('click', closeModal);
    });

    searchInput?.addEventListener('input', applyFilter);
    roleFilter?.addEventListener('change', applyFilter);

    document.getElementById('prev-page')?.addEventListener('click', () => {
        if (page > 1) { page--; renderTable(); }
    });

    document.getElementById('next-page')?.addEventListener('click', () => {
        const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
        if (page < totalPages) { page++; renderTable(); }
    });

    // Save (Create/Edit)
    modalSave?.addEventListener('click', async () => {
        const payload = {
            name: modalName.value.trim(),
            email: modalEmail.value.trim(),
            role: modalRole.value.trim() || 'user',
        };

        // Add password only for create mode
        if (!editingUserId) {
            payload.password = modalPassword.value.trim();
        }

        // Add OCR status only for edit mode
        if (editingUserId && modalOcrEnabled) {
            payload.ocr_enabled = modalOcrEnabled.checked;
        }

        // Validation
        if (!payload.name || !payload.email) {
            showToast('Name and email are required', 'error');
            return;
        }

        if (!editingUserId && !payload.password) {
            showToast('Password is required for new users', 'error');
            return;
        }

        if (!editingUserId && payload.password.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            return;
        }

        try {
            let res;
            if (editingUserId) {
                // Edit mode - PUT request
                res = await apiFetch(`/api/admin/users/${editingUserId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (!res.ok) throw new Error('Failed to update user');
                showToast('User updated successfully', 'success');
            } else {
                // Create mode - POST request
                res = await apiFetch('/api/admin/users', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (!res.ok) throw new Error('Failed to create user');
                showToast('User created successfully', 'success');
            }
            closeModal();
            await loadUsers();
        } catch (e) {
            showToast(e.message, 'error');
        }
    });

    // Init
    loadUsers();
});