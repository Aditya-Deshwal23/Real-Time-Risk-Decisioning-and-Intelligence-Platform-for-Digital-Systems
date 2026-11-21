import verdict_model_service


def test_smoke_import() -> None:
    assert verdict_model_service.__name__ == "verdict_model_service"
