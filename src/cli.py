from src.models import Vacancy


class CLI:
    """Класс для ввода/вывода информации пользователем"""

    @staticmethod
    def ask_search_query() -> str:
        return input("Введите запрос для поиска: ")

    @staticmethod
    def ask_top_n() -> int | None:
        print("Вывести только топ N вакансий? Да/Нет\n")
        choice = CLI.__get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            return CLI.__get_user_input("Введите количество вакансий для отображения: ", int)
        else:
            return None

    @staticmethod
    def ask_filter_range():
        print("Фильтровать вакансии по зарплате? Да/Нет\n")
        choice = CLI.__get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            min_val = CLI.__get_user_input("Введите минимальную зарплату: ", int)
            max_val = CLI.__get_user_input("Введите максимальную зарплату: ", int)
            return min_val, max_val
        else:
            return None, None

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
        print("Доступные действия: [1, 2, 3]\n"
              "1. Показать сохраненные вакансии\n"
              "2. Сделать новый поиск вакансий\n"
              "3. Выход")
        result = CLI.__get_user_choice("Ваш выбор: ", [1, 2, 3])

        if result == 1:
            return "1. Показать сохраненные вакансии"
        elif result == 2:
            return "2. Сделать новый поиск вакансий"
        else:
            return "3. Выход"

    @staticmethod
    def ask_region_name(region_names: dict):
        while True:
            user_input = CLI.__get_user_input("Введите регион для поиска вакансий: ", str)

            key = region_names.get(user_input)
            if key:
                return key
            else:
                print(f"Введенный регион {user_input} отсутствует в справочнике!")


    @staticmethod
    def ask_filter_by_word():
        print("Фильтровать вакансии по ключевому слову? Да/Нет\n")
        choice = CLI.__get_user_choice("Ваш выбор: ", ["да", "нет"])
        if choice == "да":
            result = CLI.__get_user_input("Введите ключевое слово для фильтрации: ", str)
            return result.lower().split()
        else:
            return None
