// Глобальная переменная для хранения данных
let tableData = {};
let isEditing = false;

// Функция для заполнения таблицы
function populateTable(data) {
    tableData = { ...data }; // Сохраняем данные для редактирования
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; // Очищаем таблицу перед заполнением

    const objects = ['ПТО-1', 'ПТО-2', 'ПТО-3', 'ТП-1', 'ТП-2', 'ТП-3', 'ТП-4', 'ФБО-1', 'ФБО-2', 'ФБО-3', 'ФБО-4', 'Крепость', 'Условия труда'];

    objects.forEach((object, rowIndex) => {
        const row = document.createElement('tr');
        const firstCell = document.createElement('td');
        firstCell.textContent = object;
        row.appendChild(firstCell);

        for (let colIndex = 0; colIndex < objects.length; colIndex++) {
            const cell = document.createElement('td');
            const key = `${object}_${objects[colIndex]}`;
            cell.textContent = data[key] || '';
            cell.dataset.key = key; // Сохраняем ключ для редактирования
            row.appendChild(cell);
        }

        tableBody.appendChild(row);
    });
}

// Функция для переключения режима редактирования
function toggleEditMode() {
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');
    const cells = document.querySelectorAll('#table-body td:not(:first-child)'); // Все ячейки, кроме первого столбца

    if (!isEditing) {
        // Включаем режим редактирования
        isEditing = true;
        editBtn.textContent = 'Отменить';
        saveBtn.style.display = 'inline-block';

        cells.forEach(cell => {
            if (cell.textContent.trim() !== '') { // Редактируем только непустые ячейки
                const input = document.createElement('input');
                input.type = 'text';
                input.value = cell.textContent;
                cell.innerHTML = '';
                cell.appendChild(input);
                cell.classList.add('editable-cell');
                input.addEventListener('input', () => {
                  if (input.value !== tableData[cell.dataset.key]) {
                      cell.classList.add('changed-cell');
                  } else {
                      cell.classList.remove('changed-cell');
                  }
              });
            }
        });
    } else {
        // Выключаем режим редактирования без сохранения
        isEditing = false;
        editBtn.textContent = 'Редактировать разрывы';
        saveBtn.style.display = 'none';
        populateTable(tableData); // Возвращаем исходные данные
    }
}

// Функция для сохранения изменений
async function saveChanges() {
    const cells = document.querySelectorAll('#table-body td.editable-cell');
    const updatedData = {};

    // Собираем изменённые данные
    cells.forEach(cell => {
        const input = cell.querySelector('input');
        const key = cell.dataset.key;
        const newValue = input.value.trim();

        if (newValue !== tableData[key]) {
            updatedData[key] = newValue;
            tableData[key] = newValue; // Обновляем локальные данные
        }
    });

    // Если есть изменения, отправляем их на сервер
    if (Object.keys(updatedData).length > 0) {
        try {
            // const response = await fetch('/api/schedule/update', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(updatedData),
            // });

            // if (response.ok) {
            //     alert('Изменения успешно сохранены!');
            // } else {
            //     throw new Error('Ошибка при сохранении данных');
            // }
            console.log("Изменения:", JSON.stringify(updatedData));
        } catch (error) {
            console.error('Ошибка при отправке данных:', error);
            alert('Не удалось сохранить изменения. Попробуйте позже.');
        }
    }

    // Выключаем режим редактирования
    isEditing = false;
    document.getElementById('edit-btn').textContent = 'Редактировать разрывы';
    document.getElementById('save-btn').style.display = 'none';
    populateTable(tableData); // Обновляем таблицу
}

// Функция для получения данных с сервера
async function fetchData() {
    try {
        // const response = await fetch('/api/schedule');
        // const data = await response.json();
        let data = {
          "ПТО-1_ПТО-1": "64",
          "ПТО-2_ПТО-2": "64",
          "ПТО-3_ПТО-3": "64",
          "ТП-1_ТП-1": "64",
          "ТП-2_ПТО-1": "15",
          "ТП-2_ПТО-2": "15",
          "ТП-2_ПТО-3": "15",
          "ТП-2_ТП-1": "15",
          "ТП-3_ТП-3": "336",
          "ТП-4_ТП-4": "64",
          "ФБО-1_ФБО-1": "64",
          "ФБО-2_ФБО-2": "64",
          "ФБО-3_ФБО-3": "336",
          "ФБО-4_ФБО-4": "64",
          "Крепость_Крепость": "64",
          "Условия труда_Условия труда": "64"
        }
        populateTable(data);
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
        alert('Не удалось загрузить данные. Попробуйте позже.');
    }
}

// Добавляем обработчики событий
document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    document.getElementById('edit-btn').addEventListener('click', toggleEditMode);
    document.getElementById('save-btn').addEventListener('click', saveChanges);
});

// Функция для переключения меню (уже есть в вашем коде)
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
}