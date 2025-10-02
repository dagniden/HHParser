# Структура проекта
```
src/
├── main.py            # точка входа в программу
├── vacancy_api.py     # BaseVacancyAPI, HHClient
├── models.py          # Vacancy, VacancyList
├── storage.py         # BaseStorage (CRUD), JSONStorage
└── cli.py             # интерфейс пользователя (консоль)

tests/
├── test_client.py
├── test_models.py
├── test_storage.py
└── test_cli.py

logs/
├── main.log
└── vacancy_api.log

```
# Диаграмма классов

```mermaid

classDiagram
    class BaseVacancyAPI {
        <<abstract>>
        - base_url: str
        + get_vacancies(query: str, per_page: int) -> VacancyList
    }

    class HHClient {
        - base_url: str
        + get_vacancies(query: str, per_page: int) -> VacancyList
    }

    class Vacancy {
        + id: str
        + title: str
        + company: str
        + salary: float
        + url: str
        + to_dict() dict
    }

    class VacancyList {
        # vacancies: List[Vacancy]
        + add(v: Vacancy) -> None
        + filter_by_salary(min: float, max: float) -> VacancyList
        + top_n(n: int) -> VacancyList
        + __iter__()
    }

    class BaseStorage {
        <<abstract>>
        + create(vacancy: Vacancy) -> None
        + read_all() -> VacancyList
        + read(criteria: dict) -> VacancyList
        + update(vacancy: Vacancy) -> None
        + delete(vacancy_id: str) -> None
    }

    class JSONStorage {
        - filename: str
        + create(vacancy: Vacancy) -> None
        + read_all() -> VacancyList
        + read(criteria: dict) -> VacancyList
        + update(vacancy: Vacancy) -> None
        + delete(vacancy_id: str) -> None
    }
        
    HHClient --|> BaseVacancyAPI: наследуется от
    HHClient --> VacancyList: возвращает
    VacancyList --> Vacancy: содержит
    JSONStorage --|> BaseStorage: наследуется от



```
# Справочная информация по API HH

1. Описание эндпоинта получения вакансий:
https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies

2. Описание Дерево всех регионов
https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas


# Todo

- [x] Спроектировать структуру проекта
- [x] Спроектировать классы
- [x] Сделать класс HHClient
- [x] Сделать классы с моделями
- [x] Сделать парсинг ответа от HH в модель Vacancy
- [x] Наполнить VacancyList объектами Vacancy
- [ ] Добавить модель Region
- [ ] Добавить список регионов в HHClient и его наполнение методом get_areas

