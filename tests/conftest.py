import pytest

from src.models import Vacancy


@pytest.fixture
def vacancy() -> Vacancy:
    return Vacancy(
        "124937232",
        "https://api.hh.ru/vacancies/124937232?host=hh.ru",
        "Менеджер",
        "Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.",
        "Е-Клиник",
        "Москва",
        125000,
        150000,
    )
