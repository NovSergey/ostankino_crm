const form = document.getElementById('employee-form');
const inputs = form.querySelectorAll('input');


form.addEventListener('submit', async (e) => {
    e.preventDefault();
    let data = {};
    inputs.forEach(input => {
        data[input.name] = input.value;
    });
    try{
        const response = await fetch(`/api/objects/`, {
            method: 'POST',
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
            alert('Не удалось добавить');
        }
        else{
            alert('Объект добавлен');
        }
    } catch(e){
        console.log("Error: ", e)
    }
    
    window.location.reload();
});
