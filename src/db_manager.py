import os

from src.models import VacancyList
from src.storage import DBStorage
from src.vacancy_api import HHClient
from loguru import logger

# Конфигурация логгера для файла
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "db_manager.log")
logger.add(sink=log_file, level="DEBUG")


class DBManager:
    """Класс для бизнес-логики работы с базой данных вакансий"""

    def __init__(self) -> None:
        """Инициализирует DBManager, создает БД и таблицы если их нет"""
        DBStorage.initialize_database()
        self.db: DBStorage = DBStorage()

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """
        Получает список всех компаний и количество вакансий у каждой.

        Returns:
            Список словарей с полями company_name и vacancies_count
        """
        pass

    def get_all_vacancies(self) -> list[dict]:
        """
        Получает список всех вакансий с информацией о компаниях.

        Returns:
            Список словарей с полями: company_name, title, salary_from, salary_to, vacancy_url
        """
        pass

    def get_avg_salary(self) -> float:
        """
        Вычисляет среднюю зарплату по всем вакансиям.

        Returns:
            Средняя зарплата (salary_from)
        """
        pass

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """
        Получает список вакансий с зарплатой выше средней.

        Returns:
            Список словарей с информацией о вакансиях
        """
        pass

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict]:
        """
        Получает список вакансий, содержащих ключевое слово в названии.

        Args:
            keyword: Ключевое слово для поиска

        Returns:
            Список словарей с информацией о вакансиях
        """
        pass

    def get_companies_id(self) -> list[int]:
        """
        Получает список ID всех компаний из БД.

        Returns:
            Список идентификаторов компаний
        """
        query = "select company_id from companies;"
        companies = self.db.fetch_query(query)
        return [company['company_id'] for company in companies]

    def save_vacancies(self, vacancies: VacancyList) -> None:
        """
        Сохраняет список вакансий в базу данных.

        Args:
            vacancies: Объект VacancyList с вакансиями для сохранения

        Note:
            Дубликаты (по hh_id) автоматически пропускаются с логированием warning
        """
        for vacancy in vacancies:
            try:
                params = (vacancy.vacancy_id,
                          vacancy.vacancy_url,
                          vacancy.title,
                          vacancy.description,
                          vacancy.company_id,
                          vacancy.area_name,
                          vacancy.salary_from,
                          vacancy.salary_to)

                query = "INSERT INTO vacancies (hh_id, vacancy_url, title, description, company_id, area_name, salary_from, salary_to) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                self.db.execute_query(query, params)
                logger.debug(f"Сохранена вакансия: {vacancy.vacancy_id=} {vacancy.title=}")
            except Exception as e:
                print(f"Ошибка при сохранении вакансии: {e}")


if __name__ == "__main__":
    db_manager = DBManager()
    result = db_manager.get_companies_id()
    print(result)

    hh = HHClient()
    vacancy_list = hh.fetch_vacancies("", 15478, 1)
    db_manager.save_vacancies(vacancy_list)
