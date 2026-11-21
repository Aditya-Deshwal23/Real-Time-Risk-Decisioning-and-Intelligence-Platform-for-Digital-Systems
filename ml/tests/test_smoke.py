import verdict_ml


def test_smoke_import() -> None:
    assert verdict_ml.__name__ == "verdict_ml"
