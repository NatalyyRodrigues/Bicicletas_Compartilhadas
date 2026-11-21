"""Testes iniciais. Na E2: testes das regras em app/models (sem depender de HTTP)."""


def test_app_fastapi_configurada():
    from main import app

    assert app.title == "Bicicletas Compartilhadas API"
    assert app.version == "1.0"