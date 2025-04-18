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
    document.getElementById("generatedPassword").value = password;
}


document.getElementById("userForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const userData = {
        "username": document.getElementById("username").value,
        "full_name": document.getElementById("full_name").value,
        "phone": document.getElementById("phone").value,
        "password": document.getElementById("generatedPassword").value,
    }
    console.log(userData);
    try {
        const res = await fetch("/api/users/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData)
        });

        if (!res.ok) throw new Error("Ошибка при добавлении пользователя");

        alert("Пользователь добавлен");
        document.getElementById("generatedPassword").value = "";
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
});
