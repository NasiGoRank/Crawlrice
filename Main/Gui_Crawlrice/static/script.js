document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement; 

    const applyTheme = () => {
        const theme = localStorage.getItem('theme') || 'dark'; 
        htmlElement.setAttribute('data-bs-theme', theme);
        darkModeToggle.textContent = theme === 'dark' ? '🌙' : '☀️';
    };

    const toggleTheme = () => {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        darkModeToggle.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    };

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleTheme);
    }

    applyTheme();
});