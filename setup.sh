set -e

echo "🚀 Memulai setup global untuk Crawlrice..."
echo "Skrip ini akan meminta password sudo untuk instalasi global."

echo "--- [1/3] Memeriksa Python 3 dan Pip3..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "❌ Error: python3 atau pip3 tidak ditemukan. Mohon install terlebih dahulu."
    exit 1
fi
echo "✅ Python 3 dan Pip3 ditemukan."

echo "--- [2/3] Menginstall dependensi dari requirements.txt..."
sudo pip3 install -r requirements.txt
echo "✅ Dependensi berhasil diinstal."

echo "--- [3/3] Membuat 'crawlrice' menjadi perintah global..."

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