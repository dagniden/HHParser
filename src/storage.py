import json
import os
from abc import ABC, abstractmethod

import psycopg2
from loguru import logger

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
                    company_name=item.get("company_name"),
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

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Dpiexmax1"
        )

        self.conn.autocommit = True
        self._create_database("parser_db")

        self.conn.close()

        self.conn = psycopg2.connect(
            host="localhost",
            database="parser_db",
            user="postgres",
            password="Dpiexmax1"
        )
        self.conn.autocommit = True
        self._create_tables()
        self.conn.close()

    def _create_database(self, db_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {db_name}")
        finally:
            cursor.close()

    def _create_tables(self):
        cursor = self.conn.cursor()
        query = """
        DROP TABLE IF EXISTS companies CASCADE;
        DROP TABLE IF EXISTS vacancies CASCADE;
        
        CREATE TABLE companies
         (
            company_id SERIAL,
            company_name VARCHAR(255),
            CONSTRAINT pk_companies_company_id PRIMARY KEY (company_id)
        );
        
        INSERT INTO companies VALUES (1122462, 'Skyeng'); 	-- 1
        INSERT INTO companies VALUES (15478, 'VK'); 		-- 2
        INSERT INTO companies VALUES (11063264, 'Яндекс'); 	-- 3
        INSERT INTO companies VALUES (681672, 'USETECH'); 	-- 4
        INSERT INTO companies VALUES (2180, 'Ozon'); 		-- 5
        INSERT INTO companies VALUES (3529, 'СБЕР'); 		-- 6
        INSERT INTO companies VALUES (4309, 'Ингосстрах'); 	-- 7
        INSERT INTO companies VALUES (5860936, 'Лоция'); 	-- 8
        INSERT INTO companies VALUES (80, 'Альфа-Банк'); 	-- 9
        INSERT INTO companies VALUES (3776, 'МТС'); 		-- 10
        
        CREATE TABLE vacancies
        (
            vacancy_id SERIAL,	        
            vacancy_url TEXT,
            title TEXT,
            description TEXT,
            company_id INT,
            area_name VARCHAR(255),
            salary_from DECIMAL,
            salary_to DECIMAL,
            CONSTRAINT fk_vacancies_company_id FOREIGN KEY (company_id) REFERENCES companies(company_id)
        );
        """
        try:
            cursor.execute(query)
        finally:
            cursor.close()


    def create(self, vacancy: Vacancy) -> bool:
        pass

    def read(self) -> list:
        pass

    def update(self, vacancy: Vacancy) -> bool:
        pass

    def delete(self, vacancy: Vacancy) -> bool:
        pass


if __name__ == "__main__":
    db = DBStorage()
