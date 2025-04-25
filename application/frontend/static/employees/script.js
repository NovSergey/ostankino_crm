document.addEventListener("DOMContentLoaded", () => {
    const searchName = document.getElementById("searchName");
    const searchPhone = document.getElementById("searchPhone");
    const searchGroup = document.getElementById("searchGroup");
    const searchObject = document.getElementById("searchObject");
    const tableBody = document.getElementById("tableBody");

    let offset = 0;
    const limit = 100;
    let loading = false;
    let hasMore = true;

    async function getData() {
        try {
            const response = await fetch(`/api/employees?offset=${offset}&count=${limit}`);
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            const data = await response.json();
            renderTable(data);
            return data.length
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
        return 0
    }

    async function searchData(full_name, phone, group_id, object_id) {
        try {
            const params = {
                offset: offset,
                count: limit,
                full_name: full_name,
                phone: phone,
                ...(group_id && { group_id }),
                ...(object_id && { object_id }),
              };
              
            const queryString = new URLSearchParams(params).toString();
            const response = await fetch(`/api/employees/search?${queryString}`);
            if (!response.ok){
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
        return 0;
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
        const phoneValue = searchPhone.value.trim();
        const groupId = searchGroup.value.trim();
        const objectId = searchObject.value.trim();

        let data_count = 0;
        if (nameValue || phoneValue || groupId || objectId) {
            data_count = await searchData(nameValue, phoneValue, groupId, objectId);
        } else {
            data_count = await getData();
        }
        offset += data_count;
        if (data_count < limit) {
            hasMore = false;
        }
        loading = false;
        
    }

    async function getGroups() {
        searchGroup.innerHTML = '<option value="">Выберите группу</option>';
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
        searchObject.innerHTML += '<option value="-1">Не установлено</option>';
    }

    function renderTable(data) {
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
        tableBody.innerHTML = "";
        offset = 0;
        hasMore = true;
        loading = false;
        let nameValue = searchName.value.trim();
        let phoneValue = searchPhone.value.trim();
        let groupId = searchGroup.value.trim();
        let objectId = searchObject.value.trim();

        let data_count = await searchData(nameValue, phoneValue, groupId, objectId);
        offset += data_count;
        if (data_count < limit) {
            hasMore = false;
        }
        loading = false;
    }

    function openModal(entry) {
        document.body.classList.add('modal-open');
        document.getElementById("modal").style.display = "block";
        document.getElementById("modalId").textContent = entry.id;
        document.getElementById("modalId").setAttribute("href", "/employees/"+entry.id)
        document.getElementById("modalName").textContent = entry.full_name;
        document.getElementById("modalPhone").textContent = entry.phone;
        document.getElementById("modalObject").textContent = entry.object ? entry.object.name : "Не установлено";
        document.getElementById("modalGroup").textContent = entry.group ? entry.group.title : "Не установлено";
    }

    function closeModal() {
        document.body.classList.remove('modal-open');
        document.getElementById("modal").style.display = "none";
    }


    window.addEventListener("scroll", async () => {
        const scrollPosition = window.scrollY + window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (scrollPosition >= documentHeight - 100 && !loading) {
            await loadEmployees(false);
        }
    });

    searchName.addEventListener("input", filterTable);
    searchPhone.addEventListener("input", filterTable);
    searchGroup.addEventListener("input", filterTable);
    searchObject.addEventListener("input", filterTable);

    loadEmployees(true);
    getGroups();
    getObjects();
    window.closeModal = closeModal;
});