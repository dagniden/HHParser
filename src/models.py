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

    def to_dict(self) -> dict:
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def salary_tuple(self):
        return (
            self.salary_from if self.salary_from is not None else 0,
            self.salary_to if self.salary_to is not None else float("inf"),
        )

    def __lt__(self, other):
        return self.salary_tuple() < other.salary_tuple()

    def __le__(self, other):
        return self.salary_tuple() <= other.salary_tuple()

    def __eq__(self, other):
        return self.salary_tuple() == other.salary_tuple()

    def __gt__(self, other):
        return self.salary_tuple() > other.salary_tuple()

    def __ge__(self, other):
        return self.salary_tuple() >= other.salary_tuple()


class VacancyList:
    """Класс для хранения списка вакансий"""

    def __init__(self, vacancies: list[Vacancy]) -> None:
        self.vacancies = vacancies

    def add(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)

    def __len__(self) -> int:
        return len(self.vacancies)

    def filter_by_salary_range(self, min_val: float, max_val: float) -> list[Vacancy]:
        result = []
        for x in self.vacancies:
            from_ = x.salary_from if x.salary_from is not None else 0
            to_ = x.salary_to if x.salary_to is not None else float("inf")

            if from_ <= max_val and to_ >= min_val:
                result.append(x)
        return result

    def get_top_n(self, n: int) -> list[Vacancy]:
        sorted_vacancies = sorted(self.vacancies, reverse=True)
        return sorted_vacancies[:n]

    def filter_by_words(self, words: list[str]) -> list[Vacancy]:
        result = []
        lower_words = [w.lower() for w in words]

        for vacancy in self.vacancies:
            text = (vacancy.title + " " + vacancy.description).lower()
            if any(word in text for word in lower_words):
                result.append(vacancy)
        return result
