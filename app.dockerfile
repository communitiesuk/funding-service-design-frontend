FROM python:3.10-slim-bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt
COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:create_app()"]
