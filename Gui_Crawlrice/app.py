import os
import json
import sys
import subprocess
import threading
import queue
from flask import Flask, render_template, abort, request, redirect, url_for, flash, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)

@app.template_filter('datetimeformat')
def format_datetime(value):
    """Filter untuk mengubah format tanggal ISO menjadi lebih mudah dibaca."""
    if not isinstance(value, str):
        return value
    try:
        dt_object = datetime.fromisoformat(value)
        return dt_object.strftime("%d %b %Y, %H:%M:%S")
    except (ValueError, TypeError):
        return value

app.config['SECRET_KEY'] = 'ganti-ini-dengan-string-acak-yang-panjang'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, 'reports')

if os.path.exists('/.dockerenv'):
    SCANNER_SCRIPT_PATH = '/app/Cli_Crawlrice/crawlrice.py'
else:
    SCANNER_SCRIPT_PATH = os.path.join(SCRIPT_DIR, '..', 'Cli_Crawlrice', 'crawlrice.py')
log_queue = queue.Queue()

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
ADMIN_USER = {'id': '1', 'username': 'admin', 'password': 'password123'}

@login_manager.user_loader
def load_user(user_id):
    if user_id == ADMIN_USER['id']:
        return User(id=ADMIN_USER['id'], username=ADMIN_USER['username'])
    return None

def run_scan_in_thread(command):
    """Menjalankan scan dan memasukkan output ke queue secara real-time."""
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   text=True, encoding='utf-8', errors='replace', 
                                   bufsize=1, env=env)
        
        for line in iter(process.stdout.readline, ''):
            log_queue.put(line.strip())
        
        process.stdout.close()
        process.wait()

    except Exception as e:
        log_queue.put(f"❌ Terjadi error saat menjalankan scan: {e}")
    finally:
        log_queue.put('---SCAN-END---')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('index'))
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        if username == ADMIN_USER['username'] and password == ADMIN_USER['password']:
            login_user(User(id=ADMIN_USER['id'], username=ADMIN_USER['username']))
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Halaman utama yang menampilkan daftar semua laporan."""
    reports_data = []
    try:
        files = os.listdir(REPORTS_DIR)
        report_files = [f for f in files if f.endswith('.json')]

        for filename in report_files:
            file_path = os.path.join(REPORTS_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    summary = content.get('summary', {})
                    reports_data.append({
                        'filename': filename,
                        'domain': content.get('base_url', 'N/A'),
                        'vuln_count': summary.get('vulnerabilities_found', 0),
                        'scan_date': content.get('tested_at', 'N/A'),
                    })
            except Exception as e:
                print(f"Gagal membaca file {filename}: {e}")
                reports_data.append({
                    'filename': filename, 'domain': 'Error', 
                    'vuln_count': 'N/A', 'scan_date': 'Error Reading File'
                })

        reports_data.sort(key=lambda x: x.get('scan_date', '0'), reverse=True)

    except FileNotFoundError:
        print(f"Direktori laporan tidak ditemukan di {REPORTS_DIR}")

    return render_template('index.html', reports=reports_data)

@app.route('/report/<filename>')
@login_required
def view_report(filename):
    """Halaman untuk menampilkan detail dari satu file laporan."""
    file_path = os.path.join(REPORTS_DIR, filename)

    if not os.path.exists(file_path):
        abort(404) 

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Gagal memuat file laporan {filename}: {e}")
        abort(500) 

    return render_template('report.html', report=report_data, filename=filename)


@app.route('/scan')
@login_required
def scan():
    """Menampilkan halaman form scan."""
    return render_template('scan.html')

@app.route('/start_scan', methods=['POST'])
@login_required
def start_scan():
    """Menerima data dari form dan memulai scan di background."""
    url = request.form.get('url')
    attacker_user = request.form.get('attacker_user')
    attacker_pass = request.form.get('attacker_pass')
    victim_user = request.form.get('victim_user')
    victim_pass = request.form.get('victim_pass')
    
    command = [
        sys.executable, SCANNER_SCRIPT_PATH, '--url', url,
        '--attacker-user', attacker_user, '--victim-user', victim_user
    ]
    if attacker_pass: command.extend(['--attacker-pass', attacker_pass])
    if victim_pass: command.extend(['--victim-pass', victim_pass])

    scan_thread = threading.Thread(target=run_scan_in_thread, args=(command,))
    scan_thread.start()

    return redirect(url_for('scan_progress'))

@app.route('/scan_progress')
@login_required
def scan_progress():
    """Halaman yang akan menampilkan log secara real-time."""
    return render_template('scan_progress.html')

@app.route('/stream_scan_logs')
def stream_scan_logs():
    """Rute ini berfungsi sebagai sumber SSE (Server-Sent Events)."""
    def generate():
        while True:
            message = log_queue.get()
            yield f"data: {message}\n\n"
            if message == '---SCAN-END---':
                break
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/clear_reports', methods=['POST'])
@login_required
def clear_reports():
    """Menghapus semua file laporan dari direktori reports."""
    files_deleted = 0
    try:
        for filename in os.listdir(REPORTS_DIR):
            file_path = os.path.join(REPORTS_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                files_deleted += 1
        
        flash(f'Berhasil menghapus {files_deleted} file laporan.', 'success')
    except Exception as e:
        print(f"Error saat menghapus riwayat: {e}")
        flash('Terjadi kesalahan saat mencoba menghapus riwayat laporan.', 'danger')
        
    return redirect(url_for('index'))

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

if __name__ == '__main__':
    app.run(debug=True, port=5050, threaded=True)