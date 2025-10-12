# Документация проекта: Агрегатор вакансий

## Описание проекта

Консольное приложение для поиска и управления вакансиями с платформы HeadHunter. Проект реализует паттерны
проектирования для работы с внешними API, хранением данных и пользовательским интерфейсом.

## Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/dagniden/HHParser.git

# Установка зависимостей
poetry install

# Запуск приложения
python src/main.py
```

## Архитектура проекта

### Структура файлов

```
src/
├── main.py            # точка входа в программу
├── vacancy_api.py     # BaseVacancyAPI, HHClient
├── models.py          # Vacancy, VacancyList
├── storage.py         # BaseStorage, JSONStorage - реализует CRUD хранилище
└── cli.py             # интерфейс пользователя (консоль)

tests/
├── test_client.py
├── test_models.py
├── test_storage.py
└── test_cli.py

logs/
├── main.log
├── vacancy_api.log
├── storage.log
└── models.log
```

### Диаграмма классов

```mermaid
classDiagram
    class BaseVacancyAPI {
        <<abstract>>
        +BASE_URL: str
        +fetch_vacancies(search_string, region)* VacancyList
    }

    class HHClient {
        +BASE_URL: str
        -__region_names: dict
        +region_names: dict
        +fetch_vacancies(search_string, region, per_page) VacancyList
        +fetch_regions() None
        -__make_request(endpoint, params) dict|list
        +parse_vacancy(data) Vacancy
        +parse_regions(data) dict
    }

    class Vacancy {
        +vacancy_id: str
        +vacancy_url: str
        +title: str
        +description: str
        +company_name: str
        +area_name: str
        +salary_from: float
        +salary_to: float
        +__init__(vacancy_id, vacancy_url, title, description, company_name, area_name, salary_from, salary_to)
        -__validate_salary_from(value) float
        -__validate_salary_to(value) float
        +to_dict() dict
        +salary_tuple() tuple
        +__str__() str
        +__repr__() str
        +__lt__(other) bool
        +__le__(other) bool
        +__eq__(other) bool
        +__gt__(other) bool
        +__ge__(other) bool
    }

    class VacancyList {
        +vacancies: List~Vacancy~
        +__init__(vacancies)
        +add(vacancy) None
        +__len__() int
        +filter_by_salary_range(min_val, max_val) VacancyList
        +get_top_n(n) VacancyList
        +filter_by_words(words) VacancyList
        +__iter__() Iterator
        +__getitem__(index) Vacancy
    }

    class BaseStorage {
        <<abstract>>
        +create(vacancy)* bool
        +read()* list
        +update(vacancy)* bool
        +delete(vacancy)* bool
    }

    class JSONStorage {
        -__filename: str
        +data: list
        +__init__(filename)
        -_init_file() None
        +create(vacancy) bool
        +read() list
        +update(vacancy) bool
        +delete(vacancy) bool
        -_save() None
        +read_as_vacancy_list() VacancyList
    }

    class CLI {
        <<static>>
        +ask_search_query() str
        +ask_top_n() int|None
        +ask_filter_range() tuple
        -__get_user_input(message, input_type) int|str
        -__get_user_choice(message, correct_choices) str
        +display_vacancies(vacancies) None
        +show_menu() str
    }

    HHClient --|> BaseVacancyAPI: наследуется от
    HHClient --> VacancyList: возвращает
    VacancyList o-- Vacancy: содержит
    JSONStorage --|> BaseStorage: наследуется от
    JSONStorage --> VacancyList: возвращает
    JSONStorage --> Vacancy: работает с
    CLI --> Vacancy: отображает
```

## API Reference

### `HHClient`

Клиент для работы с API HeadHunter.

**Атрибуты:**

- `BASE_URL: str` — базовый URL API HeadHunter (`https://api.hh.ru`)
- `region_names: dict` — справочник регионов (только чтение)

**Методы:**

- `fetch_vacancies(search_string: str, region: int = 1, per_page: int = 5) -> VacancyList`

  Получает список вакансий по поисковому запросу.

  - `search_string` — ключевые слова для поиска
  - `region` — ID региона (по умолчанию 1 — Москва)
  - `per_page` — количество вакансий на странице (макс. 100)
  - **Возвращает:** объект `VacancyList` с найденными вакансиями

