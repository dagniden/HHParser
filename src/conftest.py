import pytest

from src.models import Vacancy

@pytest.fixture
def test_vacancy() -> Vacancy:
    return Vacancy(200,
                   300,
                   "Тестировщик",
                   "Тестировать приложения лопатой")
