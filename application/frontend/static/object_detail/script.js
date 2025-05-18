const editBtn = document.getElementById('edit-btn');
const saveBtn = document.getElementById('save-btn');
const cancelBtn = document.getElementById('cancel-btn');
const form = document.getElementById('employee-form');
const inputs = form.querySelectorAll('input');
const selects = form.querySelectorAll('select');

const restoreBtn = document.getElementById('restore-btn');
const deleteBtn = document.getElementById('delete-btn');


function changeActive(active){
    inputs.forEach(input => input.disabled = active);
    selects.forEach(select => select.disabled = active);
    if(active){
        editBtn.classList.remove('hidden');
        saveBtn.classList.add('hidden');
        cancelBtn.classList.add('hidden');
    }
    else{
        editBtn.classList.add('hidden');
        saveBtn.classList.remove('hidden');
        cancelBtn.classList.remove('hidden');
    }
}

editBtn.addEventListener('click', () => {
    changeActive(false);
});

cancelBtn.addEventListener('click', () => {
    changeActive(true);
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    let data = {};
    inputs.forEach(input => {data[input.name] = input.value;});
    selects.forEach(input => data[input.name] = input.value == "" ? null : input.value);
    console.log(data);
    try{
        const response = await fetch(`/api/objects/${CURRENT_OBJECT}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if(!response.ok){
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login/'
            }
            else{
                alert('Не удалось изменить');
                return;
            }
        }
    } catch(e){
        console.log("Error: ", e)
    }


    changeActive(true)

    alert('Изменения сохранены');
    
    window.location.reload();
});

if(deleteBtn){
    deleteBtn.addEventListener('click', async () => {
        try{
            const response = await fetch(`/api/objects/${CURRENT_OBJECT}/`, {
                method: 'DELETE',
            });
            if(!response.ok){
                if (response.status === 403){
                    window.location.href = '/';
                }
                else if (response.status === 401){
                    window.location.href = '/login/'
                }
            }
        } catch(e){
            console.log("Error: ", e)
        }
        alert('Объект удалён');
        window.location.reload();
    });
}

if(restoreBtn){
    restoreBtn.addEventListener('click', async () => {
        try{
            const response = await fetch(`/api/objects/restore/${CURRENT_OBJECT}/`, {
                method: 'POST',
            });
            if(!response.ok){
                if (response.status === 403){
                    window.location.href = '/';
                }
                else if (response.status === 401){
                    window.location.href = '/login/'
                }
            }
        } catch(e){
            console.log("Error: ", e)
        }
        alert('Объект восстановлен');
        window.location.reload();
    });
}
