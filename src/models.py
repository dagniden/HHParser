import os

from loguru import logger

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "models.log")
logger.add(sink=log_file, level="DEBUG")


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = (
        "vacancy_id",
        "vacancy_url",
        "title",
        "description",
        "company_name",
        "area_name",
        "salary_from",
        "salary_to",
    )

    def __init__(self, vacancy_id, vacancy_url, title, description, company_name, area_name, salary_from, salary_to):
        logger.debug(f"Создание вакансии: ID={vacancy_id}, Title='{title}'")

        self.vacancy_id = vacancy_id
        self.vacancy_url = vacancy_url
        self.title = title
        self.description = description
        self.company_name = company_name
        self.area_name = area_name
        self.salary_from = self.__validate_salary_from(salary_from)
        self.salary_to = self.__validate_salary_to(salary_to)

        logger.info(
            f"Вакансия создана: ID={vacancy_id}, Title='{title}', "
            f"Salary={self.salary_from}-{self.salary_to}, Company='{company_name}'"
        )

    @staticmethod
    def __validate_salary_from(value):
        if value is None or value < 0:
            logger.debug(f"Валидация salary_from: {value} -> 0")
            return 0
        logger.debug(f"Валидация salary_from: {value} -> {value}")
        return value

    @staticmethod
    def __validate_salary_to(value):
        if value is None or value < 0:
            logger.debug(f"Валидация salary_to: {value} -> inf")
            return float("inf")
        logger.debug(f"Валидация salary_to: {value} -> {value}")
        return value

    def __str__(self) -> str:
        attrs = {slot: getattr(self, slot) for slot in self.__slots__}
        return f"{attrs}"

    def __repr__(self) -> str:
        attrs = {slot: getattr(self, slot) for slot in self.__slots__}
        return f"{attrs}"

    def to_dict(self) -> dict:
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def salary_tuple(self):
        return self.salary_from, self.salary_to

    def __lt__(self, other):
        result = self.salary_tuple() < other.salary_tuple()
        logger.debug(f"Сравнение {self.vacancy_id} < {other.vacancy_id}: {result}")
        return result

    def __le__(self, other):
        return self.salary_tuple() <= other.salary_tuple()

    def __eq__(self, other):
        result = self.salary_tuple() == other.salary_tuple()
        logger.debug(f"Сравнение {self.vacancy_id} == {other.vacancy_id}: {result}")
        return result

    def __gt__(self, other):
        result = self.salary_tuple() > other.salary_tuple()
        logger.debug(f"Сравнение {self.vacancy_id} > {other.vacancy_id}: {result}")
        return result

    def __ge__(self, other):
        return self.salary_tuple() >= other.salary_tuple()


class VacancyList:
    """Класс для хранения списка вакансий"""

    def __init__(self, vacancies: list[Vacancy] = None) -> None:
        self.vacancies = vacancies if vacancies else []
        logger.info(f"VacancyList инициализирован с {len(self.vacancies)} вакансиями")

    def add(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)
        logger.debug(f"Добавлена вакансия в список: ID={vacancy.vacancy_id}, всего вакансий: {len(self.vacancies)}")

    def __len__(self) -> int:
        return len(self.vacancies)

    def filter_by_salary_range(self, min_val: float, max_val: float) -> list[Vacancy]:
        logger.debug(f"Фильтрация по зарплате: {min_val} - {max_val}")
        result = []
        for x in self.vacancies:
            if x.salary_from <= max_val and x.salary_to >= min_val:
                result.append(x)

        logger.info(
            f"Фильтрация по зарплате {min_val}-{max_val}: " f"найдено {len(result)} из {len(self.vacancies)} вакансий"
        )
        return result

    def get_top_n(self, n: int) -> list[Vacancy]:
        logger.debug(f"Получение топ-{n} вакансий")
        sorted_vacancies = sorted(self.vacancies, reverse=True)
        result = sorted_vacancies[:n]

        logger.info(f"Получено топ-{n} вакансий из {len(self.vacancies)}")
        if result:
            logger.debug(
                f"Топ вакансия: ID={result[0].vacancy_id}, " f"Salary={result[0].salary_from}-{result[0].salary_to}"
            )
        return result

    def filter_by_words(self, words: list[str]) -> list[Vacancy]:
        logger.debug(f"Фильтрация по ключевым словам: {words}")
        result = []
        lower_words = [w.lower() for w in words]

        for vacancy in self.vacancies:
            text = (vacancy.title + " " + vacancy.description).lower()
            if any(word in text for word in lower_words):
                result.append(vacancy)

        logger.info(f"Фильтрация по словам {words}: " f"найдено {len(result)} из {len(self.vacancies)} вакансий")
        return result
