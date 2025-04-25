function togglePassword(e) {
    const passwordInput = e.previousElementSibling;
    const toggleIcon = e.querySelector('i');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}


const tabs = {
    sanitary: {
        data: { main: [], car: [], tractor: [] },
        offset: { main: 0, car: 0, tractor: 0 },
        limit: 100,
        hasMore: { main: true, car: true, tractor: true },
        loading: false,
        activeSubtab: 'main',

        async init() {
            this.setupSubtabs();
            await this.loadData(true);
            await this.getObjects();

            document.getElementById("closeBreaksModal").addEventListener('click', () => {
                this.closeModal();
            });

            picker.on('selected', () => {
                this.filterTable();
            });
        
            document.addEventListener('datesCleared', ()=>{
                this.filterTable();
            })
            document.getElementById("searchObjectFirst").addEventListener("input", function() {
                this.filterTable();
            }.bind(this));
            
            document.getElementById("searchObjectSecond").addEventListener("input", function() {
                this.filterTable();
            }.bind(this));
            
            window.closeModal = this.closeModal.bind(this);
        },

        async getData(){
            try {
                const response = await fetch(`/api/sanitary_changes/${this.activeSubtab}?offset=${this.offset[this.activeSubtab]}&count=${this.limit}`);
                if (response.status === 403){
                    window.location.href = '/';
                }
                else if (response.status === 401){
                    window.location.href = '/login'
                }
                const newData = await response.json();
                return newData
            } catch (error) {
                console.error("Ошибка загрузки данных:", error);
            }
            return []
        },
        async searchData(object_from_id, object_to_id, start_time, end_time) {
            try {
                const params = {
                    offset: this.offset[this.activeSubtab],
                    count: this.limit,
                    ...(object_from_id && { object_from_id }),
                    ...(object_to_id && { object_to_id }),
                    ...(start_time && { start_time }),
                    ...(end_time && { end_time }),
                  };
                console.log(params);
                const queryString = new URLSearchParams(params).toString();
                const response = await fetch(`/api/sanitary_changes/search/${this.activeSubtab}?${queryString}`);
                if (!response.ok){
                    console.error(await response.text());
                    if (response.status === 403){
                        window.location.href = '/';
                    }
                    else if (response.status === 401){
                        window.location.href = '/login'
                    }
                }
                const newData = await response.json();
                return newData;
            } catch (error) {
                console.error("Ошибка поиска:", error);
            }
            return []
        },
        async loadData(reset = false, switch_tab=false) {
            if(switch_tab){
                const tbody = document.querySelector('#sanitaryTable tbody');
                tbody.innerHTML = "";
                if(this.data[this.activeSubtab].length > 0){
                    this.fillTable(this.data[this.activeSubtab]);
                    return
                }
            }
            if (this.loading || (!this.hasMore[this.activeSubtab] && !reset)) return;

            this.loading = true;

            if (reset) {
                const tbody = document.querySelector('#sanitaryTable tbody');
                tbody.innerHTML = "";
                this.offset[this.activeSubtab] = 0;
                this.hasMore[this.activeSubtab] = true;
                this.data[this.activeSubtab] = [];
            }

            let objectFirst = document.getElementById('searchObjectFirst').value.trim();
            let objectSecond = document.getElementById('searchObjectSecond').value.trim();
            let startDate = picker.getStartDate()?.format('DD-MM-YYYY');
            let endDate = picker.getEndDate()?.format('DD-MM-YYYY');

            let newData;
            if (objectFirst || objectSecond || startDate || endDate) {
                newData = await this.searchData(nameValue, objectId, startDate, endDate);
            } else {
                newData = await this.getData();
            }
            this.data[this.activeSubtab].push(...newData);
            this.offset[this.activeSubtab] += newData.length;
            this.fillTable(newData);
            if (newData.length < this.limit) {
                this.hasMore[this.activeSubtab] = false;
            }
            this.loading = false;
        },
        async filterTable() {
            const tbody = document.querySelector('#sanitaryTable tbody');
            tbody.innerHTML = "";

            this.offset[this.activeSubtab] = 0;
            this.hasMore[this.activeSubtab] = true;
            this.loading = false;

            let objectFirst = document.getElementById('searchObjectFirst').value.trim();
            let objectSecond = document.getElementById('searchObjectSecond').value.trim();
            let startDate = picker.getStartDate()?.format('DD-MM-YYYY');
            let endDate = picker.getEndDate()?.format('DD-MM-YYYY');
            
            let newData = await this.searchData(objectFirst, objectSecond, startDate, endDate);
            this.data[this.activeSubtab].push(...newData)
            this.offset[this.activeSubtab] += newData.length;
            this.fillTable(newData);

            if (newData.length < this.limit) {
                this.hasMore[this.activeSubtab] = false;
            }
            this.loading = false;
        },
        setupSubtabs() {
            document.querySelectorAll('.subtab-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    this.activeSubtab = btn.dataset.type;
                    this.loadData(false, true);
                });
            });
        },
        fillTable(data) {
            const tbody = document.querySelector('#sanitaryTable tbody');
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.id}</td>
                    <td>${row.user.username}</td>
                    <td>${row.time_changed}</td>
                    <td>Смена карантина ${row.sanitary_break.object_from.name} на объект ${row.sanitary_break.object_to.name} c ${row.time_from} на ${row.time_to} часов</td>`;
                tr.addEventListener("click", () => this.openModal(row));
                tbody.appendChild(tr);
            });
        },
        
        openModal(entry) {
            document.body.classList.add('modal-open');
            document.getElementById("breaksModal").style.display = "block";
        
            document.getElementById("modalBreakId").textContent = entry.id;
            document.getElementById("modalBreakUser").textContent = entry.user.username;
            document.getElementById("modalBreakDate").textContent = entry.time_changed;
            document.getElementById("modalBreakAction").textContent = `Смена карантина ${entry.sanitary_break.object_from.name} на объект ${entry.sanitary_break.object_to.name} c ${entry.time_from} на ${entry.time_to} часов`;
        },

        closeModal() {
            document.body.classList.remove('modal-open');
            document.getElementById("breaksModal").style.display = "none";
        },
        async getObjects(){            
            let objectFirst = document.getElementById('searchObjectFirst');
            let objectSecond = document.getElementById('searchObjectSecond');
            
            objectFirst.innerHTML = '<option value="">Выберите объект 1</option>';
            objectSecond.innerHTML = '<option value="">Выберите объект 2</option>';
            try {
                const response = await fetch("/api/objects/");
                if (response.status === 401){
                    window.location.href = '/login'
                }
                const objects = await response.json();
                objects.forEach(object => {
                    const option = document.createElement("option");
                    option.value = object.id;
                    option.textContent = object.name;
                    objectFirst.appendChild(option);

                    const option2 = document.createElement("option");
                    option2.value = object.id;
                    option2.textContent = object.name;
                    objectSecond.appendChild(option2);
                });
            } catch (error) {
                console.error("Ошибка загрузки объектов:", error);
            }
        }
    },
    users: {
        data: [],
        offset: 0,
        limit: 100,
        hasMore: true,
        loading: false,
        async init() {
            await this.loadData(true);

            document.getElementById("closeUsersModal").addEventListener('click', () => {
                this.closeModal();
            });

            window.closeModal = closeModal;
        },
        async loadData(reset = false) {
            if (this.loading || (!this.hasMore && !reset)) return;

            this.loading = true;

            if (reset) {
                this.offset = 0;
                this.hasMore = true;
                this.data = [];
                this.fillTable();
            }

            try {
                const response = await fetch(`/api/users?offset=${this.offset}&count=${this.limit}`);
                if (!response.ok) {
                    if (response.status === 401) {
                        window.location.href = '/login';
                    } else if (response.status === 403) {
                        window.location.href = '/';
                    }
                    throw new Error('Ошибка загрузки данных');
                }
                const newData = await response.json();
                this.data.push(...newData);
                this.offset += newData.length;
                if (newData.length < this.limit) {
                    this.hasMore = false;
                }
                this.fillTable();
            } catch (error) {
                console.error('Ошибка загрузки данных для users:', error);
            } finally {
                this.loading = false;
            }
        },

        fillTable() {
            const tbody = document.querySelector('#usersTable tbody');
            tbody.innerHTML = '';
            this.data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.id}</td>
                    <td>${row.username}</td>
                    <td>${row.full_name}</td>
                    <td class="hide-on-small">${row.phone}</td>
                    <td class="hide-on-small">${row.is_superuser ? 'Да' : 'Нет'}</td>`;
                tr.addEventListener("click", () => this.openModal(row));
                tbody.appendChild(tr);
            });
        },

        openModal(entry) {
            document.body.classList.add('modal-open');
            document.getElementById("usersModal").style.display = "block";
        
            document.getElementById("modalUserId").textContent = entry.id;
            document.getElementById("modalUserNickname").textContent = entry.username;
            document.getElementById("modalUserFullName").textContent = entry.full_name;
            document.getElementById("modalUserPhone").textContent = entry.phone;
            document.getElementById("modalUserSuperuser").textContent = entry.is_superuser ? 'Да' : 'Нет';
        },

        closeModal() {
            document.body.classList.remove('modal-open');
            document.getElementById("usersModal").style.display = "none";
        }
    },
    add_user: {
        init() {
            this.setupForm();
        },
        setupForm() {
            const form = document.getElementById('addUserForm');
            if (form) {
                form.addEventListener('submit', async e => {
                    e.preventDefault();
                    const userData = {
                        username: document.getElementById('addUsername').value,
                        full_name: document.getElementById('addFullName').value,
                        phone: document.getElementById('addPhone').value,
                        password: document.getElementById('addGeneratedPassword').value
                    };
                    try {
                        const res = await fetch('/api/users/register', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(userData)
                        });
                        if (!res.ok) throw new Error('Ошибка при добавлении пользователя: ' + await res.text());
                        alert('Пользователь добавлен');
                        document.getElementById('addGeneratedPassword').value = '';
                    } catch (err) {
                        alert('Ошибка: ' + err.message);
                    }
                });
            }
        }
    },
    account: {
        init() {
            this.setupForm();
            this.setupPasswordModal();
        },
        setupForm() {
            const editBtn = document.getElementById('editAccountBtn');
            const saveBtn = document.getElementById('saveAccountBtn');
            const cancelBtn = document.getElementById('cancelEditBtn');
            const inputs = document.querySelectorAll('#accountForm input');
            let originalValues = {};

            editBtn.addEventListener('click', () => {
                inputs.forEach(input => {
                    originalValues[input.id] = input.value;
                    input.disabled = false;
                });
                editBtn.style.display = 'none';
                document.getElementById('changePasswordBtn').style.display = 'none';
                saveBtn.style.display = 'inline-flex';
                cancelBtn.style.display = 'inline-flex';
            });

            cancelBtn.addEventListener('click', () => {
                inputs.forEach(input => {
                    input.value = originalValues[input.id];
                    input.disabled = true;
                });
                editBtn.style.display = 'inline-flex';
                document.getElementById('changePasswordBtn').style.display = 'inline-flex';
                saveBtn.style.display = 'none';
                cancelBtn.style.display = 'none';
            });

            saveBtn.addEventListener('click', async () => {
                const userData = {
                    username: document.getElementById('accountUsername').value,
                    full_name: document.getElementById('accountFullName').value,
                    phone: document.getElementById('accountPhone').value
                };
                const response = await fetch(`/api/users/${userData.username}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });
                if (!response.ok) {
                    if (response.status === 403) window.location.href = '/';
                    else alert('Ошибка при изменении данных');
                }
                window.location.reload();
            });
        },
        setupPasswordModal() {
            const passwordModal = document.getElementById('passwordModal');
            const changePasswordBtn = document.getElementById('changePasswordBtn');
            const closeModal = document.getElementById('closeModal');
            const passwordForm = document.getElementById('passwordForm');

            passwordModal.style.display = 'none';

            changePasswordBtn.addEventListener('click', () => {
                passwordModal.style.display = 'flex';
            });

            closeModal.addEventListener('click', () => {
                passwordModal.style.display = 'none';
            });

            passwordForm.addEventListener('submit', async e => {
                e.preventDefault();
                const username = document.getElementById('accountUsername').value;
                const password = document.getElementById('currentPassword').value;
                const new_password = document.getElementById('newPassword').value;
                const confirm_password = document.getElementById('confirmPassword').value;

                if (new_password !== confirm_password) {
                    alert('Пароли различаются');
                    return;
                }

                try {
                    const response = await fetch('/api/users/change_password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password, new_password })
                    });
                    if (response.ok) {
                        alert('Успешно');
                        passwordModal.style.display = 'none';
                    } else {
                        alert('Ошибка смены пароля. Проверьте пароль.');
                    }
                } catch (error) {
                    alert('Произошла ошибка при смене пароля.');
                }
                passwordForm.reset();
            });
        }
    }
};

async function getSanitaryBreaks(break_type, offset, count) {
    try {
        const response = await fetch(`/api/sanitary_changes/${break_type}?offset=${offset}&count=${count}`);
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
            }
            throw new Error('Ошибка загрузки данных');
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка загрузки объектов:', error);
        return [];
    }
}

function generatePassword() {
    const password = Math.random().toString(36).slice(-8);
    document.getElementById('addGeneratedPassword').value = password;
}

document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    function activateTab(tabId) {
        tabButtons.forEach(btn => {
            const isActive = btn.getAttribute('data-tab') === tabId;
            btn.classList.toggle('active', isActive);
        });

        tabContents.forEach(content => {
            content.classList.toggle('active', content.id === tabId);
        });

        if (tabs[tabId]) {
            tabs[tabId].init();
        }
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            activateTab(tabId);
            history.replaceState(null, null, `#${tabId}`);
        });
    });

    // Centralized scroll event listener
    window.addEventListener('scroll', async () => {
        const scrollPosition = window.scrollY + window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (scrollPosition >= documentHeight - 100) {
            if (document.querySelector('#sanitary').classList.contains('active') && !tabs.sanitary.loading) {
                await tabs.sanitary.loadData(false);
            } else if (document.querySelector('#users').classList.contains('active') && !tabs.users.loading) {
                await tabs.users.loadData(false);
            }
        }
    });

    const hash = window.location.hash.slice(1);
    if (hash && tabs[hash]) {
        activateTab(hash);
    } else {
        activateTab('sanitary');
    }
});