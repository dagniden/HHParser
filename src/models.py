class Vacancy:
    """Класс для представления вакансии"""
    __slots__ = ("salary_from", "salary_to", "title", "description")

    def __init__(self, salary_from: int, salary_to: int, title: str, description: str) -> None:

        self.salary_from = salary_from
        self.salary_to = salary_to
        self.title = title
        self.description = description

    def __str__(self) -> str:
        attrs = {slot: getattr(self, slot) for slot in self.__slots__}
        return f"{attrs}"

    def __repr__(self) -> str:
        attrs = {slot: getattr(self, slot) for slot in self.__slots__}
        return f"{attrs}"


class VacancyList:
    """Класс для хранения списка вакансий"""
    def __init__(self, vacancies: list[Vacancy]) -> None:
        self.vacancies = vacancies

    def add(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)
