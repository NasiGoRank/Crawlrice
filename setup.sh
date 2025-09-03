#!/bin/bash
set -e

echo "🚀 Memulai setup global untuk Crawlrice..."
echo "PERINGATAN: Skrip ini akan meminta password sudo dan menginstal paket secara global."

echo "--- Memeriksa Python 3 dan Pip3..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "❌ Error: python3 atau pip3 tidak ditemukan."
    read -p "   Apakah Anda ingin mencoba menginstalnya sekarang? (y/n) " -n 1 -r
    echo "" 

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v apt-get &> /dev/null; then
            echo "   -> Menginstall Python 3, Pip, dan Venv menggunakan apt-get..."
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv 
            echo "   ✅ Python 3 berhasil diinstal."
        else
            echo "   ❌ Instalasi otomatis tidak didukung di OS ini (hanya Debian/Ubuntu)."
            echo "      Silakan install Python 3.7+ secara manual lalu jalankan kembali skrip ini."
            exit 1
        fi
    else
        echo "   Instalasi dibatalkan oleh pengguna."
        exit 1
    fi
else
    echo "✅ Python 3 dan Pip3 sudah ditemukan."
fi

echo "--- Menginstall dependensi dari requirements.txt..."
sudo pip3 install -r requirements.txt
echo "✅ Dependensi berhasil diinstal."

echo "--- Membuat 'crawlrice' menjadi perintah global..."

SCRIPT_PATH=$(realpath "Main/Cli_Crawlrice/crawlrice.py")
chmod +x "$SCRIPT_PATH"

if [ -f "/usr/local/bin/crawlrice" ]; then
    echo "  > Menghapus link lama..."
    sudo rm /usr/local/bin/crawlrice
fi
sudo ln -s "$SCRIPT_PATH" /usr/local/bin/crawlrice
echo "✅ Perintah 'crawlrice' berhasil dibuat."

echo ""
echo "--- ✨ Setup Selesai! ---"
echo "Anda sekarang bisa membuka terminal baru dan menjalankan perintah 'crawlrice' dari direktori mana pun."
echo "Contoh: crawlrice --help"
echo "--------------------------"