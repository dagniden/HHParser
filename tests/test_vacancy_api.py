import pytest
from unittest.mock import patch, MagicMock

from src.vacancy_api import HHClient
from src.models import Vacancy, VacancyList


@pytest.fixture
def mock_vacancy_data():
    return {
        "id": "123",
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "employer": {"name": "TechCorp"},
        "area": {"name": "Москва"},
        "salary": {"from": 100000, "to": 200000},
        "snippet": {"responsibility": "Разработка", "requirement": "Python"},
        "schedule": {"name": "Полный день"},
    }


@pytest.fixture
def mock_region_data():
    return [
        {
            "id": "1",
            "name": "Россия",
            "areas": [
                {"id": "2", "name": "Москва", "areas": []},
                {"id": "3", "name": "Санкт-Петербург", "areas": []},
            ],
        }
    ]


def test_parse_vacancy(mock_vacancy_data):
    """Проверяем корректность парсинга одной вакансии"""
    vacancy = HHClient.parse_vacancy(mock_vacancy_data)
    assert isinstance(vacancy, Vacancy)
    assert vacancy.vacancy_id == "123"
    assert vacancy.title == "Python Developer"
    assert vacancy.company_name == "TechCorp"
    assert vacancy.area_name == "Москва"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 200000
    assert "Полный день" in vacancy.description


def test_parse_regions(mock_region_data):
    """Проверяем, что регионы парсятся в плоский словарь"""
    regions = HHClient.parse_regions(mock_region_data)
    assert isinstance(regions, dict)
    assert "Россия" in regions
    assert "Москва" in regions
    assert regions["Москва"] == 2


@patch("src.vacancy_api.HHClient._HHClient__make_request")
def test_fetch_regions(mock_request, mock_region_data):
    """Тестирует fetch_regions с мокнутым запросом"""
    mock_request.return_value = mock_region_data

    HHClient.fetch_regions()
    regions = HHClient().region_names

    assert "Москва" in regions
    assert isinstance(regions["Москва"], int)
    mock_request.assert_called_once_with("/areas")


@patch("src.vacancy_api.HHClient._HHClient__make_request")
def test_fetch_vacancies(mock_request, mock_vacancy_data):
    """Проверяем, что fetch_vacancies возвращает VacancyList"""
    mock_request.return_value = {"items": [mock_vacancy_data]}

    client = HHClient()
    result = client.fetch_vacancies("Python", region=1)

    assert isinstance(result, VacancyList)
    assert len(result.vacancies) == 1
    assert result.vacancies[0].title == "Python Developer"


@patch("requests.get")
def test_make_request_success(mock_get):
    """Проверяем, что __make_request возвращает JSON при 200 OK"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_get.return_value = mock_response

    result = HHClient._HHClient__make_request("/vacancies")
    assert result == {"ok": True}


@patch("requests.get")
def test_make_request_failure(mock_get):
    """Проверяем, что при ошибке HTTP выбрасывается исключение"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        HHClient._HHClient__make_request("/vacancies")
