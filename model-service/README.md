# model-service/

**Responsibility:** FastAPI inference service and model artifact loading.

**Must never contain:** Tenant state, direct tenant-table access, or training pipelines.

**First implementation phase:** Phase 11 — Model serving and reliable inference.

## uv commands

Run all commands from the repository root:

- Sync: `uv sync --locked`
- Lint: `cd model-service && uv run ruff check .`
- Format check: `cd model-service && uv run ruff format --check .`
- Type check: `cd model-service && uv run mypy src`
- Test: `cd model-service && uv run pytest -m "not slow"`
