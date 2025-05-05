let tableData = {};
let isEditing = false;
let objectsList = [];

document.addEventListener("DOMContentLoaded", () => {
    async function getObjects() {
        try {
            const response = await fetch("/api/objects/");
            if (response.status === 401) {
                window.location.href = '/login/';
            }
            return await response.json();
        } catch (error) {
            console.error("Ошибка загрузки объектов:", error);
            return [];
        }
    }

    async function getBreaks() {
        try {
            const response = await fetch(`/api/sanitary_breaks/${TYPE_BREAK}/`);
            if (response.status === 401) {
                window.location.href = '/login/';
            }
            return await response.json();
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
            return [];
        }
    }

    function populateTable(objects, data) {
        objectsList = [...objects];
        tableData = {};

        data.forEach(item => {
            const key = `${item.object_from_id}_${item.object_to_id}`;
            tableData[key] = item.time_break;
        });

        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        const tableHead = document.getElementById('table-head');
        tableHead.innerHTML = '';

        const column = document.createElement('tr');
        const columnCell = document.createElement('th');
        column.appendChild(columnCell);
        objects.forEach(fromObj => {
            const row = document.createElement('tr');

            const firstCell = document.createElement('td');
            firstCell.textContent = fromObj.name;
            
            const columnCell = document.createElement('th');
            columnCell.textContent = fromObj.name;
            
            row.appendChild(firstCell);
            column.appendChild(columnCell);

            objects.forEach(toObj => {
                const cell = document.createElement('td');
                const key = `${fromObj.id}_${toObj.id}`;
            
                if (fromObj.id === toObj.id) {
                    cell.textContent = '—';
                    cell.classList.add('disabled-cell');
                    cell.dataset.disabled = 'true';
                } else {
                    cell.textContent = tableData[key] || '';
                    cell.dataset.key = key;
                }
            
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
        
        tableHead.appendChild(column);
    }

    function toggleEditMode() {
        const editBtn = document.getElementById('edit-btn');
        const saveBtn = document.getElementById('save-btn');
        const cells = document.querySelectorAll('#table-body td:not(:first-child)');

        if (!isEditing) {
            isEditing = true;
            editBtn.textContent = 'Отменить';
            saveBtn.style.display = 'inline-block';

            cells.forEach(cell => {
                if (cell.dataset.disabled === 'true') return;
                
                const value = cell.textContent.trim();
                const input = document.createElement('input');
                input.type = 'number';
                input.value = value;
                cell.innerHTML = '';
                cell.appendChild(input);
                cell.classList.add('editable-cell');

                input.addEventListener('input', () => {
                    if (input.value !== (tableData[cell.dataset.key] ?? '').toString()) {
                        cell.classList.add('changed-cell');
                    } else {
                        cell.classList.remove('changed-cell');
                    }
                });
            });
        } else {
            isEditing = false;
            editBtn.textContent = 'Редактировать разрывы';
            saveBtn.style.display = 'none';
            fetchData(); // обновляем данные с сервера
        }
    }

    async function saveChanges() {
        const cells = document.querySelectorAll('#table-body td.editable-cell');
        const updatedData = [];

        cells.forEach(cell => {
            const input = cell.querySelector('input');
            const key = cell.dataset.key;
            const [fromId, toId] = key.split('_').map(Number);
            const newValue = parseInt(input.value.trim());

            if (!isNaN(newValue) && newValue !== tableData[key]) {
                updatedData.push({
                    object_from_id: fromId,
                    object_to_id: toId,
                    time_break: newValue
                });
                tableData[key] = newValue;
            }
        });

        if (updatedData.length > 0) {
            try {
                const response = await fetch(`/api/sanitary_breaks/${TYPE_BREAK}/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedData)
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        window.location.href = '/login/';
                    }
                    throw new Error('Ошибка при сохранении данных');
                }
            } catch (error) {
                console.error('Ошибка при отправке данных:', error);
                alert('Не удалось сохранить изменения. Попробуйте позже.');
            }
        }

        isEditing = false;
        document.getElementById('edit-btn').textContent = 'Редактировать разрывы';
        document.getElementById('save-btn').style.display = 'none';
        fetchData();
    }

    async function fetchData() {
        const objects = await getObjects();
        const data = await getBreaks();
        populateTable(objects, data);
    }

    document.getElementById('edit-btn').addEventListener('click', toggleEditMode);
    document.getElementById('save-btn').addEventListener('click', saveChanges);

    fetchData();
});
