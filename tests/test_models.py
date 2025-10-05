import pytest

from src.models import Vacancy, VacancyList


def test_vacancy_valid(vacancy) -> None:
    assert vacancy.vacancy_id == "124937232"
    assert vacancy.vacancy_url == "https://api.hh.ru/vacancies/124937232?host=hh.ru"
    assert vacancy.title == "Менеджер"
    assert vacancy.description == "Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа."
    assert vacancy.company_name == "Е-Клиник"
    assert vacancy.area_name == "Москва"
    assert vacancy.salary_from == 125000
    assert vacancy.salary_to == 150000


def test_vacancy_invalid(vacancy) -> None:
    with pytest.raises(AttributeError):
        vacancy.company_abc = 123


def test_vacancy_str(vacancy: Vacancy) -> None:
    assert (
            str(vacancy)
            == "{'vacancy_id': '124937232', 'vacancy_url': 'https://api.hh.ru/vacancies/124937232?host=hh.ru', "
               "'title': 'Менеджер', "
               "'description': 'Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.', "
               "'company_name': 'Е-Клиник', 'area_name': 'Москва', 'salary_from': 125000, 'salary_to': 150000}"
    )

    assert (
            repr(vacancy)
            == "{'vacancy_id': '124937232', 'vacancy_url': 'https://api.hh.ru/vacancies/124937232?host=hh.ru', "
               "'title': 'Менеджер', "
               "'description': 'Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.', "
               "'company_name': 'Е-Клиник', 'area_name': 'Москва', 'salary_from': 125000, 'salary_to': 150000}"
    )


def test_vacancy_comparison() -> None:
    v1 = Vacancy(1, "", "Vacancy1", "", "Comp", "Moscow", 100000, 200000)
    v2 = Vacancy(2, "", "Vacancy2", "", "Comp", "Moscow", 120000, None)
    v3 = Vacancy(3, "", "Vacancy3", "", "Comp", "Moscow", None, 150000)

    assert (v1 < v2) == True
    assert (v3 < v1) == True
    assert (v1 > v2) == False
    assert (v1 >= v2) == False
    assert (v3 <= v1) == True
    assert (v1 == v1) == True


def test_vacancy_list(vacancy: Vacancy) -> None:
    vacancy_list = VacancyList([vacancy])
    assert vacancy_list.vacancies == [vacancy]

    vacancy_list.add(vacancy)
    assert vacancy_list.vacancies == [vacancy, vacancy]


def test_vacancy_list_filter_by_salary(vacancy_list: VacancyList) -> None:
    res1 = vacancy_list.filter_by_salary_range(50_000, 100_000)

    assert len(res1) == 1
    assert (res1[0].salary_from, res1[0].salary_to) >= (50_000, 100_000)


def test_vacancy_get_top_n():
    v1 = Vacancy(1, "", "Vacancy1", "", "Comp", "Moscow", 100000, 200000)
    v2 = Vacancy(2, "", "Vacancy2", "", "Comp", "Moscow", 120000, None)
    v3 = Vacancy(3, "", "Vacancy3", "", "Comp", "Moscow", None, 150_000)
    v4 = Vacancy(4, "", "Vacancy3", "", "Comp", "Moscow", None, 180_000)
    v5 = Vacancy(5, "", "Vacancy3", "", "Comp", "Moscow", None, 200_000)
    vacancy_list1 = VacancyList([v1, v2, v3, v4, v5])

    top_vacancies = vacancy_list1.get_top_n(2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0] > top_vacancies[1]
