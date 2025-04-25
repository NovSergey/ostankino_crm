import { openModalEmployee, openModalSecurity } from '/static/table/script.js';

document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchObject = document.getElementById("searchObject");
    const searchDate = document.getElementById("datepicker");
    const tableBody = document.getElementById("tableBody");


    let offset = 0;
    const limit = 100;
    let loading = false;
    let hasMore = true;

    document.querySelectorAll('.fake-placeholder-input input[type="date"]').forEach(input => {
        input.addEventListener('input', () => {
            input.classList.toggle('has-value', !!input.value);
        });
    });

    function renderTable(data) {
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
            const response = await fetch(`/api/visit_history?offset=${offset}&count=${limit}`);
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            const data = await response.json();
            renderTable(data);
            return data.length;
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
    }

    async function searchData(full_name, object_id, start_time, end_time) {
        try {
            const params = {
                offset: offset,
                count: limit,
                full_name: full_name,
                ...(object_id && { object_id }),
                ...(start_time && { start_time }),
                ...(end_time && { end_time }),
              };
              
            const queryString = new URLSearchParams(params).toString();
            const response = await fetch(`/api/visit_history/search?${queryString}`);
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
            return data.length;
        } catch (error) {
            console.error("Ошибка поиска:", error);
        }
    }


    async function loadEmployees(reset = false) {
        if (loading || (!hasMore && !reset)) return;

        loading = true;

        if (reset) {
            offset = 0;
            hasMore = true;
            tableBody.innerHTML = "";
        }

        const nameValue = searchName.value.trim();
        const objectId = searchObject.value.trim();
        const startDate = picker.getStartDate()?.format('DD-MM-YYYY');
        const endDate = picker.getEndDate()?.format('DD-MM-YYYY');

        let data_count = 0;
        if (nameValue || objectId || startDate || endDate) {
            data_count = await searchData(nameValue, objectId, startDate, endDate);
        } else {
            data_count = await getData();
        }
        offset += data_count;
        if (data_count < limit) {
            hasMore = false;
        }
        loading = false;
        
    }
    
    async function filterTable() {
        tableBody.innerHTML = "";
        offset = 0;
        hasMore = true;
        loading = false;
        let nameValue = searchName.value.trim();
        let groupId = searchObject.value.trim();
        let startDate = picker.getStartDate()?.format('DD-MM-YYYY');
        let endDate = picker.getEndDate()?.format('DD-MM-YYYY');

        let data_count = await searchData(nameValue, groupId, startDate, endDate);
        offset += data_count;
        if (data_count < limit) {
            hasMore = false;
        }
        loading = false;
    }

    
    async function getObjects() {
        searchObject.innerHTML = '<option value="">Выберите объект</option>';
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
    }

    window.addEventListener("scroll", async () => {
        const scrollPosition = window.scrollY + window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (scrollPosition >= documentHeight - 100 && !loading) {
            await loadEmployees(false);
        }
    });

    searchName.addEventListener("input", filterTable);
    searchObject.addEventListener("input", filterTable);
    
    picker.on('selected', () => {
        filterTable();
    });

    document.addEventListener('datesCleared', ()=>{
        filterTable();
    })


    loadEmployees(true);
    getObjects();
});

