import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _imports(source: Path) -> set[str]:
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_python_projects_do_not_import_each_other() -> None:
    forbidden = {
        "ml": "verdict_model_service",
        "model-service": "verdict_ml",
    }

    violations: list[str] = []
    for project, forbidden_package in forbidden.items():
        source_root = ROOT / project / "src"
        for source in source_root.rglob("*.py"):
            for imported in _imports(source):
                if imported == forbidden_package or imported.startswith(
                    f"{forbidden_package}.",
                ):
                    violations.append(f"{source}: imports {imported}")

    assert not violations, "\n".join(violations)
