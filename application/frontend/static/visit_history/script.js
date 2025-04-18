import { openModalEmployee, openModalSecurity } from '/static/table/script.js';

document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchObject = document.getElementById("searchObject");
    const tableBody = document.getElementById("tableBody");

    function renderTable(data) {
        tableBody.innerHTML = "";
        data.forEach(entry => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td class="hide-on-small">${entry.id}</td>
                <td>${entry.employee.full_name}</td>
                <td>${entry.object.name}</td>
                <td>${entry.entry_time}</td>
                <td>${entry.exit_time ? entry.exit_time : "-"}</td>
                <td class="hide-on-small">${entry.status}</td>
                <td class="hide-on-small">${entry.employee.role == "security" ? '-' : entry.scanned_by_user.full_name}</td>
            `;
            if (entry.employee.role == "security"){
                row.addEventListener("click", () => openModalSecurity(entry));
            }
            else{
                row.addEventListener("click", () => openModalEmployee(entry));
                
            }
            tableBody.appendChild(row);
        });
    }

    async function getData() {
        try {
            const response = await fetch("/api/visit_history/");
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

    async function getObjects() {
        searchObject.innerHTML = '<option value="">Выберите объект...</option>';
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
                searchObject.appendChild(option);
            });
        } catch (error) {
            console.error("Ошибка загрузки объектов:", error);
        }
        searchObject.innerHTML += '<option value="-1">Не установлено</option>';
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

    async function filterTable() {
        let nameValue = searchName.value.trim();
        let groupId = searchGroup.value.trim();
        await searchData(nameValue, groupId);
    }
    searchName.addEventListener("input", filterTable);
    searchObject.addEventListener("input", filterTable);

    getData();
    getObjects();
});