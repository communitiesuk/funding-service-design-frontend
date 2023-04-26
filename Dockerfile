FROM python:3.10-bullseye

WORKDIR /app
COPY requirements-dev.txt requirements-dev.txt
RUN python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt
COPY . .

EXPOSE 8080

CMD ["flask", "run", "--port", "8080", "--host", "0.0.0.0"]
