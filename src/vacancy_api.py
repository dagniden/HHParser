import os
from abc import ABC, abstractmethod

import requests
from loguru import logger

from src.models import Vacancy, VacancyList

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "vacancy_api.log")
logger.add(sink=log_file, level="DEBUG")


class BaseVacancyAPI(ABC):
    BASE_URL: str

    @abstractmethod
    def get_vacancies(self):
        pass


class HHClient(BaseVacancyAPI):
    BASE_URL = "https://api.hh.ru"

    def __init__(self, text: str, area: int = 1, per_page: int = 5):
        self.text = text
        self.area = area
        self.per_page = per_page

    def get_vacancies(self) -> VacancyList:
        """Публичный метод. Получает список вакансий по ключевому слову."""
        params = {"text": self.text,
                  "area": self.area,
                  "per_page": self.per_page,
                  "search_field": ["name", "description"]}

        data = self.__make_request("/vacancies", params).get("items", [])

        logger.debug(f"Ответ от headhunter: {data}")
        logger.debug(f"HHClient response length: {len(data)}")
        result = VacancyList([self.__parse_vacancy(vacancy) for vacancy in data])

        return result

    def get_areas(self):
        data = self.__make_request("/areas")
        logger.debug(f"Получен справочник регионов: {len(data)}")
        return data

    def __make_request(self, endpoint: str, params: dict = {}) -> dict:
        """Приватный метод. Инкапсулирует логику обращения к API HeadHunter."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")

        return response.json()

    @staticmethod
    def __parse_vacancy(data: dict) -> Vacancy:
        logger.debug(f"Добавление новой вакансии в VacancyList: {data}")

        vacancy_id = data.get("id")
        vacancy_url = data.get("url")
        title = data.get("title")
        company_name = (data.get("employer") or {}).get("name")
        area_name = (data.get("area") or {}).get("name")
        salary_from = (data.get("salary") or {}).get("from")
        salary_to = (data.get("salary") or {}).get("to")

        responsibility = (data.get("snippet") or {}).get("responsibility")
        schedule = (data.get("schedule") or {}).get("name")
        description = f'{responsibility} {schedule}.'

        vacancy = Vacancy(
            vacancy_id,
            vacancy_url,
            title,
            description,
            company_name,
            area_name,
            salary_from,
            salary_to
        )

        logger.debug(f"Добавлена Vacancy: {vacancy}")
        return vacancy
