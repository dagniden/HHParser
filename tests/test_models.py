from src.models import Vacancy, VacancyList


def test_vacancy_valid(vacancy) -> None:
    assert vacancy.vacancy_id == '124937232'
    assert vacancy.vacancy_url == 'https://api.hh.ru/vacancies/124937232?host=hh.ru'
    assert vacancy.title == "Менеджер"
    assert vacancy.description == 'Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.'
    assert vacancy.company_name == 'Е-Клиник'
    assert vacancy.area_name == 'Москва'
    assert vacancy.salary_from == 125000
    assert vacancy.salary_to == 150000


def test_vacancy_str(vacancy: Vacancy) -> None:
    assert str(
        vacancy) == "{'vacancy_id': '124937232', 'vacancy_url': 'https://api.hh.ru/vacancies/124937232?host=hh.ru', 'title': 'Менеджер', 'description': 'Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.', 'company_name': 'Е-Клиник', 'area_name': 'Москва', 'salary_from': 125000, 'salary_to': 150000}"

    assert repr(
        vacancy) == "{'vacancy_id': '124937232', 'vacancy_url': 'https://api.hh.ru/vacancies/124937232?host=hh.ru', 'title': 'Менеджер', 'description': 'Ставить задачи, сопровождать и контролировать их выполнение . Удаленная работа.', 'company_name': 'Е-Клиник', 'area_name': 'Москва', 'salary_from': 125000, 'salary_to': 150000}"


def test_vacancy_list(vacancy: Vacancy) -> None:
    vacancy_list = VacancyList([vacancy])
    assert vacancy_list.vacancies == [vacancy]

    vacancy_list.add(vacancy)
    assert vacancy_list.vacancies == [vacancy, vacancy]
