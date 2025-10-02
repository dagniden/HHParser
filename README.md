Структура проекта
    - src 
        - main.py
        - clients.py
            - class BaseVacancyAPI(ABC)
            - class HHClient(BaseVacancyAPI)
                - get_vacancies
                - get_areas
                - __make_request
                - __parse_vacancy
        - vacancies.py
            - class BaseVacancy(ABC)
            - class VacancyList
        - CLI.py
            - class
    - tests

Справочная информация по API HH
Поиск по вакансиям
https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies

Дерево всех регионов
https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas