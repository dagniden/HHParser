import pytest

from src.models import Vacancy, VacancyList


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


@pytest.fixture
def vacancy_list() -> VacancyList:
    v1 = Vacancy(1, "", "Vacancy1", "", "Comp", "Moscow", 120000, None)
    v2 = Vacancy(2, "", "Vacancy2", "", "Comp", "Moscow", 120000, None)
    v3 = Vacancy(3, "", "Vacancy3", "", "Comp", "Moscow", 100000, 150000)

    return VacancyList([v1, v2, v3])