- `fetch_regions() -> None`

  Загружает справочник регионов России с кэшированием результата.

- `parse_vacancy(data: dict) -> Vacancy` *(статический)*

  Парсит данные вакансии из ответа API в объект `Vacancy`.

- `parse_regions(data: list[dict]) -> dict` *(статический)*

  Рекурсивно парсит иерархическую структуру регионов в плоский словарь.

**Пример использования:**

```python
from src.vacancy_api import HHClient

client = HHClient()
vacancies = client.fetch_vacancies("Python Developer", region=1, per_page=10)
print(f"Найдено вакансий: {len(vacancies)}")
```

---

### `Vacancy`

Модель данных для представления вакансии с поддержкой сравнения по зарплате.

**Атрибуты:**

| Атрибут        | Тип   | Описание                                    |
|----------------|-------|---------------------------------------------|
| `vacancy_id`   | str   | Уникальный идентификатор                    |
| `vacancy_url`  | str   | Ссылка на вакансию                          |
| `title`        | str   | Название вакансии                           |
| `description`  | str   | Краткое описание                            |
| `company_name` | str   | Название компании                           |
| `area_name`    | str   | Регион                                      |
| `salary_from`  | float | Зарплата от (0 если не указана)             |
| `salary_to`    | float | Зарплата до (inf если не указана)           |

**Методы:**

- `to_dict() -> dict` — конвертирует объект в словарь для сериализации
- `salary_tuple() -> tuple` — возвращает кортеж `(salary_from, salary_to)` для сравнения
- Операторы сравнения: `<`, `<=`, `==`, `>`, `>=` — сравнивают вакансии по зарплатам

**Пример использования:**

```python
vacancy1 = Vacancy("123", "url1", "Python Dev", "desc", "Company A", "Moscow", 100000, 150000)
vacancy2 = Vacancy("124", "url2", "Java Dev", "desc", "Company B", "SPb", 120000, 180000)

print(vacancy1 < vacancy2)  # True (сравнение по зарплате)
print(vacancy1.to_dict())   # Словарь для сохранения
```

---

### `VacancyList`

Контейнер для хранения и фильтрации коллекции вакансий.

**Атрибуты:**

- `vacancies: list[Vacancy]` — список объектов вакансий

**Методы:**

- `add(vacancy: Vacancy) -> None` 
  
  Добавляет вакансию в список.

- `__len__() -> int` 
  
  Возвращает количество вакансий.

- `filter_by_salary_range(min_val: float, max_val: float) -> VacancyList`
  
  Фильтрует вакансии по диапазону зарплат (изменяет текущий объект). Возвращает `self` для цепочки вызовов.

- `get_top_n(n: int) -> VacancyList`
  
  Оставляет только топ-N вакансий с наивысшей зарплатой (изменяет текущий объект). Возвращает `self` для цепочки вызовов.

- `filter_by_words(words: list[str]) -> VacancyList`
  
  Фильтрует вакансии по ключевым словам в названии или описании (изменяет текущий объект). Возвращает `self` для цепочки вызовов.

- `__iter__()` — поддержка итерации по вакансиям
- `__getitem__(index)` — доступ по индексу

**Пример использования:**

```python
from src.models import VacancyList

vacancy_list = VacancyList()
vacancy_list.add(vacancy1)
vacancy_list.add(vacancy2)

# Цепочка фильтров
vacancy_list.filter_by_salary_range(100000, 200000) \
            .filter_by_words(["Python", "Django"]) \
            .get_top_n(5)

for vacancy in vacancy_list:
    print(vacancy)
```

---

### `JSONStorage`

Реализация хранилища данных в формате JSON с поддержкой CRUD-операций.

**Атрибуты:**

- `data: list` — кэш данных из файла

**Методы:**

- `__init__(filename: str = "vacancies.json")`
  
  Инициализирует хранилище. Создает файл, если он не существует.

- `create(vacancy: Vacancy) -> bool`
  
  Сохраняет вакансию в файл. Проверяет на дубликаты по `vacancy_id`.
  - **Возвращает:** `True` если вакансия добавлена, `False` если дубликат

