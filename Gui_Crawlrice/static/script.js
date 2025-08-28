document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement; // Target elemen <html>

    // Fungsi untuk menerapkan tema berdasarkan preferensi
    const applyTheme = () => {
        const theme = localStorage.getItem('theme') || 'dark'; // Default ke dark
        htmlElement.setAttribute('data-bs-theme', theme);
        darkModeToggle.textContent = theme === 'dark' ? '🌙' : '☀️';
    };

    // Fungsi untuk mengubah tema
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

    // Terapkan tema saat halaman dimuat
    applyTheme();
});