document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchObject = document.getElementById("searchObject");
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

    async function searchData(full_name) {
        try {
            const response = await fetch(`/api/employees/search?full_name=${encodeURIComponent(full_name)}`);
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
        if (nameValue.length > 0) {
            await searchData(nameValue);
        } else {
            tableBody.innerHTML = ""; // Очищаем таблицу, если поле пустое
        }
    }

    function openModal(entry) {
        document.getElementById("modal").style.display = "block";
        document.getElementById("modalId").textContent = entry.id;
        document.getElementById("modalName").textContent = entry.full_name;
        document.getElementById("modalObject").textContent = entry.position ? entry.position.title : "Не установлено";
    }

    function closeModal() {
        document.getElementById("modal").style.display = "none";
    }

    searchName.addEventListener("input", filterTable);
    searchObject.addEventListener("input", filterTable);

    getData();

    window.closeModal = closeModal;
});