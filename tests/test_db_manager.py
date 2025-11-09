"""Тесты для DBManager"""

from unittest.mock import MagicMock, patch

import pytest

from src.db_manager import DBManager
from src.models import Vacancy, VacancyList


@pytest.fixture
def db_manager_mock() -> DBManager:
    """Фикстура для создания DBManager с mock DBStorage"""
    with patch("src.db_manager.DBStorage") as mock_storage:
        # Mock initialize_database
        mock_storage.initialize_database.return_value = None

        # Create DBManager instance
        db_manager = DBManager()

        # Mock db attribute
        db_manager.db = MagicMock()

        yield db_manager


def test_get_companies_and_vacancies_count(db_manager_mock: DBManager) -> None:
    """Тест получения списка компаний и количества вакансий"""
    # Arrange
    expected = [
        {"company_name": "VK", "count": 10},
        {"company_name": "Яндекс", "count": 5},
    ]
    db_manager_mock.db.fetch_query.return_value = expected

    # Act
    result = db_manager_mock.get_companies_and_vacancies_count()

    # Assert
    assert result == expected
    db_manager_mock.db.fetch_query.assert_called_once()


def test_get_all_vacancies(db_manager_mock: DBManager) -> None:
    """Тест получения всех вакансий"""
    # Arrange
    expected = [
        {
            "company_name": "VK",
            "title": "Python Developer",
            "salary_from": 100000,
            "salary_to": 150000,
            "vacancy_url": "https://hh.ru/vacancy/123",
        }
    ]
    db_manager_mock.db.fetch_query.return_value = expected

    # Act
    result = db_manager_mock.get_all_vacancies()

    # Assert
    assert result == expected
    db_manager_mock.db.fetch_query.assert_called_once()


def test_get_avg_salary(db_manager_mock: DBManager) -> None:
    """Тест получения средней зарплаты"""
    # Arrange
    expected = [{"avg_salary": 125000.50}]
    db_manager_mock.db.fetch_query.return_value = expected

    # Act
    result = db_manager_mock.get_avg_salary()

    # Assert
    assert result == expected
    db_manager_mock.db.fetch_query.assert_called_once()


def test_get_vacancies_with_higher_salary(db_manager_mock: DBManager) -> None:
    """Тест получения вакансий с зарплатой выше средней"""
    # Arrange
    expected = [
        {"title": "Senior Python Developer", "salary_from": 200000},
        {"title": "Lead Developer", "salary_from": 250000},
    ]
    db_manager_mock.db.fetch_query.return_value = expected

    # Act
    result = db_manager_mock.get_vacancies_with_higher_salary()

    # Assert
    assert result == expected
    db_manager_mock.db.fetch_query.assert_called_once()


def test_get_vacancies_with_keyword(db_manager_mock: DBManager) -> None:
    """Тест получения вакансий по ключевому слову"""
    # Arrange
    keyword = "python"
    expected = [
        {"title": "Python Developer"},
        {"title": "Senior Python Engineer"},
    ]
    db_manager_mock.db.fetch_query.return_value = expected

    # Act
    result = db_manager_mock.get_vacancies_with_keyword(keyword)

    # Assert
    assert result == expected
    db_manager_mock.db.fetch_query.assert_called_once_with(
        "\n        select * \n        from vacancies \n        where lower(title) like %s\n        ",
        (f"%{keyword}%",),
    )


def test_get_companies_id(db_manager_mock: DBManager) -> None:
    """Тест получения списка ID компаний"""
    # Arrange
    expected_db_response = [{"company_id": 1122462}, {"company_id": 15478}, {"company_id": 11063264}]
    db_manager_mock.db.fetch_query.return_value = expected_db_response

    # Act
    result = db_manager_mock.get_companies_id()

    # Assert
    assert result == [1122462, 15478, 11063264]
    db_manager_mock.db.fetch_query.assert_called_once()


def test_save_vacancies(db_manager_mock: DBManager) -> None:
    """Тест сохранения списка вакансий"""
    # Arrange
    vacancies = VacancyList(
        [
            Vacancy(123, "http://test.com", "Test Job", "Description", 15478, "Moscow", 100000, 150000),
            Vacancy(124, "http://test.com/2", "Test Job 2", "Description 2", 15478, "SPb", 120000, 180000),
        ]
    )
    db_manager_mock.db.execute_query.return_value = 1

    # Act
    db_manager_mock.save_vacancies(vacancies)

    # Assert
    assert db_manager_mock.db.execute_query.call_count == 2


def test_save_vacancies_with_error(db_manager_mock: DBManager) -> None:
    """Тест сохранения вакансий с ошибкой (например, дубликат)"""
    # Arrange
    vacancies = VacancyList([Vacancy(123, "http://test.com", "Test Job", "Desc", 15478, "Moscow", 100000, 150000)])
    db_manager_mock.db.execute_query.side_effect = Exception("Duplicate key")

    # Act - не должно падать, только логирование
    db_manager_mock.save_vacancies(vacancies)

    # Assert
    db_manager_mock.db.execute_query.assert_called_once()
