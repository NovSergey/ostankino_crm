document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchGroup = document.getElementById("searchGroup");
    const tableBody = document.getElementById("tableBody");

    async function getData() {
        try {
            const response = await fetch("/api/employees/");
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            const data = await response.json();
            renderTable(data);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
    }

    async function getGroups() {
        searchGroup.innerHTML = '<option value="">Выберите объект...</option>';
        try {
            const response = await fetch("/api/groups/");
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            const groups = await response.json();
            groups.forEach(pos => {
                const option = document.createElement("option");
                option.value = pos.id;
                option.textContent = pos.title;
                searchGroup.appendChild(option);
            });
        } catch (error) {
            console.error("Ошибка загрузки объектов:", error);
        }
        searchGroup.innerHTML += '<option value="-1">Не установлено</option>';
    }

    async function searchData(full_name, group_id) {
        try {
            const response = await fetch(`/api/employees/search?full_name=${encodeURIComponent(full_name)}&${group_id != "" ? "group_id="+group_id:""}`);
            if (!response.ok){
                console.log(full_name);
                console.error(await response.text());
                if (response.status === 403){
                    window.location.href = '/';
                }
                else if (response.status === 401){
                    window.location.href = '/login'
                }
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
                <td class="hide-on-small">${entry.phone}</td>
                <td>${entry.object ? entry.object.name : "Не установлено"}</td>
                <td>${entry.group ? entry.group.title : "Не установлено"}</td>
            `;
            row.addEventListener("click", () => openModal(entry));
            tableBody.appendChild(row);
        });
    }

    async function filterTable() {
        let nameValue = searchName.value.trim();
        let groupId = searchGroup.value.trim();
        await searchData(nameValue, groupId);
    }

    function openModal(entry) {
        document.getElementById("modal").style.display = "block";
        document.getElementById("modalId").textContent = entry.id;
        document.getElementById("modalName").textContent = entry.full_name;
        document.getElementById("modalPhone").textContent = entry.phone;
        document.getElementById("modalObject").textContent = entry.object ? entry.object.name : "Не установлено";
        document.getElementById("modalGroup").textContent = entry.group ? entry.group.title : "Не установлено";
    }

    function closeModal() {
        document.getElementById("modal").style.display = "none";
    }

    searchName.addEventListener("input", filterTable);
    searchGroup.addEventListener("input", filterTable);

    getData();
    getGroups();
    window.closeModal = closeModal;
});