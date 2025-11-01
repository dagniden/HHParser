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
    def __init__(self):
        DBStorage.initialize_database()
        self.db = DBStorage()

    def get_companies_and_vacancies_count():
        pass

    def get_all_vacancies():
        pass

    def get_avg_salary():
        pass

    def get_vacancies_with_higher_salary():
        pass

    def get_vacancies_with_keyword():
        pass

    def get_companies_id(self) -> list[int]:
        """Получает список ID компаний"""
        query = "select company_id from companies;"
        companies = self.db.fetch_query(query)
        return [company['company_id'] for company in companies]

    def save_vacancies(self, vacancies: VacancyList):
        """Сохраняет вакансии в базу данных"""
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
