import os
from typing import Any, Generator

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


@pytest.fixture
def test_filename() -> Generator[str, Any, None]:
    """Фикстура для создания временного тестового файла"""
    filename = "test_vacancies.json"
    yield filename
    # Cleanup: удаляем файл после теста
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Фикстура для создания тестовой вакансии"""
    return Vacancy(
        vacancy_id="12345",
        vacancy_url="https://test.com/vacancy/12345",
        title="Python Developer",
        description="Разработка на Python",
        company_name="Test Company",
        area_name="Москва",
        salary_from=100000,
        salary_to=150000,
    )


@pytest.fixture
def another_vacancy() -> Vacancy:
    """Фикстура для создания второй тестовой вакансии"""
    return Vacancy(
        vacancy_id="67890",
        vacancy_url="https://test.com/vacancy/67890",
        title="Java Developer",
        description="Разработка на Java",
        company_name="Another Company",
        area_name="Санкт-Петербург",
        salary_from=120000,
        salary_to=180000,
    )
