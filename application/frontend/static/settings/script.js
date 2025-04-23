let sanitaryData = {};
let groups = [];
let visitHistory = [];

async function getSanitaryBreaks(break_type) {
    try {
        const response = await fetch(`/api/sanitary_changes/${break_type}`);
        if (!response.ok){
            if (response.status === 401) {
                window.location.href = '/login';
            }
        }
        return await response.json();
    } catch (error) {
        console.error("Ошибка загрузки объектов:", error);
        return [];
    }
}


document.addEventListener("DOMContentLoaded", async () => {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    const editBtn = document.getElementById("editAccountBtn");
    const saveBtn = document.getElementById("saveAccountBtn");
    const cancelBtn = document.getElementById("cancelEditBtn");
    const passwordlBtn = document.getElementById("changePasswordBtn");
    const inputs = document.querySelectorAll("#accountForm input");

    let originalValues = {};

    editBtn.addEventListener("click", () => {
        inputs.forEach(input => {
            originalValues[input.id] = input.value;
            input.disabled = false;
        });
        editBtn.style.display = "none";
        passwordlBtn.style.display = "none";
        saveBtn.style.display = "inline-flex";
        cancelBtn.style.display = "inline-flex";
    });

    cancelBtn.addEventListener("click", () => {
        inputs.forEach(input => {
            input.value = originalValues[input.id];
            input.disabled = true;
        });
        editBtn.style.display = "inline-flex";
        passwordlBtn.style.display = "inline-flex";
        saveBtn.style.display = "none";
        cancelBtn.style.display = "none";
    });

    function activateTab(tabId) {
        tabButtons.forEach(btn => {
            const isActive = btn.getAttribute('data-tab') === tabId;
            btn.classList.toggle('active', isActive);
        });

        tabContents.forEach(content => {
            content.classList.toggle('active', content.id === tabId);
        });
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            activateTab(tabId);
            history.replaceState(null, null, `#${tabId}`);
        });
    });

    const hash = window.location.hash.slice(1);
    if (hash) {
        activateTab(hash);
    }

    async function LoadData() {
        try {
            sanitaryData["main"] = await getSanitaryBreaks("main");
            sanitaryData["car"] = await getSanitaryBreaks("car");
            sanitaryData["tractor"] = await getSanitaryBreaks("tractor");
            fillSanitaryTable("main");
        } catch(error){
            console.error("Ошибка загрузки данных:", error);
        }
    }
    LoadData();
});


document.querySelectorAll(".subtab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".subtab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        fillSanitaryTable(btn.dataset.type);
    });
});

function fillSanitaryTable(type) {
    const tbody = document.querySelector("#sanitaryTable tbody");
    tbody.innerHTML = "";
    (sanitaryData[type] || []).forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML += `<td>${row.user.username}</td>`;
        tr.innerHTML += `<td>${row.time_changed}</td>`;
        tr.innerHTML += `<td>Смена карантина ${row.sanitary_break.object_from.name} на объект ${row.sanitary_break.object_to.name} c ${row.time_from} на ${row.time_to} часов</td>`;
        
        tbody.appendChild(tr);
    });
}

function generatePassword() {
    const password = Math.random().toString(36).slice(-8);
    document.getElementById("addGeneratedPassword").value = password;
}


document.getElementById("addUserForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const userData = {
        "username": document.getElementById("addUsername").value,
        "full_name": document.getElementById("addFullName").value,
        "phone": document.getElementById("addPhone").value,
        "password": document.getElementById("addGeneratedPassword").value,
    }
    console.log(userData);
    try {
        const res = await fetch("/api/users/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData)
        });

        if (!res.ok) throw new Error("Ошибка при добавлении пользователя" + await res.text());

        alert("Пользователь добавлен");
        document.getElementById("addGeneratedPassword").value = "";
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
});


document.getElementById('passwordModal').style.display = 'none';

document.getElementById('editAccountBtn').addEventListener('click', () => {
    ['accountUsername', 'accountFullName', 'accountPhone'].forEach(id => {
        document.getElementById(id).disabled = false;
    });
    document.getElementById('saveAccountBtn').style.display = 'inline-block';
});

document.getElementById('saveAccountBtn').addEventListener('click', async () => {
    const userData = {
        "username": document.getElementById("accountUsername").value,
        "full_name": document.getElementById("accountFullName").value,
        "phone": document.getElementById("accountPhone").value,
    }
    const response = await fetch(`/api/users/${userData["username"]}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    });
    if (!response.ok) {
        if(response.status === 403)
            window.location.href = '/';
        else
            alert("Ошибка при изменении данных");
    }
    window.location.reload();
});


document.getElementById('changePasswordBtn').addEventListener('click', () => {
    document.getElementById('passwordModal').style.display = 'flex';
});

document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('passwordModal').style.display = 'none';
});


document.getElementById('passwordForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const username = document.getElementById('accountUsername').value;
    const password = document.getElementById('currentPassword').value;
    const new_password = document.getElementById('newPassword').value;
    const confirm_password = document.getElementById('confirmPassword').value;
    if (new_password != confirm_password){
        alert('Пароли различаются');
        return;
    }
    try {
        const response = await fetch('/api/users/change_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "new_password": new_password
            })
        });

        if (response.ok) {
            alert("Успешно")
            document.getElementById('passwordModal').style.display = 'none';
        } else {
            console.error('Ошибка входа:', response.statusText);
            alert('Ошибка смены пароля. Проверьте пароль.');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при смене пароля.');
    }
    document.getElementById('passwordForm').reset();
});