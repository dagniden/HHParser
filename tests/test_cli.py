import pytest

from src.cli import CLI
from src.models import Vacancy


# ===== ТЕСТЫ ДЛЯ __get_user_input =====
def test_get_user_input_str(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "  Python  ")
    result = CLI._get_user_input("Введите строку: ", str)
    assert result == "Python"


def test_get_user_input_int(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["abc", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    printed = []
    monkeypatch.setattr("builtins.print", lambda msg: printed.append(msg))
    result = CLI._get_user_input("Введите число: ", int)
    assert result == 42
    assert any("некорректное" in msg.lower() for msg in printed)


# ===== ТЕСТЫ ДЛЯ __get_user_choice =====
def test_get_user_choice_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "Да")
    result = CLI._get_user_choice("Ваш выбор: ", ["да", "нет"])
    assert result == "да"


def test_get_user_choice_invalid_then_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["maybe", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    printed = []
    monkeypatch.setattr("builtins.print", lambda msg: printed.append(msg))
    cli = CLI()
    result = cli._get_user_choice("Ваш выбор: ", ["да", "нет"])
    assert result == "нет"
    assert any("некорректное" in msg.lower() for msg in printed)


# ===== ТЕСТЫ ASK МЕТОДОВ =====
def test_ask_search_query(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "Python developer")
    result = CLI.ask_search_query()
    assert result == "Python developer"


def test_ask_top_n_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["да", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = CLI.ask_top_n()
    assert result == 5


def test_ask_top_n_no(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")
    result = CLI.ask_top_n()
    assert result is None


def test_ask_filter_range_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["да", "100000", "200000"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = CLI.ask_filter_range()
    assert result == (100000, 200000)


def test_ask_filter_range_no(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")
    result = CLI.ask_filter_range()
    assert result == (None, None)


def test_ask_region_name_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "Москва")
    regions = {"Москва": 1, "Сочи": 2}
    result = CLI.ask_region_name(regions)
    assert result == 1


def test_ask_region_name_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["Питер", "Москва"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    printed = []
    monkeypatch.setattr("builtins.print", lambda msg: printed.append(msg))
    regions = {"Москва": 1}
    result = CLI.ask_region_name(regions)
    assert result == 1
    assert any("отсутствует" in msg.lower() for msg in printed)


def test_ask_filter_by_word_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    inputs = iter(["да", "Python Developer"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = CLI.ask_filter_by_word()
    assert result == ["python", "developer"]


def test_ask_filter_by_word_no(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")
    result = CLI.ask_filter_by_word()
    assert result is None


# ===== ТЕСТ SHOW_MENU =====
def test_show_menu_option_1(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "1")
    result = CLI.show_menu()
    assert result == "1. Показать сохраненные вакансии"


def test_show_menu_option_2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "2")
    result = CLI.show_menu()
    assert result == "2. Сделать новый поиск вакансий"


def test_show_menu_option_3(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "3")
    result = CLI.show_menu()
    assert result == "3. Выход"


# ===== ТЕСТ DISPLAY_VACANCIES =====
def test_display_vacancies(monkeypatch: pytest.MonkeyPatch) -> None:
    vacancies = [
        Vacancy(1, "", "Dev", "", "Comp", "Moscow", 100000, 200000),
        Vacancy(2, "", "Analyst", "", "Comp", "Sochi", 120000, None),
    ]
    printed = []
    monkeypatch.setattr("builtins.print", lambda msg: printed.append(msg))
    CLI.display_vacancies(vacancies)
    assert all(isinstance(p, Vacancy) or isinstance(p, str) for p in printed)
