import json
import os
import pytest

from src.models import Vacancy
from src.storage import JSONStorage







def test_init_creates_file(test_filename):
    """Тест: инициализация создает файл"""
    storage = JSONStorage(test_filename)
    assert os.path.exists(test_filename)

def test_init_with_existing_file( test_filename):
    """Тест: инициализация с существующим файлом"""
    # Создаем файл с данными
    with open(test_filename, "w", encoding="utf-8") as f:
        json.dump([{"vacancy_id": "999"}], f)

    storage = JSONStorage(test_filename)
    assert len(storage.data) == 1
    assert storage.data[0]["vacancy_id"] == "999"

def test_create_adds_vacancy(test_filename, sample_vacancy):
    """Тест: create добавляет вакансию"""
    storage = JSONStorage(test_filename)
    result = storage.create(sample_vacancy)

    assert result is True
    assert len(storage.data) == 1
    assert storage.data[0]["vacancy_id"] == "12345"

def test_create_prevents_duplicates(test_filename, sample_vacancy):
    """Тест: create не добавляет дубликаты"""
    storage = JSONStorage(test_filename)
    storage.create(sample_vacancy)
    result = storage.create(sample_vacancy)

    assert result is False
    assert len(storage.data) == 1

def test_read_returns_data(test_filename, sample_vacancy):
    """Тест: read возвращает данные"""
    storage = JSONStorage(test_filename)
    storage.create(sample_vacancy)

    data = storage.read()
    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"

def test_read_empty_file(test_filename):
    """Тест: read возвращает пустой список для пустого файла"""
    storage = JSONStorage(test_filename)
    data = storage.read()
    assert data == []

def test_update_existing_vacancy(test_filename, sample_vacancy):
    """Тест: update обновляет существующую вакансию"""
    storage = JSONStorage(test_filename)
    storage.create(sample_vacancy)

    # Обновляем данные вакансии
    updated_vacancy = Vacancy(
        vacancy_id="12345",
        vacancy_url="https://test.com/vacancy/12345",
        title="Senior Python Developer",  # Изменили title
        description="Разработка на Python",
        company_name="Test Company",
        area_name="Москва",
        salary_from=150000,  # Изменили зарплату
        salary_to=200000,
    )

    result = storage.update(updated_vacancy)
    assert result is True
    assert storage.data[0]["title"] == "Senior Python Developer"
    assert storage.data[0]["salary_from"] == 150000

def test_update_nonexistent_vacancy(test_filename, sample_vacancy):
    """Тест: update возвращает False для несуществующей вакансии"""
    storage = JSONStorage(test_filename)

    result = storage.update(sample_vacancy)
    assert result is False

def test_delete_nonexistent_vacancy(test_filename, sample_vacancy):
    """Тест: delete возвращает False для несуществующей вакансии"""
    storage = JSONStorage(test_filename)

    result = storage.delete(sample_vacancy)
    assert result is False

def test_data_persistence(test_filename, sample_vacancy):
    """Тест: данные сохраняются между созданиями экземпляров"""
    storage1 = JSONStorage(test_filename)
    storage1.create(sample_vacancy)

    # Создаем новый экземпляр с тем же файлом
    storage2 = JSONStorage(test_filename)
    assert len(storage2.data) == 1
    assert storage2.data[0]["vacancy_id"] == "12345"

def test_default_filename():
    """Тест: используется имя файла по умолчанию"""
    storage = JSONStorage()
    assert os.path.exists("vacancies.json")
    # Cleanup
    os.remove("vacancies.json")
