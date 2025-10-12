import os
from abc import ABC, abstractmethod
from functools import cache

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
    """Базовый абстрактный класс для API вакансий."""

    BASE_URL: str

    @abstractmethod
    def fetch_vacancies(self, search_string: str, region: int) -> VacancyList:
        """Получает список вакансий по поисковой строке и региону."""
        pass


class HHClient(BaseVacancyAPI):
    """Клиент для работы с API HeadHunter."""

    BASE_URL = "https://api.hh.ru"
    __region_names = {}

    def __init__(self):
        """Инициализирует клиент и загружает справочник регионов."""
        if not self.__region_names:
            self.fetch_regions()

    def fetch_vacancies(self, search_string: str, region: int = 1, per_page: int = 5) -> VacancyList:
        """Получает список вакансий по ключевому слову и региону."""

        params = {"text": search_string, "area": region, "per_page": per_page, "search_field": ["name", "description"]}

        response = self.__make_request("/vacancies", params).get("items", [])

        logger.debug(f"Ответ от headhunter: {response}")
        logger.debug(f"HHClient response length: {len(response)}")

        vacancy_list = VacancyList()
        # [self.__parse_vacancy(vacancy) for vacancy in response]
        for item in response:
            vacancy = self.__parse_vacancy(item)
            vacancy_list.add(vacancy)
        return vacancy_list

    @property
    def region_names(self):
        """Геттер справочника регионов."""
        return self.__region_names

    @staticmethod
    def __make_request(endpoint: str, params: dict = {}) -> dict | list[dict]:
        """Выполняет HTTP-запрос к API HeadHunter."""
        url = f"{HHClient.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")

        return response.json()

    @staticmethod
    def __parse_vacancy(data: dict) -> Vacancy:
        """Парсит данные вакансии из ответа API в объект Vacancy."""
        logger.debug(f"Парсинг вакансии для добавления в VacancyList: {data}")

        vacancy_id = data.get("id")
        vacancy_url = data.get("alternate_url")
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

    @classmethod
    @cache
    def fetch_regions(cls) -> None:
        """Загружает и кэширует справочник регионов HeadHunter."""

        response = cls.__make_request("/areas")
        logger.debug("Получен справочник регионов")

        regions = cls.parse_regions(response)
        logger.debug(f"Сделан парсинг справочника регионов: {len(regions)}")
        cls.__region_names = regions

    @staticmethod
    def parse_regions(data: list[dict]) -> dict:
        """Рекурсивно парсит иерархическую структуру регионов в плоский словарь."""
        region_names = {}
        for item in data:
            region_names[item["name"]] = int(item["id"])

            if item["areas"]:
                children_names = HHClient.parse_regions(item["areas"])
                region_names.update(children_names)

        return region_names
