from typing import Any

from src.models import Vacancy


class CLI:
    """Класс для ввода/вывода информации пользователем"""

    @staticmethod
    def ask_search_query() -> str:
        return input("Введите запрос для поиска: ")

    @staticmethod
    def ask_top_n() -> int | None:
        print("Вывести только топ N вакансий? Да/Нет\n")
        choice = CLI._get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            return int(CLI._get_user_input("Введите количество вакансий для отображения: ", int))
        else:
            return None

    @staticmethod
    def ask_filter_range() -> tuple[int | None, int | None]:
        print("Фильтровать вакансии по зарплате? Да/Нет\n")
        choice = CLI._get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            min_val = CLI._get_user_input("Введите минимальную зарплату: ", int)
            max_val = CLI._get_user_input("Введите максимальную зарплату: ", int)
            return (int(min_val), int(max_val))
        else:
            return (None, None)

    @staticmethod
    def _get_user_input(message: str, input_type: type[str] | type[int]) -> int | str:
        """Получает ввод пользователя с валидацией типа"""
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

        # This line is unreachable but needed for type checker
        return ""

    @staticmethod
    def _get_user_choice(message: str, correct_choices: list[Any]) -> Any:
        while True:
            user_input = input(message)
            try:
                # Преобразуем ответ пользователя к типу правильного ответа
                user_choice = type(correct_choices[0])(user_input)

                if isinstance(user_choice, str):
                    # Для корректного сравнения строк преобразуем к нижнему регистру
                    user_choice = user_choice.lower()

                if user_choice in correct_choices:
                    return user_choice
                else:
                    print("Введено некорректное значение")
            except ValueError:
                print("Введено некорректное значение")

    @staticmethod
    def display_vacancies(vacancies: list[Vacancy]) -> None:
        for item in vacancies:
            print(item)

    @staticmethod
    def show_menu() -> str:
        print(
            "\nДоступные действия: [1, 2, 3, 4, 5, 6, 7]\n"
            "1. Показать сохраненные вакансии\n"
            "2. Сделать новый поиск вакансий\n"
            "3. Показать список компаний в базе и количество вакансий у каждой\n"
            "4. Показать среднюю зарплату по всем вакансиям\n"
            "5. Показать вакансии с зарплатой выше средней\n"
            "6. Показать вакансии, содержащие ключевое слово в названии\n"
            "7. Выход\n"
        )
        result = CLI._get_user_choice("Ваш выбор: ", [1, 2, 3, 4, 5, 6, 7])

        if result == 1:
            return "1. Показать сохраненные вакансии"
        elif result == 2:
            return "2. Сделать новый поиск вакансий"
        elif result == 3:
            return "3. Показать список компаний в базе и количество вакансий у каждой"
        elif result == 4:
            return "4. Показать среднюю зарплату по всем вакансиям"
        elif result == 5:
            return "5. Показать вакансии с зарплатой выше средней"
        elif result == 6:
            return "6. Показать вакансии, содержащие ключевое слово в названии"
        else:
            return "7. Выход"

    @staticmethod
    def ask_region_name(region_names: dict[str, int]) -> int:
        while True:
            user_input = CLI._get_user_input("Введите регион для поиска вакансий: ", str)

            key = region_names.get(str(user_input))
            if key:
                return key
            else:
                print(f"Введенный регион {user_input} отсутствует в справочнике!")

    @staticmethod
    def ask_filter_by_word() -> list[str] | None:
        print("Фильтровать вакансии по ключевому слову? Да/Нет\n")
        choice = CLI._get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            result = CLI._get_user_input("Введите ключевое слово для фильтрации: ", str)
            return str(result).lower().split()
        else:
            return None

    @staticmethod
    def display_db_results(results: list[dict[str, Any]]) -> None:
        """Отображение результатов запросов к БД в читаемом виде"""
        print("-" * 50)
        for row in results:
            for key, value in row.items():
                print(f"{key}: {value}")
            print("-" * 50)
