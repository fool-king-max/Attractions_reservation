document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const alertBox = document.querySelector('.alert');

    if (alertBox) {
        setTimeout(() => {
            alertBox.style.display = 'none';
        }, 5000);  // 5秒后自动消失
    }
});
