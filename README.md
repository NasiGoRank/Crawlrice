# IDOR/BAC Scanner with Web GUI

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A tool for automatically scanning for IDOR (*Insecure Direct Object References*) and BAC (*Broken Access Control*) vulnerabilities. This project consists of two main parts: a flexible CLI scanner and a Flask-based web interface (GUI) to simplify scan execution and report analysis.

## 📸 Interface Showcase

### Main Dashboard

*A searchable and sortable dashboard displaying all scan reports.*

### Real-time Scan Progress Page

*A terminal-like view showing live output from the scanner as it runs.*

---

## ✨ Key Features

* **Interactive Web Dashboard**: View scan history in a searchable and sortable table.
* **Execute Scans from the Web**: Easily run new scans via a form in the web interface.
* **Real-time Scan Logs**: Monitor the scanner's output process directly in the browser.
* **Flexible CLI Scanner**: Run scans directly from the terminal with various dynamic arguments.
* **Intelligent Crawling**: Uses Selenium to crawl modern, JavaScript-heavy websites.
* **Report Management**: View vulnerability finding details and easily clear the report history.

---

## 🛠️ Technology Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, Bootstrap 5, JavaScript, DataTables.js
* **Scanner**: Selenium, BeautifulSoup4, Requests
* **Deployment**: Docker, Gunicorn

---

## 📂 Project Structure
```
Crawlrice/
├── Main                         # Main folder
│    ├── Cli_Crawlrice/
│    │   ├── __init__.py
│    │   └── crawlrice.py        # Main scanner script (CLI)
│    └── Gui_Crawlrice/
│        ├── app.py              # Flask web application (GUI)
│        ├── reports/            # Report output folder (ignored by Git)
│        ├── static/             # CSS and JavaScript files
│        └── templates/          # HTML files
├── Dockerfile                   # Instructions to build the Docker image
├── docker-compose.yml           # Easy one-command Docker startup
├── setup.py                     # Setup script for installing the CLI
├── setup.sh                     # Setup script for Linux/macOS
├── setup.bat                    # Setup script for Windows (Currently not available)
├── requirements.txt             # List of required Python libraries
└── README.md                    # This documentation
```

---

## ⚙️ Installation Guide
Follow this guide to install the project manually from your command line.

**Prerequisites:**

* [Git](https://git-scm.com/)
* [Python](https://www.python.org/) (version 3.7+ is recommended)
* [Google Chrome](https://www.google.com/chrome/) (or Chromium)
* ChromeDriver (matching your Chrome version)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/NasiGoRank/Crawlrice.git
cd Crawlrice
```

### Step 2: Install Google Chrome & ChromeDriver

Since the scanner relies on Selenium, you need a working browser and driver.

**Install Google Chrome:**

```bash
sudo apt update
sudo apt install wget unzip -y

#Get your latest version of Google Chrome
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Verify installation
google-chrome --version
```

**Install ChromeDriver (must match your Chrome version):**

```bash
# Remove old versions
sudo rm -f /usr/local/bin/chromedriver

# Example: Chrome version 139.0.7258.154 (Make sure it's the same version with the Google Chrome)
sudo wget https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.154/linux64/chromedriver-linux64.zip
sudo unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Verify installation
chromedriver --version
```

### Step 3: Make the Scanner a Global Command

Run the setup script for your operating system. This will make the `crawlrice` command available from any directory in your terminal.

**For Windows (Currently not available):**

```bash
.\setup.bat
```

*(You may need to run as Administrator. Open a new terminal after setup completes.)*

**For Linux/macOS:**

```bash
chmod +x setup.sh
sudo ./setup.sh
```

*(Open a new terminal after setup completes.)*

---
## 🚀 Usage Guide

This project can be run in several ways depending on your needs.

### 🐳 Method 1: Running the Web GUI with Docker (Recommended)

This is the easiest and most reliable way to get the web application running.

**Prerequisites:**

* [Docker](https://www.docker.com/products/docker-desktop/) & Docker Compose

**Instructions:**

1. Clone this repository.
2. Navigate to the project's root directory (`Crawlrice/`) in your terminal.
3. Run the application using Docker Compose:

   ```bash
   docker-compose up -d --build
   ```
4. The web application is now running at **`http://127.0.0.1:5050`**.
5. To stop the application, run: `docker-compose down`.

### 🔧 Post-Setup Configuration (Optional but Recommended)

For smoother integration between CLI and Docker (so reports sync correctly):

1. Give your user ownership of the Crawlrice project folder:

   ```bash
   sudo chown -R Your Username:Your Username Crawlrice
   ```

2. Add Crawlrice project root as an environment variable:

   ```bash
   nano ~/.bashrc
   ```

   Add this line at the bottom:

   ```bash
   export CRAWLRICE_PROJECT_ROOT="Your path to Crawlrice"
   ```

3. Reload your shell configuration:

   ```bash
   source ~/.bashrc
   ```

Now the project root is globally accessible via `$CRAWLRICE_PROJECT_ROOT`, which makes volume mounts and CLI report syncing easier.

Now you can access the website using this credetial.
| Username | Password   |
| -------- | ---------- |
| admin    | password123|
---

### 👨‍💻 Method 2: CLI Usage (Manual)

You can run the `crawlrice` command from any directory. For reports to sync with the Docker GUI, it's best to run the command from the project's root folder (`Crawlrice/`).

**Usage Examples:**

```bash
# Scan with full passwords
crawlrice -u http://example.com -au attacker -ap password -vu victim -vp password

# Display the help menu
crawlrice --help
```

---

## 🔬 Testing Selenium Setup

(Optional, but recommended before first use)

Create a file `test_selenium.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
print("Page Title:", driver.title)

driver.quit()
```

Run:

```bash
python3 test_selenium.py
```

Expected output:

```
Page Title: Google
```

This confirms that Chrome + ChromeDriver are working correctly.
