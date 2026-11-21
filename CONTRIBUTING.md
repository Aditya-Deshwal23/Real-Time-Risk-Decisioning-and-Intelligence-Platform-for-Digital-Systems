# Contributing

The project owner is the sole developer and decision-maker. Contributions and assistant-prepared changes must stay within the approved specification; the owner reviews changes and decides whether to commit, push or merge them.

Before working, read the six files in [`docs/context/`](docs/context/), especially [`ai-workflow-rules.md`](docs/context/ai-workflow-rules.md) and its section 12 standing rules. Follow the architecture and code standards there, do not invent paths or requirements, and report unverified checks honestly. The [documentation index](docs/README.md) shows where project records belong.

## Repository hooks

The repository uses pre-commit for file hygiene, secret scanning, the four repository scripts, and ecosystem format checks. Sync the workspace and install the hook before committing:

```text
uv sync --locked
uv run pre-commit install
uv run pre-commit run --all-files
```

The individual repository checks are:

```text
python3 tools/ci/check_docs.py
python3 tools/ci/check_size.py
python3 tools/ci/check_notebooks.py
python3 tools/ci/check_context_refs.py
```

## GitHub Actions

Pull requests run change-aware workflows for JVM, Python, console, and docs/tools areas. Skipped areas do not leave required checks pending. The exact branch-protection status checks are:

- `JVM / status`
- `Python / status`
- `Console / status`
- `Docs and tools / status`
- `CI / aggregate status`
