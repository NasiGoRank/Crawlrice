FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget gnupg --no-install-recommends \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./Gui_Crawlrice/. .

COPY ./Cli_Crawlrice ./Cli_Crawlrice

EXPOSE 5050

CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]