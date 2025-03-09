FROM python:3.12-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY src /app/src
COPY uv.lock pyproject.toml /app/

WORKDIR /app

RUN apt-get update && \
    uv sync --frozen && \
    rm -rf /var/lib/apt/lists/*


ENV LOGURU_LEVEL="INFO"
CMD [ \
    "uv", "run", \
    "python", "src/main.py" \
]