function toggleMenu() {
    document.querySelector('.nav-menu').classList.toggle('active');
    document.querySelector('.hamburger').classList.toggle('active');
}

document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = toggle.parentElement;
        parent.classList.toggle('active');
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const dataBody = document.getElementById("notification-container");
    const toggleBtn = document.getElementById("filter-btn");

    let offset = 0;
    const limit = 20;
    let loading = false;
    let allLoaded = false;
    let readFilter = false;

    async function getData() {
        if (loading || allLoaded) return;
        loading = true;

        try {
            const response = await fetch(`/api/notifications?active=${readFilter}&offset=${offset}&count=${limit}`);
            if (response.status === 403) {
                window.location.href = '/login';
                return;
            }

            const data = await response.json();
            if (data.length < limit) {
                allLoaded = true;
            }

            renderObjects(data);
            offset += data.length;

        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }

        loading = false;
    }

    function renderObjects(data) {
        data.forEach(entry => {
            const li = document.createElement("li");
            li.classList.add("notification-item");
            if (!entry.is_read) li.classList.add("unread");

            const icon = document.createElement("i");
            icon.classList.add("notification-icon", "fas", "fa-exclamation-circle");

            const content = document.createElement("div");
            content.classList.add("notification-content");
            content.innerHTML = `
                <p class="notification-title">${entry.title}</p>
                <p class="notification-message">${entry.message}</p>
                <p class="notification-time">${entry.time}</p>
            `;

            const actions = document.createElement("div");
            actions.classList.add("notification-actions");

            if (!entry.is_read) {
                const button = document.createElement("button");
                button.textContent = "Пометить как прочитанное";
                button.onclick = function () {
                    markAsRead(button, entry.id);
                };
                actions.appendChild(button);
            }

            li.appendChild(icon);
            li.appendChild(content);
            li.appendChild(actions);
            dataBody.appendChild(li);
        });
    }

    async function markAsRead(button, id) {
        try {
            const response = await fetch(`/api/notifications/read/${id}`, { method: 'POST' });
            if (!response.ok) {
                if (response.status === 403) {
                    window.location.href = '/login';
                } else {
                    alert("Не удалось пометить прочитанным");
                    return;
                }
            }
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
            alert("Не удалось пометить прочитанным");
            return;
        }
        const notification = button.closest('.notification-item');
        notification.classList.remove('unread');
        button.remove();
    }

    window.addEventListener("scroll", () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
            getData();
        }
    });

    toggleBtn.addEventListener("click", () => {
        readFilter = !readFilter;
        offset = 0;
        allLoaded = false;
        dataBody.innerHTML = "";
        toggleBtn.textContent = readFilter ? "Показать непрочитанные" : "Показать прочитанные";
        getData();
    });

    getData();
});