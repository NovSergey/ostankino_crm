// Функции для меню
function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');

    document.querySelectorAll('.dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
    });
}

document.querySelectorAll('.dropdown-toggle').forEach(item => {
    item.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024) {
            e.preventDefault();
            const parent = item.parentElement;
            const isActive = parent.classList.contains('active');

            // Закрываем все остальные подменю
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                if (dropdown !== parent) {
                    dropdown.classList.remove('active');
                }
            });

            // Переключаем состояние текущего подменю
            parent.classList.toggle('active', !isActive);
        }
    });
});

// Закрытие меню при клике вне области
document.addEventListener('click', (e) => {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');

    if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Закрытие меню при изменении размера окна
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        const navMenu = document.querySelector('.nav-menu');
        const hamburger = document.querySelector('.hamburger');
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});