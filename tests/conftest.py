import pytest

from src.main import create_app


@pytest.fixture
def app():
    app, _ = create_app()
    return app
