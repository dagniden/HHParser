import json
from abc import ABC, abstractmethod

from src.models import Vacancy


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
        self.__filename = filename  # Приватный атрибут с значением по умолчанию
        self.data = []
        self._init_file()
        self.read()

    def _init_file(self):
        """Создает файл с пустым JSON-массивом, если его нет"""
        try:
            with open(self.__filename, "x", encoding="utf-8") as file:
                json.dump([], file)
        except FileExistsError:
            pass

    def create(self, vacancy: Vacancy):
        """Добавляет новую вакансию без дублей"""
        self.read()

        # Проверка на дубли
        if not any(item["vacancy_id"] == vacancy.vacancy_id for item in self.data):
            self.data.append(vacancy.to_dict())
            self._save()
            return True
        return False

    def read(self):
        """Получает данные из файла"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                return self.data
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []
            return []

    def update(self, vacancy: Vacancy):
        """Обновляет существующую вакансию"""
        self.read()

        for index, item in enumerate(self.data):
            if item["vacancy_id"] == vacancy.vacancy_id:
                self.data[index] = vacancy.to_dict()
                self._save()
                return True
        return False

    def delete(self, vacancy_id: int):
        """Удаляет вакансию по ID"""
        self.read()

        initial_length = len(self.data)
        self.data = [item for item in self.data if int(item["vacancy_id"]) != vacancy_id]

        if len(self.data) < initial_length:
            self._save()
            return True
        return False

    def _save(self):
        """Сохраняет данные в файл"""
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    vacancy1 = Vacancy(
        "99887766",
        "https://api.hh.ru/vacancies/124937232?host=hh.ru",
        "Стилист",
        "Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.",
        "Е-Клиник",
        "Москва",
        125000,
        150000,
    )

    storage = JSONStorage("../data/vacancy.json")
    print(storage.read())

    storage.update(vacancy1)
    print(storage.delete(11223344))
