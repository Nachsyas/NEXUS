# NEXUS Backend Service

FastAPI Modular Monolith backend for NEXUS.

## Local Setup
```bash
# Install dependencies with uv
uv sync --extra dev

# Run tests
uv run pytest

# Run linter and formatter
uv run ruff check .
uv run ruff format --check .

# Run type checker
uv run mypy app
```
