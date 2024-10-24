FROM python:3.10-bullseye
ARG USE_DEV_REQUIREMENTS

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml .
RUN uv sync
COPY . .

EXPOSE 8080

CMD ["uv", "run", "flask", "run", "--port", "8080", "--host", "0.0.0.0"]
