

.PHONY: install dev test lint format migrate run docker-up docker-down clean

# ─── Setup ───────────────────────────────────────
install:
	uv sync

dev:
	uv sync --extra dev

# ─── Development ─────────────────────────────────
run:
	uv run uvicorn imtiaz_mart_ai.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	uv run python -m imtiaz_mart_ai.infrastructure.db migrate

# ─── Testing ─────────────────────────────────────
test:
	uv run pytest

test-cov:
	uv run pytest --cov-report=html

# ─── Code Quality ────────────────────────────────
lint:
	uv run ruff check src tests
	uv run mypy src

format:
	uv run ruff check --fix src tests
	uv run ruff format src tests

# ─── Docker ──────────────────────────────────────
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# ─── Cleanup ─────────────────────────────────────
clean:
	rm -rf .venv uv.lock .pytest_cache .mypy_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete