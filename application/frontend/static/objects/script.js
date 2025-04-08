document.addEventListener("DOMContentLoaded", () => {
    const dataBody = document.getElementById("objects-container");

    async function getData() {
        try {
            const response = await fetch("/api/objects/");
            const data = await response.json();
            renderObjects(data);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
    }

    function renderObjects(data) {
        dataBody.innerHTML = "";
        data.forEach(entry => {
            let row = document.createElement("div");
            row.classList.add("object-card")
            row.onclick = function() {
              location.href = `/objects/${entry.id}`;
            };
            row.innerHTML = `
                <h3>${entry.name}</h3>
                <p class="status ${entry.status === 'Открыт'? 'open' : 'close'}">${entry.status}</p>
            `;
            row.addEventListener("click", () => openModal(entry));
            dataBody.appendChild(row);
        });
    }

    getData();
});