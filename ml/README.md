# ml/

**Responsibility:** Offline dataset preparation, feature processing, training, evaluation and drift reports.

**Must never contain:** Online services or imports from deployable service source trees.

**First implementation phase:** Phase 9 — Python data engineering and ML pipelines.

## Notebook policy

Notebooks live only in `ml/notebooks/`, are exploratory, and are committed without outputs. They must not be the source of reported results.

## uv commands

Run all commands from the repository root:

- Sync: `uv sync --locked`
- Lint: `cd ml && uv run ruff check .`
- Format check: `cd ml && uv run ruff format --check .`
- Type check: `cd ml && uv run mypy src`
- Test: `cd ml && uv run pytest -m "not slow"`
