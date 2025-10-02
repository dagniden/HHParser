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
        self.vacancy_id = vacancy_id
        self.vacancy_url = vacancy_url
        self.title = title
        self.description = description
        self.company_name = company_name
        self.area_name = area_name
        self.salary_from = salary_from
        self.salary_to = salary_to

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

    def __len__(self) -> int:
        return len(self.vacancies)