- `read() -> list`
  
  Читает все данные из файла в формате списка словарей.
  - **Возвращает:** список словарей с данными вакансий

- `update(vacancy: Vacancy) -> bool`
  
  Обновляет существующую вакансию по `vacancy_id`.
  - **Возвращает:** `True` если обновлено, `False` если не найдена

- `delete(vacancy: Vacancy) -> bool`
  
  Удаляет вакансию по `vacancy_id`.
  - **Возвращает:** `True` если удалена, `False` если не найдена

- `read_as_vacancy_list() -> VacancyList`
  
  Читает файл и возвращает объект `VacancyList` с объектами `Vacancy`. Преобразует строки `"inf"` в `float("inf")`.

**Пример использования:**

```python
from src.storage import JSONStorage
from src.models import Vacancy

storage = JSONStorage("my_vacancies.json")

# Добавление
vacancy = Vacancy("123", "url", "Title", "desc", "Company", "Moscow", 100000, 150000)
storage.create(vacancy)

# Чтение
vacancy_list = storage.read_as_vacancy_list()
print(f"Сохранено вакансий: {len(vacancy_list)}")

# Обновление
vacancy.salary_from = 120000
storage.update(vacancy)

# Удаление
storage.delete(vacancy)
```

---

### `CLI`

Класс для взаимодействия с пользователем через консоль (все методы статические).

**Методы:**

- `ask_search_query() -> str`
  
  Запрашивает у пользователя поисковый запрос.

- `ask_top_n() -> int | None`
  
  Спрашивает, нужно ли выводить топ-N вакансий. Возвращает число или `None`.

- `ask_filter_range() -> tuple[int | None, int | None]`
  
  Спрашивает о фильтрации по зарплате. Возвращает кортеж `(min_val, max_val)` или `(None, None)`.

- `display_vacancies(vacancies: list[Vacancy]) -> None`
  
  Выводит список вакансий в консоль.

- `show_menu() -> str`
  
  Показывает главное меню и возвращает выбранный пункт в виде строки.

**Пример использования:**

```python
from src.cli import CLI

query = CLI.ask_search_query()
top_n = CLI.ask_top_n()
min_sal, max_sal = CLI.ask_filter_range()

# Отображение результатов
CLI.display_vacancies(vacancy_list)
```

---

## Примечания

- Все методы фильтрации в `VacancyList` изменяют объект **in-place** и возвращают `self` для поддержки цепочки вызовов
- `JSONStorage` автоматически создает файл при инициализации
- Класс `Vacancy` использует `__slots__` для оптимизации памяти
- Все модули поддерживают логирование через `loguru`
## Логирование

Логи сохраняются в директории `logs/`:

- `main.log` — основные события приложения
- `vacancy_api.log` — запросы к API и парсинг данных

Уровень логирования: `DEBUG`

## Внешние API

### HeadHunter API

**Используемые эндпоинты:**

1. **Поиск вакансий:** `GET /vacancies`
   -
   Документация: [hh.ru/openapi/get-vacancies](https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies)

2. **Справочник регионов:** `GET /areas`
   -
   Документация: [hh.ru/openapi/get-areas](https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas)

## Roadmap

- [x] Базовая архитектура проекта
- [x] Интеграция с HeadHunter API
- [x] Модели данных `Vacancy` и `VacancyList`
- [x] Парсинг ответов API
- [x] Справочник регионов с кэшированием
- [x] Реализация `JSONStorage`
- [x] Сравнение вакансий
- [x] Реализация методов `VacancyList`
- [x] Подключение метода `VacancyList.add` при парсинге вакансий
- [x] Добавить логирование в models.py
- [x] Добавить логирование в storage.py
- [x] Консольный интерфейс (CLI)
- [x] Полное покрытие тестами

## Чек-лист требований

### Общие критерии для проекта

- [x] Функциональный код разбит на модули: модуль для взаимодействия с API, модуль для взаимодействия с файлами, модуль
  для взаимодействия с вакансиями.
