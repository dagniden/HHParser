# Структура проекта
```
src/
├── main.py            # точка входа в программу
├── vacancy_api.py     # классы: BaseVacancyAPI, HHClient
├── models.py          # классы: Vacancy, VacancyList
├── storage.py         # классы: BaseStorage, JSONStorage
├── services.py        # функции фильтрации, сортировки, топ N
└── cli.py             # взаимодействие с пользователем (консоль)

tests/
├── test_client.py
├── test_models.py
├── test_storage.py
└── test_services.py

logs/
├── main.log
└── test_services.py
```
# Диаграмма классов

```mermaid

classDiagram
    class HHClient {
        - base_url: str
        + get_vacancies(query: str, per_page: int) List~Vacancy~
    }

    class Vacancy {
        + id: str
        + title: str
        + company: str
        + salary: float?
        + url: str
    }

    class VacancyList {
        - vacancies: List[Vacancy]
        + add(v: Vacancy) void
        + filter_by_salary(min: float, max: float) -> VacancyList
        + top_n(n: int) VacancyList
        + __iter__()
    }

    class BaseStorage {
        <<abstract>>
        + save(data: Any, path: str) void
        + load(path: str) Any
    }

    class JSONStorage {
        + save(data: Any, path: str) void
        + load(path: str) Any
    }

    class Service {
        + filter_vacancies(vacancies: VacancyList, keyword: str) VacancyList
        + sort_vacancies(vacancies: VacancyList, by: str) VacancyList
        + get_top_n(vacancies: VacancyList, n: int) VacancyList
    }

    HHClient --> VacancyList : "возвращает"
    VacancyList --> Vacancy : "содержит *"
    JSONStorage --|> BaseStorage
    Service --> VacancyList : "работает с"

```
# Справочная информация по API HH

1. Описание эндпоинта получения вакансий:
https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies

2. Описание Дерево всех регионов
https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas