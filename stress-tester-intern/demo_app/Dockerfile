FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV HOST=0.0.0.0 PORT=8000
CMD ["sh", "-c", "gunicorn -w ${APP_WORKERS:-2} --threads ${APP_THREADS:-4} -b 0.0.0.0:8000 app:app"]
