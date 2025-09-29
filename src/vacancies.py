from abc import ABC, abstractmethod


class BaseVacancy(ABC):
    """Класс для представления вакансии"""

    pass


class Vacancy(BaseVacancy):

    __slots__ = ("salary_from", "salary_to", "title", "description")

    def __str__(self):
        return f"{self.__dict__}"


class VacancyList:
    pass