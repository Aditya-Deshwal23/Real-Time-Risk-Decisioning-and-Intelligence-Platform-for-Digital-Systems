import importlib.util
import unittest
from pathlib import Path

DEV_PATH = Path(__file__).resolve().with_name("dev.py")
SPEC = importlib.util.spec_from_file_location("verdict_dev", DEV_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load infra/compose/dev.py")
DEV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEV)


class DevScriptTests(unittest.TestCase):
    def test_reset_refuses_without_confirmation(self) -> None:
        with self.assertRaises(SystemExit) as exit_context:
            DEV.reset(None)
        self.assertEqual(exit_context.exception.code, 2)

    def test_generated_password_placeholders_are_replaced(self) -> None:
        lines = [
            "REDIS_PASSWORD=generate-on-first-run",
            "POSTGRES_PASSWORD=",
            "VERDICT_APP_PASSWORD=local-placeholder",
            "MINIO_ROOT_PASSWORD=generate-on-first-run",
            "POSTGRES_PORT=5432",
        ]
        updated = DEV.apply_generated_passwords(lines)
        values = dict(line.split("=", 1) for line in updated if "=" in line)
        self.assertNotIn(values["REDIS_PASSWORD"], ("", "generate-on-first-run"))
        self.assertNotIn(values["POSTGRES_PASSWORD"], ("", "generate-on-first-run"))
        self.assertNotIn(
            values["MINIO_ROOT_PASSWORD"],
            ("", "generate-on-first-run"),
        )
        self.assertEqual(values["POSTGRES_PORT"], "5432")


if __name__ == "__main__":
    unittest.main()
