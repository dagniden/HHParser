import json
import os
from abc import ABC, abstractmethod

from loguru import logger

from src.models import Vacancy

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "storage.log")
logger.add(sink=log_file, level="DEBUG")


class BaseStorage(ABC):
    @abstractmethod
    def create(self, vacancy):
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def read(self):
        """Получает данные из файла"""
        pass

    @abstractmethod
    def update(self, vacancy):
        """Обновляет вакансию в файле"""
        pass

    @abstractmethod
    def delete(self, vacancy):
        """Удаляет вакансию из файла"""
        pass


class JSONStorage(BaseStorage):
    def __init__(self, filename="vacancies.json"):
        self.__filename = filename
        self.data = []
        logger.info(f"Инициализация JSONStorage с файлом: {filename}")
        self._init_file()
        self.read()

    def _init_file(self):
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

    def _save(self):
        """Сохраняет данные в файл"""
        try:
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            logger.debug(f"Данные сохранены в файл: {self.__filename}, записей: {len(self.data)}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных в файл {self.__filename}: {e}")
