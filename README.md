# IDOR/BAC Scanner with Web GUI

A tool for automatically scanning for IDOR (*Insecure Direct Object References*) and BAC (*Broken Access Control*) vulnerabilities. This project consists of two main parts: a flexible CLI scanner and a Flask-based web interface (GUI) to simplify scan execution and report analysis.

## 📸 Interface Showcase

### Main Dashboard


### Real-time Scan Progress Page


---
## ✨ Key Features
-   **Interactive Web Dashboard**: View scan history in a searchable and sortable table.
-   **Execute Scans from the Web**: Easily run new scans via a form in the web interface.
-   **Real-time Scan Logs**: Monitor the scanner's output process directly in the browser.
-   **Flexible CLI Scanner**: Run scans directly from the terminal with various dynamic arguments.
-   **Intelligent Crawling**: Uses Selenium to crawl modern, JavaScript-heavy websites.
-   **Automatic Role Detection**: Capable of extracting user roles (e.g., "admin", "student") from the profile page after logging in.
-   **Report Management**: View vulnerability finding details and easily clear the report history.

---
## 📂 Project Structure
```
Crawlrice/
├── Cli_Crawlrice/
│   ├── __init__.py         # Makes the directory a Python package
│   └── crawlrice.py        # Main scanner script (CLI)
├── Gui_Crawlrice/
│   ├── app.py              # Flask web application (GUI)
│   ├── reports/            # Report output folder (ignored by Git)
│   ├── static/             # CSS and JavaScript files
│   └── templates/          # HTML files
├── setup.sh
├── README.md               # This documentation
├── requirements.txt        # List of required libraries
└── setup.py                # Setup script for installing the CLI command
```

---
## ⚙️ Installation (Docker installation currently unavailable)
To run this project on your computer, follow these steps:

```yaml
Before you install it please make sure to install Google Crhome on your device.  
```

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/NasiGoRank/Crawlrice.git
    cd Crawlrice
    ```

2.  **(Optional but recommended) Create and activate a virtual environment:**
    ```bash
    # Create venv
    python -m venv venv

    # Activate venv on Windows
    .\venv\Scripts\activate

    # Activate venv on Linux/macOS
    source venv/bin/activate
    ```

3.  **Install all required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

---
## 🚀 How to Use
There are several ways to use this tool: via the Web Interface (recommended) or the Command-Line.

### 1. Using the Web Interface (GUI)
This is the easiest and most interactive method.

1.  **Run the Flask web server:**
    Open a terminal, navigate to the `Gui_Crawlrice` folder, and then run:
    ```bash
    cd Gui_Crawlrice
    python app.py
    ```

2.  **Open the Dashboard:**
    Open your browser and visit `http://127.0.0.1:5050`.

3.  **Login:**
    Use the admin credentials configured in the `app.py` file. Defaults:
    -   Username: `admin`
    -   Password: `password123`

4.  **Start a New Scan:**
    -   Click the **"🚀 New Scan"** button.
    -   Fill the form with the target URL and credentials for the attacker (low privilege) and victim (high privilege) accounts.
    -   Click **"Start Scan"**. You will be redirected to a page that displays the scan process log in real-time.
    -   After it's finished, return to the dashboard to see the new report.
---

### 3. Using the Command-Line (CLI)
You can also run the scanner script directly from the terminal. This is useful for automation. There are two ways to do this:

This method allows you to run the `crawlrice` command from **any directory** in your terminal, just like a native application.

1.  **Navigate to the project's root directory** (`Crawlrice/`) in your terminal and ensure your virtual environment is activated.

2.  **Install the package** in "editable" mode. This creates a link to your script so any changes you make are immediately active.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

3.  Once installed, you can open a **new terminal** and use the `crawlrice` command from anywhere.

**Usage Examples (Global):**
```bash
# Scan with full passwords from any directory
crawlrice -u [http://example.com](http://example.com) -au attacker -ap password -vu victim -vp password

# Display the help menu from any directory
crawlrice --help
```