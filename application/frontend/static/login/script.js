function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.password-toggle i');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

document.getElementById('login-form').addEventListener('submit', async function(event) {

    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
        const response = await fetch('/api/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Успешный вход:', result);
            window.location.href = '/';
        } else {
            console.error('Ошибка входа:', response.statusText);
            alert('Ошибка входа. Проверьте логин и пароль.');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе.');
    }
});