from src.models import VacancyList
from src.storage import JSONStorage
from src.vacancy_api import HHClient


class CLI:
    """Класс для ввода/вывода информации пользователем"""

    def __init__(self):
        pass

    @staticmethod
    def ask_search_query() -> str:
        return input("Введите запрос для поиска: ")

    @staticmethod
    def ask_top_n() -> int | None:
        print("Вывести только топ N вакансий? Да/Нет\n")
        choice = CLI.__get_user_choice("Ваш выбор: ", ['да', 'нет'])
        if choice == 'да':
            return CLI.__get_user_input("Введите количество вакансий для отображения: ", type(int))
        else:
            return None

    @staticmethod
    def __get_user_input(message: str, input_type: type(str) | type(int)) -> int | str:

        while True:
            user_input = input(message)

            if input_type is int:
                try:
                    result = int(user_input)
                    return result
                except ValueError:
                    print("Введено некорректное значение, попробуйте снова")

            elif input_type is str:
                return user_input.strip()

    @staticmethod
    def __get_user_choice(message: str, correct_choices: list) -> str:
        while True:
            user_input = input(message).strip().lower()
            if user_input in [choice.lower() for choice in correct_choices]:
                return user_input
            print("Введено некорректное значение, попробуйте снова")

    def display_vacancies(self):
        pass

    def show_menu(self):
        pass


class VacancyService:
    """Бизнес-логика приложения"""

    def __init__(self):
        self.api_client = HHClient()
        self.storage = JSONStorage()
        self.vacancy_list = VacancyList()

    def search_and_save(self, query: str, region: int):
        pass

    def get_top_vacancies(self, n: int):
        pass

    def filter_by_keywords(self, words: list[str]):
        pass

    def save_to_storage(self):
        pass