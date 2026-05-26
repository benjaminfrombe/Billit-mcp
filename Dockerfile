FROM python:3.12-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN pip install --no-cache-dir uv==0.7.12

COPY README.md pyproject.toml uv.lock ./
COPY billit ./billit
COPY src ./src
RUN uv sync --locked --no-dev

COPY . .

CMD ["python", "-m", "billit_mcp"]
