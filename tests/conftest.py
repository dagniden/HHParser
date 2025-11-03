
from typing import Any

import pytest

from src.models import Vacancy, VacancyList


@pytest.fixture
def vacancy() -> Vacancy:
    return Vacancy(
        124937232,
        "https://api.hh.ru/vacancies/124937232?host=hh.ru",
        "Менеджер",
        "Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.",
        100500,
        "Москва",
        125000,
        150000,
    )


@pytest.fixture
def vacancy_list() -> VacancyList:
    v1 = Vacancy(1, "", "Vacancy1", "", 100500, "Moscow", 120000, None)
    v2 = Vacancy(2, "", "Vacancy2", "", 100500, "Moscow", 120000, None)
    v3 = Vacancy(3, "", "Vacancy3", "", 100500, "Moscow", 100000, 150000)

    return VacancyList([v1, v2, v3])


@pytest.fixture
def test_filename(tmp_path: Any) -> str:
    """Фикстура для создания временного тестового файла"""
    # Используем tmp_path от pytest для создания уникального файла
    filename = str(tmp_path / "test_vacancies.json")
    return filename


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Фикстура для создания тестовой вакансии"""
    return Vacancy(
        vacancy_id=12345,
        vacancy_url="https://test.com/vacancy/12345",
        title="Python Developer",
        description="Разработка на Python",
        company_id=100500,
        area_name="Москва",
        salary_from=100000,
        salary_to=150000,
    )


@pytest.fixture
def another_vacancy() -> Vacancy:
    """Фикстура для создания второй тестовой вакансии"""
    return Vacancy(
        vacancy_id=67890,
        vacancy_url="https://test.com/vacancy/67890",
        title="Java Developer",
        description="Разработка на Java",
        company_id=100501,
        area_name="Санкт-Петербург",
        salary_from=120000,
        salary_to=180000,
    )
