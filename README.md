2# IDOR/BAC Scanner with Web GUI

Sebuah tool untuk melakukan pemindaian kerentanan IDOR (*Insecure Direct Object References*) dan BAC (*Broken Access Control*) secara otomatis. Proyek ini terdiri dari dua bagian utama: sebuah *scanner* CLI yang fleksibel dan antarmuka web (GUI) berbasis Flask untuk mempermudah eksekusi *scan* dan analisis laporan.

## 📸 Tampilan Antarmuka

### Dashboard Utama


### Halaman Proses Scan Real-time


---
## ✨ Fitur Utama
-   **Dashboard Web Interaktif**: Melihat riwayat laporan dalam bentuk tabel yang dapat dicari dan diurutkan.
-   **Eksekusi Scan dari Web**: Menjalankan pemindaian baru dengan mudah melalui form di antarmuka web.
-   **Log Scan Real-time**: Memantau output dari proses *scanner* secara langsung di browser.
-   **Scanner CLI Fleksibel**: Menjalankan pemindaian langsung dari terminal dengan berbagai argumen dinamis.
-   ***Crawling* Cerdas**: Menggunakan Selenium untuk menjelajahi website modern yang sangat bergantung pada JavaScript.
-   **Deteksi Peran Otomatis**: Mampu mengekstrak peran pengguna (misal: "admin", "student") dari halaman profil setelah login.
-   **Manajemen Laporan**: Melihat detail temuan kerentanan dan membersihkan riwayat laporan dengan mudah.

---
## 📂 Struktur Proyek
```
Crawlrice/
├── Cli_Crawlrice/
│   └── crawlrice.py        # Skrip utama scanner (CLI)
├── Gui_Crawlrice/
│   ├── app.py              # Aplikasi web Flask (GUI)
│   ├── reports/            # Folder output laporan (diabaikan oleh Git)
│   ├── static/             # File CSS dan JavaScript
│   └── templates/          # File HTML
├── README.md               # Dokumentasi ini
└── requirements.txt        # Daftar library yang dibutuhkan
```

---
## ⚙️ Instalasi
Untuk menjalankan proyek ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/NasiGoRank/Crawlrice.git](https://github.com/NasiGoRank/Crawlrice.git)
    cd Crawlrice
    ```

2.  **(Opsional) Buat dan aktifkan *virtual environment*:**
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan venv di Windows
    .\venv\Scripts\activate

    # Mengaktifkan venv di Linux/macOS
    source venv/bin/activate
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

---
## 🚀 Cara Penggunaan
Ada beberapa cara untuk menggunakan tool ini: melalui Antarmuka Web (rekomendasi) atau melalui Command-Line.

### 1. Menggunakan Antarmuka Web (GUI)
Ini adalah cara termudah dan paling interaktif.

1.  **Jalankan server web Flask:**
    Buka terminal, masuk ke folder `Gui_Crawlrice`, lalu jalankan:
    ```bash
    cd Gui_Crawlrice
    python app.py
    ```

2.  **Buka Dashboard:**
    Buka browser Anda dan kunjungi alamat `http://127.0.0.1:5050`.

3.  **Login:**
    Gunakan kredensial admin yang sudah diatur di dalam file `app.py`. Default:
    -   Username: `admin`
    -   Password: `password123`

4.  **Mulai Scan Baru:**
    -   Klik tombol **"🚀 Scan Baru"**.
    -   Isi form dengan URL target dan kredensial untuk akun *attacker* (hak akses rendah) dan *victim* (hak akses tinggi).
    -   Klik **"Mulai Scan"**. Anda akan diarahkan ke halaman yang menampilkan log proses scan secara *real-time*.
    -   Setelah selesai, kembali ke dashboard untuk melihat laporan baru.

### 2. 🐳 Menjalankan dengan Docker (Direkomendasikan)
Ini adalah cara termudah untuk menjalankan aplikasi web. Anda hanya perlu Docker dan Docker Compose terinstal.

#### Opsi 1: Menggunakan Docker Compose (Satu Perintah)
1.  Pastikan Anda memiliki file `Dockerfile` dan `docker-compose.yml` di dalam folder `Gui_Crawlrice`.
2.  Buka terminal di dalam folder `Gui_Crawlrice`, lalu jalankan:
    ```bash
    docker-compose up -d
    ```
3.  Aplikasi web sekarang berjalan di `http://127.0.0.1:5001`.
4.  Untuk menghentikan aplikasi, jalankan:
    ```bash
    docker-compose down
    ```

#### Opsi 2: Menggunakan Docker Build & Run (Manual)
1.  Pastikan Anda memiliki `Dockerfile` di dalam folder `Gui_Crawlrice`.
2.  Buka terminal di dalam folder `Gui_Crawlrice` dan build image-nya:
    ```bash
    docker build -t scanner-gui .
    ```
3.  Setelah build selesai, jalankan container dengan perintah berikut:
    
    **Untuk Windows (CMD/PowerShell):**
    ```bash
    docker run -p 5001:5001 -v "%cd%/reports:/app/reports" --name scanner-container scanner-gui
    ```
    **Untuk Linux/macOS:**
    ```bash
    docker run -p 5001:5001 -v "$(pwd)/reports:/app/reports" --name scanner-container scanner-gui
    ```
4.  Aplikasi web sekarang berjalan di `http://127.0.0.1:5001`.

---
## 🚀 Cara Menjalankan Scanner
Setelah aplikasi web berjalan (baik via Docker maupun manual), Anda bisa memulai scan:

1.  Buka `http://127.0.0.1:5001` dan login (default: `admin`/`password123`).
2.  Klik tombol **"🚀 Scan Baru"**.
3.  Isi form dengan URL target dan kredensial, lalu klik **"Mulai Scan"**.
4.  Anda akan diarahkan ke halaman log, dan setelah selesai, laporan akan muncul di dashboard.

### 2. Menggunakan Command-Line (CLI)
Anda juga bisa menjalankan skrip scanner secara langsung dari terminal. Ini berguna untuk otomatisasi.

1.  Buka terminal dan masuk ke folder `Cli_Crawlrice`.
2.  Jalankan skrip dengan argumen yang diperlukan.

**Contoh Penggunaan:**
```bash
# Scan dengan password lengkap
python crawlrice.py -u [http://example.com](http://example.com) -au attacker -ap password -vu victim -vp password

# Scan jika akun attacker tidak menggunakan password
python crawlrice.py -u [http://target.com](http://target.com) -au attacker -vu admin -vp adminpass

# Menampilkan menu bantuan
python crawlrice.py --help
```

---
## 🔧 Konfigurasi
Beberapa bagian dari skrip mungkin perlu Anda sesuaikan:

-   **Kredensial Admin Web**: Untuk mengubah username dan password login ke dashboard, edit dictionary `ADMIN_USER` di file `Gui_Crawlrice/app.py`.
-   **Selector Role User**: Jika *scanner* gagal mendeteksi peran user (menampilkan "Unknown"), Anda mungkin perlu menyesuaikan *CSS Selector* di dalam fungsi `get_user_role` pada file `Cli_Crawlrice/crawlrice.py` agar cocok dengan struktur HTML website target Anda.