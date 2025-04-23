import { openModalEmployee } from '/static/table/script.js';
import { openModalSecurity } from '/static/table/script.js';

document.addEventListener("DOMContentLoaded", () => {
    const employeeTable = document.getElementById("employeeTable");
    const securityTable = document.getElementById("securityTable");
    const objectStatus = document.getElementById("object-status");
    const objectTitle = document.getElementById("object-title");

    async function getData() {
        try {
            const response = await fetch(`/api/visit_history/active_users/${CURRENT_OBJECT}`);
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            const data = await response.json();
            renderPage(data);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
    }

    function renderPage(data) {
        employeeTable.innerHTML = "";
        securityTable.innerHTML = "";
        objectTitle.innerHTML = data.object.name;
        objectStatus.innerHTML = data.object.status;
        objectStatus.classList.add(`${data.object.status === 'Открыт'? 'open' : 'close_'}`);

        data.history.forEach(entry => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.employee.full_name}</td>
                <td>${entry.entry_time}</td>
            `;

            if(entry.employee.role == "security"){
                row.addEventListener("click", () => openModalSecurity(entry, data.object.name));
                securityTable.appendChild(row);
            }
            else{                
                row.addEventListener("click", () => openModalEmployee(entry, data.object.name));
                employeeTable.appendChild(row);
            }


        });
    }

    getData();
});