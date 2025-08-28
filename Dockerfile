FROM python:3.11-slim

WORKDIR /app

COPY ./Gui_Crawlrice/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./Gui_Crawlrice/. .

COPY ./Cli_Crawlrice ./Cli_Crawlrice

EXPOSE 5050

CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]