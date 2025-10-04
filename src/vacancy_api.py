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
    def get_vacancies(self, search_string: str, region: int) -> VacancyList:
        pass


class HHClient(BaseVacancyAPI):
    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        self.region_names = self.fetch_regions()

    def get_vacancies(self, search_string: str, region: int = 1, per_page: int = 5) -> VacancyList:
        """Публичный метод. Получает список вакансий по ключевому слову."""
        params = {"text": search_string, "area": region, "per_page": per_page, "search_field": ["name", "description"]}

        response = self.__make_request("/vacancies", params).get("items", [])

        logger.debug(f"Ответ от headhunter: {response}")
        logger.debug(f"HHClient response length: {len(response)}")
        result = VacancyList([self.__parse_vacancy(vacancy) for vacancy in response])

        return result

    def __make_request(self, endpoint: str, params: dict = {}) -> dict | list[dict]:
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
        description = f"{responsibility} {schedule}."

        vacancy = Vacancy(vacancy_id, vacancy_url, title, description, company_name, area_name, salary_from, salary_to)

        logger.debug(f"Добавлена Vacancy: {vacancy}")
        return vacancy

    def fetch_regions(self) -> dict:
        """Запрашивает список регионов с HH для сохранения их в self.region_names"""

        response = self.__make_request("/areas")
        logger.debug("Получен справочник регионов")

        regions = self.parse_regions(response)
        logger.debug(f"Сделан парсинг справочника регионов: {len(regions)}")
        return regions

    def parse_regions(self, data: list[dict]) -> dict:
        region_names = {}
        for item in data:
            region_names[item["name"]] = int(item["id"])

            if item["areas"]:
                children_names = self.parse_regions(item["areas"])
                region_names.update(children_names)

        return region_names
