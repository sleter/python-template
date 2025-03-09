FROM python:3.12-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

RUN apt-get update && \
    uv sync --frozen && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8080
ENV LOGURU_LEVEL="INFO"
CMD [ \
    "uv", "run", \
    "python", "src/main.py" \
]