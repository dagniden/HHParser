import os
from abc import ABC, abstractmethod

import requests
from loguru import logger

from src.models import Vacancy

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "headhunterapi.log")
logger.add(sink=log_file, level="DEBUG")


class BaseVacancyAPI(ABC):
    BASE_URL: str

    @abstractmethod
    def get_vacancies(self):
        pass



class HHClient(BaseVacancyAPI):
    BASE_URL = "https://api.hh.ru"

    def get_vacancies(self, text: str, area: int = 1, per_page: int = 5) -> dict:
        """ Публичный метод. Получает список вакансий по ключевому слову. """
        params = {"text": text, "area": area, "per_page": per_page}  # 1 — Москва

        data = self.__make_request("/vacancies", params).get("items", [])

        logger.debug(f"Ответ от headhunter: {data}")
        logger.debug(f"HHClient response length: {len(data)}")
        vacancy_list = [self.__parse_vacancy(vacancy) for vacancy in data]

        return vacancy_list

    def get_areas(self):
        data = self.__make_request("/areas")

        logger.debug(f"Получен справочник регионов: {len(data)}")

        return data

    def __make_request(self, endpoint: str, params: dict = {}) -> dict:
        """ Приватный метод. Инкапсулирует логику обращения к API HeadHunter. """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")

        return response.json()

    def __parse_vacancy(self, data: dict) -> Vacancy:
        vacancy = Vacancy()
        vacancy.area_name = data["area"]["name"]
        vacancy.title = data["name"]
        vacancy.salary_to = data["salary"]["to"]
        vacancy.salary_from = data["name"]["from"]
        vacancy.description = data["snippet"]["responsibility"]
        logger.debug(f"Vacancy info: {vacancy}")
        return vacancy
