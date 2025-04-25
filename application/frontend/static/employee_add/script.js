const form = document.getElementById('employee-form');
const inputs = form.querySelectorAll('input');
const selects = form.querySelectorAll('select');
var phoneMask = document.getElementById('phone');
if(phoneMask){
    phoneMask = IMask(phoneMask, {
        mask: '+{7} (000) 000-00-00'
    });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    let data = {};
    inputs.forEach(input => {
        data[input.name] = input.value;
    });
    selects.forEach(input => data[input.name] = input.value == "" ? null : input.value);
    data['phone'] = phoneMask.unmaskedValue;
    try{
        console.log(data);
        const response = await fetch(`/api/employees/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if(!response.ok){
            if (response.status === 403){
                window.location.href = '/';
            }
            else if (response.status === 401){
                window.location.href = '/login'
            }
            alert('Не удалось добавить');
        }
        else{
            alert('Работник добавлен');
        }
    } catch(e){
        console.log("Error: ", e)
    }
    
    window.location.reload();
});
