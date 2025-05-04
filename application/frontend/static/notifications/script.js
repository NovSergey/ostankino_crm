function markAsRead(button) {
    const notification = button.closest('.notification-item');
    notification.classList.remove('unread');
    button.remove();
}

function toggleMenu() {
    document.querySelector('.nav-menu').classList.toggle('active');
    document.querySelector('.hamburger').classList.toggle('active');
}

document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = toggle.parentElement;
        parent.classList.toggle('active');
    });
});