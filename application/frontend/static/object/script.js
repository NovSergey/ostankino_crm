document.addEventListener("DOMContentLoaded", () => {
    const employeeTable = document.getElementById("employeeTable");
    const securityTable = document.getElementById("securityTable");
    const objectStatus = document.getElementById("object-status");

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
        objectStatus.innerHTML = data.object.status;
        objectStatus.classList.add(`${data.object.status === 'Открыт'? 'open' : 'close'}`);

        data.history.forEach(entry => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.employee.full_name}</td>
                <td>${entry.entry_time}</td>
            `;
            row.addEventListener("click", () => openModal(entry));

            if(entry.employee.role == "security")
                securityTable.appendChild(row);
            else
                employeeTable.appendChild(row);


        });
    }

    function openModal(entry) {
        document.getElementById("modal").style.display = "block";

        document.getElementById("modalEmployeeId").textContent = entry.employee.id;
        document.getElementById("modalEmployeeName").textContent = entry.employee.full_name;
        document.getElementById("modalEmployeePhone").textContent = entry.employee.phone;
        document.getElementById("modalEmployeeTime").textContent = entry.entry_time;

        document.getElementById("modalSecurityId").textContent = entry.scanned_by_user.id;
        document.getElementById("modalSecurityName").textContent = entry.scanned_by_user.full_name;
        document.getElementById("modalSecurityPhone").textContent = entry.scanned_by_user.phone;
    }

    function closeModal() {
        document.getElementById("modal").style.display = "none";
    }

    getData();
    window.closeModal = closeModal;
});