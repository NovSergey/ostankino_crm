document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchPosition = document.getElementById("searchPosition");
    const tableBody = document.getElementById("tableBody");

    async function getData() {
        try {
            const response = await fetch("/api/employees/");
            const data = await response.json();
            renderTable(data);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
    }

    async function getPositions() {
        searchPosition.innerHTML = '<option value="">Выберите объект...</option>';
        try {
            const response = await fetch("/api/positions/");
            const positions = await response.json();
            positions.forEach(pos => {
                const option = document.createElement("option");
                option.value = pos.id;
                option.textContent = pos.title;
                searchPosition.appendChild(option);
            });
        } catch (error) {
            console.error("Ошибка загрузки объектов:", error);
        }
        searchPosition.innerHTML += '<option value="-1">Не установлено</option>';
    }

    async function searchData(full_name, position_id) {
        try {
            const response = await fetch(`/api/employees/search?full_name=${encodeURIComponent(full_name)}&${position_id != "" ? "position_id="+position_id:""}`);
            if (!response.ok){
                console.log(full_name);
                console.error(await response.text());
                throw new Error("Ошибка загрузки данных");
            }
            const data = await response.json();
            renderTable(data);
        } catch (error) {
            console.error("Ошибка поиска:", error);
        }
    }
    function renderTable(data) {
        tableBody.innerHTML = "";
        data.forEach(entry => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td class="hide-on-small">${entry.id}</td>
                <td>${entry.full_name}</td>
                <td>${entry.position ? entry.position.title : "Не установлено"}</td>
            `;
            row.addEventListener("click", () => openModal(entry));
            tableBody.appendChild(row);
        });
    }

    async function filterTable() {
        let nameValue = searchName.value.trim();
        let positionId = searchPosition.value.trim();
        await searchData(nameValue, positionId);
    }

    function openModal(entry) {
        document.getElementById("modal").style.display = "block";
        document.getElementById("modalId").textContent = entry.id;
        document.getElementById("modalName").textContent = entry.full_name;
        document.getElementById("modalPosition").textContent = entry.position ? entry.position.title : "Не установлено";
    }

    function closeModal() {
        document.getElementById("modal").style.display = "none";
    }

    searchName.addEventListener("input", filterTable);
    searchPosition.addEventListener("input", filterTable);

    getData();
    getPositions();
    window.closeModal = closeModal;
});


// Функции для меню
function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
}

// Закрытие меню при клике вне области
document.addEventListener('click', (e) => {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');

    if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Закрытие меню при изменении размера окна
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        const navMenu = document.querySelector('.nav-menu');
        const hamburger = document.querySelector('.hamburger');
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});