- [x] Решение выложено на GitHub.
- [x] В проекте есть .gitignore.
- [x] В коммиты не добавлены игнорируемые файлы.
- [x] В проекте есть файл с зависимостями.
- [x] Нет грубых нарушений PEP 8 в оформлении кода.
- [x] В проекте есть «точка входа» — модуль, запустив который можно получить результат всех реализованных в проекте
  функциональностей.
- [x] Классы соответствуют минимум первым двум принципам SOLID.
- [x] Все классы задокументированы.
- [x] Все методы классов задокументированы.
- [x] Все методы классов типизированы.

### Взаимодействие с API

- [x] Создан абстрактный класс для работы с API.
- [x] Реализован метод подключения к API в абстрактном классе.
- [x] Реализован метод получения вакансий отдельно в абстрактном классе.
- [x] Используется декоратор @abstract_method для методов абстрактного класса.
- [x] Абстрактные методы не имеют реализации.
- [x] Создан класс для работы с hh.ru.
- [x] Класс для работы с hh.ru наследуется от абстрактного.
- [x] Реализованы все методы абстрактного класса.
- [x] Атрибуты экземпляра класса — приватные.
- [x] Метод подключения к API hh.ru — приватный.
- [x] В методе подключения к API отправляется запрос на базовый URL.
- [x] В методе подключения к API происходит проверка статус-кода ответа.
- [x] Метод подключения к API hh.ru вызывается в методе получения данных перед отправкой запроса.
- [x] Метод получения данных принимает параметр — ключевое слово для поиска вакансий.
- [x] Метод получения данных формирует параметры для запроса как минимум из text, per_page.
- [x] Метод получения данных отправляет запрос на API hh.ru для получения данных о вакансиях по ключевому слову.
- [x] Метод получения данных собирает данные ответа в формате списка словарей из ключа item.

### Работа с вакансиями

- [x] Создан класс для работы с вакансиями.
- [x] В классе используется __slots__ для экономии памяти.
- [x] У каждого экземпляра вакансии есть минимум 4 атрибута.
- [x] В классе реализованы методы сравнения вакансий по зарплате.
- [x] Методы сравнения реализованы через магические методы.
- [x] В классе реализованы методы для валидации данных.
- [x] Методы валидации — приватные.
- [x] Методы валидации используются при инициализации атрибутов.

### Работа с файлами

- [x] Создан абстрактный класс для работы с файлами.
- [x] Реализован метод получения данных из файла.
- [x] Реализован метод получения добавления данных в файл.
- [x] Реализован метод удаления данных из файла.
- [x] Используется декоратор @abstract_method для методов абстрактного класса.
- [x] Абстрактные методы не имеют реализации.
- [x] Реализован класс для работы с JSON-файлами.
- [x] Класс для работы с JSON-файлами наследуется от абстрактного.
- [x] В JSON-файл сохраняются данные, соответствующие атрибутам класса вакансий, с данными в виде списка словарей.
- [x] Файл не перезаписывается при каждом запуске программы, а добавляет данные.
- [x] Файл не сохраняет дубли вакансий.
- [x] В экземплярах класса есть атрибут — имя файла, которое может быть назначено при создании экземпляра.
- [x] Атрибут имени файла — приватный.
- [x] Атрибут имени файла имеет значение по умолчанию.
- [x] Реализованы дополнительные классы для работы с файлами.

### Вспомогательные функции

- [x] Дублирующаяся функциональность вынесена в функции.
- [x] Вспомогательные функции вынесены в отдельный модуль.
- [x] Вспомогательные функции документированы.
- [x] Вспомогательные функции типизированы.

### Интерфейс управления

- [x] Создана функция взаимодействия с пользователем.
- [x] Функция использует экземпляры классов и их методы, реализованные ранее.
- [x] Не дублируется функциональность, реализованная в классах.
- [x] Интерфейс взаимодействия с пользователем реализован понятным текстом, т. е. в выводе не используются коллекции,
  только человекочитаемые строки.
- [x] Функция взаимодействия с пользователем не перегружена.

### Тестирование

- [x] Написаны тесты для функциональностей проекта.
- [x] Общее покрытие функционального кода — более 70%.

## Зависимости

```
requests>=2.31.0
loguru>=0.7.0
```