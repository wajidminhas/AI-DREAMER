# ─── Stage 1: Builder ────────────────────────────
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (no project code yet for layer caching)
RUN uv sync --frozen --no-install-project

# ─── Stage 2: Development ────────────────────────
FROM python:3.12-slim-bookworm AS development

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy project code
COPY . .

# Default: development server
CMD ["uvicorn", "imtiaz_mart_ai.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ─── Stage 3: Production ─────────────────────────
FROM python:3.12-slim-bookworm AS production

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Only copy source code (no tests, no docs)
COPY src/ ./src/
COPY pyproject.toml uv.lock ./

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Production: no reload, multiple workers
CMD ["uvicorn", "imtiaz_mart_ai.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]