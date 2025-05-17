const editBtn = document.getElementById('edit-btn');
const saveBtn = document.getElementById('save-btn');
const cancelBtn = document.getElementById('cancel-btn');
const form = document.getElementById('employee-form');
const inputs = form.querySelectorAll('input');
const selects = form.querySelectorAll('select');

const restoreBtn = document.getElementById('restore-btn');
const deleteBtn = document.getElementById('delete-btn');
var phoneMask = document.getElementById('phone');
if(phoneMask){
    phoneMask = IMask(phoneMask, {
        mask: '+{7} (000) 000-00-00'
    });
}

function changeActive(active){
    inputs.forEach(input => input.disabled = active);
    selects.forEach(select => select.disabled = active);
    if(active){
        editBtn.classList.remove('hidden');
        deleteBtn.classList.remove('hidden');
        saveBtn.classList.add('hidden');
        cancelBtn.classList.add('hidden');
    }
    else{
        editBtn.classList.add('hidden');
        deleteBtn.classList.add('hidden');
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
    let id = null;
    inputs.forEach(input => {
        if(input.name != "id")
            data[input.name] = input.value;
        else
            id = input.value;
    });
    selects.forEach(input => data[input.name] = input.value == "" ? null : input.value);
    data['phone'] = phoneMask.unmaskedValue;
    try{
        const response = await fetch(`/api/employees/${id}/`, {
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
        let id = document.getElementById("id").value;
        try{
            const response = await fetch(`/api/employees/${id}/`, {
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
        alert('Работник удалён');
        window.location.reload();
    });
}

if(restoreBtn){
    restoreBtn.addEventListener('click', async () => {
        let id = document.getElementById("id").value;
        try{
            const response = await fetch(`/api/employees/restore/${id}/`, {
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
        alert('Работник восстановлен');
        window.location.reload();
    });
}
