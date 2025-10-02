class Vacancy:
    __slots__ = ("salary_from", "salary_to", "title", "description")

    def __init__(self, salary_from: int, salary_to: int, title: str, description: str) -> None:
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.title = title
        self.description = description

    def __str__(self) -> str:
        return f"{self.__slots__}"


class VacancyList:
    def __init__(self, vacancies: list[Vacancy]) -> None:
        self.vacancies = vacancies

    def add(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)
