from src.models import Vacancy, VacancyList


def test_vacancy_valid() -> None:
    vacancy1 = Vacancy(200, 300, "Тестировщик", "Тестировать приложения лопатой")
    assert vacancy1.salary_from == 200
    assert vacancy1.salary_to == 300
    assert vacancy1.title == "Тестировщик"
    assert vacancy1.description == "Тестировать приложения лопатой"


def test_vacancy_str(vacancy: Vacancy) -> None:
    assert str(vacancy) == "{'salary_from': 200, 'salary_to': 300, 'title': 'Тестировщик', 'description': 'Тестировать приложения лопатой'}"
    assert repr(vacancy) == "{'salary_from': 200, 'salary_to': 300, 'title': 'Тестировщик', 'description': 'Тестировать приложения лопатой'}"


def test_vacancy_list(vacancy: Vacancy) -> None:
    vacancy_list = VacancyList([vacancy])
    assert vacancy_list.vacancies == [vacancy]

    vacancy_list.add(vacancy)
    assert vacancy_list.vacancies == [vacancy, vacancy]