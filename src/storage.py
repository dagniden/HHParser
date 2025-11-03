import json
import os
from abc import ABC, abstractmethod

import psycopg2
from loguru import logger
from psycopg2.extras import RealDictCursor

from src.models import Vacancy, VacancyList

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "storage.log")
logger.add(sink=log_file, level="DEBUG")


class BaseStorage(ABC):
    @abstractmethod
    def create(self, vacancy: Vacancy) -> bool:
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def read(self) -> list:
        """Получает данные из файла"""
        pass

    @abstractmethod
    def update(self, vacancy: Vacancy) -> bool:
        """Обновляет вакансию в файле"""
        pass

    @abstractmethod
    def delete(self, vacancy: Vacancy) -> bool:
        """Удаляет вакансию из файла"""
        pass


class JSONStorage(BaseStorage):
    def __init__(self, filename: str = "vacancies.json") -> None:
        self.__filename = filename
        self.data: list = []
        logger.info(f"Инициализация JSONStorage с файлом: {filename}")
        self._init_file()
        self.read()

    def _init_file(self) -> None:
        """Создает файл с пустым JSON-массивом, если его нет"""
        try:
            with open(self.__filename, "x", encoding="utf-8") as file:
                json.dump([], file)
            logger.info(f"Создан новый файл: {self.__filename}")
        except FileExistsError:
            logger.debug(f"Файл уже существует: {self.__filename}")

    def create(self, vacancy: Vacancy) -> bool:
        """Добавляет новую вакансию без дублей"""
        logger.debug(f"Попытка добавить вакансию ID: {vacancy.vacancy_id}")
        self.read()

        # Проверка на дубли
        if not any(item["vacancy_id"] == vacancy.vacancy_id for item in self.data):
            self.data.append(vacancy.to_dict())
            self._save()
            logger.info(f"Вакансия добавлена: ID={vacancy.vacancy_id}, Title='{vacancy.title}'")
            return True

        logger.warning(f"Дубликат вакансии: ID={vacancy.vacancy_id} уже существует")
        return False

    def read(self) -> list:
        """Получает данные из файла"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                logger.debug(f"Прочитано {len(self.data)} вакансий из файла {self.__filename}")
                return self.data
        except FileNotFoundError:
            logger.error(f"Файл не найден: {self.__filename}")
            self.data = []
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON из файла {self.__filename}: {e}")
            self.data = []
            return []

    def update(self, vacancy: Vacancy) -> bool:
        """Обновляет существующую вакансию"""
        logger.debug(f"Попытка обновить вакансию ID: {vacancy.vacancy_id}")
        self.read()

        for index, item in enumerate(self.data):
            if item["vacancy_id"] == vacancy.vacancy_id:
                self.data[index] = vacancy.to_dict()
                self._save()
                logger.info(f"Вакансия обновлена: ID={vacancy.vacancy_id}, Title='{vacancy.title}'")
                return True

        logger.warning(f"Вакансия для обновления не найдена: ID={vacancy.vacancy_id}")
        return False

    def delete(self, vacancy: Vacancy) -> bool:
        """Удаляет вакансию"""
        logger.debug(f"Попытка удалить вакансию ID: {vacancy.vacancy_id}")
        self.read()

        initial_length = len(self.data)
        self.data = [item for item in self.data if int(item["vacancy_id"]) != vacancy.vacancy_id]

        if len(self.data) < initial_length:
            self._save()
            logger.info(f"Вакансия удалена: ID={vacancy.vacancy_id}")
            return True

        logger.warning(f"Вакансия для удаления не найдена: ID={vacancy.vacancy_id}")
        return False

    def _save(self) -> None:
        """Сохраняет данные в файл"""
        try:
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            logger.debug(f"Данные сохранены в файл: {self.__filename}, записей: {len(self.data)}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных в файл {self.__filename}: {e}")

    def read_as_vacancy_list(self) -> "VacancyList":
        """
        Читает файл JSON и возвращает объект VacancyList.
        Преобразует строки 'inf' в float('inf').
        """
        self.read()  # загружает self.data из файла
        vacancies = []

        for item in self.data:
            try:
                # Конвертация "inf" → float("inf")
                salary_from = item.get("salary_from")
                salary_to = item.get("salary_to")

                if salary_from == "inf":
                    salary_from = float("inf")
                if salary_to == "inf":
                    salary_to = float("inf")

                vacancy = Vacancy(
                    vacancy_id=item.get("vacancy_id"),
                    vacancy_url=item.get("vacancy_url"),
                    title=item.get("title"),
                    description=item.get("description"),
                    company_id=item.get("company_id"),
                    area_name=item.get("area_name"),
                    salary_from=salary_from,
                    salary_to=salary_to,
                )
                vacancies.append(vacancy)
            except Exception as e:
                logger.error(f"Ошибка при создании Vacancy из записи {item}: {e}")

        logger.info(f"Создан VacancyList из {len(vacancies)} вакансий")
        return VacancyList(vacancies)


class DBStorage(BaseStorage):
    """Хранилище данных в PostgreSQL с управлением соединениями"""

    def __init__(self):
        """Инициализация параметров подключения к целевой БД"""
        self.connection_params = {
            "host": "localhost",
            "database": "parser_db",  # целевая БД
            "user": "postgres",
            "password": "Dpiexmax1",
        }
        logger.info("DBStorage инициализирован с параметрами подключения к parser_db")

    def _get_connection(self):
        """Создаёт новое соединение к БД"""
        return psycopg2.connect(**self.connection_params)

    @classmethod
    def initialize_database(cls):
        """
        Инициализирует БД и таблицы при первом запуске.
        Вызывается один раз перед использованием DBStorage.
        """
        logger.info("Начало инициализации базы данных")

        # Параметры для подключения к служебной БД
        temp_params = {
            "host": "localhost",
            "database": "postgres",  # служебная БД
            "user": "postgres",
            "password": "Dpiexmax1",
        }

        # Шаг 1: Создание БД parser_db если её нет
        try:
            conn = psycopg2.connect(**temp_params)
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Проверка существования БД
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ("parser_db",))
                if not cursor.fetchone():
                    cursor.execute("CREATE DATABASE parser_db")
                    logger.info("База данных parser_db создана")
                else:
                    logger.info("База данных parser_db уже существует")
        except psycopg2.Error as e:
            logger.error(f"Ошибка при создании БД: {e}")
            raise

        # Шаг 2: Создание таблиц в parser_db
        target_params = {**temp_params, "database": "parser_db"}
        try:
            with psycopg2.connect(**target_params) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    # Проверка существования таблиц
                    cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'companies'")
                    if not cursor.fetchone():
                        cls._create_tables(cursor)
                        logger.info("Таблицы созданы и заполнены начальными данными")
                    else:
                        logger.info("Таблицы уже существуют")
        except psycopg2.Error as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            raise

        logger.info("Инициализация базы данных завершена успешно")

    @staticmethod
    def _create_tables(cursor):
        """Создаёт таблицы и заполняет начальными данными"""
        query = """
        DROP TABLE IF EXISTS vacancies CASCADE;
        DROP TABLE IF EXISTS companies CASCADE;

        CREATE TABLE companies
        (
            company_id INT PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL
        );

        INSERT INTO companies VALUES (1122462, 'Skyeng');
        INSERT INTO companies VALUES (15478, 'VK');
        INSERT INTO companies VALUES (11063264, 'Яндекс');
        INSERT INTO companies VALUES (681672, 'USETECH');
        INSERT INTO companies VALUES (2180, 'Ozon');
        INSERT INTO companies VALUES (3529, 'СБЕР');
        INSERT INTO companies VALUES (4309, 'Ингосстрах');
        INSERT INTO companies VALUES (5860936, 'Лоция');
        INSERT INTO companies VALUES (80, 'Альфа-Банк');
        INSERT INTO companies VALUES (3776, 'МТС');

        CREATE TABLE vacancies
        (
            isn SERIAL PRIMARY KEY,
            hh_id BIGINT UNIQUE NOT NULL,
            vacancy_url TEXT,
            title TEXT NOT NULL,
            description TEXT,
            company_id INT NOT NULL,
            area_name VARCHAR(255),
            salary_from DECIMAL,
            salary_to DECIMAL,
            CONSTRAINT fk_vacancies_company_id FOREIGN KEY (company_id)
                REFERENCES companies(company_id) ON DELETE CASCADE
        );
        """
        cursor.execute(query)

    def execute_query(self, query: str, params=None) -> int:
        """
        Выполняет запрос INSERT/UPDATE/DELETE и возвращает количество затронутых строк.

        Args:
            query: SQL запрос
            params: Параметры для запроса (tuple или dict)

        Returns:
            Количество затронутых строк
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    affected_rows = cursor.rowcount
                    logger.debug(f"Запрос выполнен, затронуто строк: {affected_rows}")
                    return affected_rows
        except psycopg2.IntegrityError as e:
            logger.warning(f"Нарушено ограничение в базе данных: {e}")
        except psycopg2.Error as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise

    def fetch_query(self, query: str, params=None) -> list[dict]:
        """
        Выполняет SELECT запрос и возвращает результат в виде списка словарей.

        Args:
            query: SQL запрос SELECT
            params: Параметры для запроса (tuple или dict)

        Returns:
            Список словарей с результатами запроса
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
                    logger.debug(f"Запрос выполнен, получено строк: {len(result)}")
                    return result
        except psycopg2.Error as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise

    def create(self, vacancy: Vacancy) -> bool:
        pass

    def read(self) -> list:
        pass

    def update(self, vacancy: Vacancy) -> bool:
        pass

    def delete(self, vacancy: Vacancy) -> bool:
        pass
