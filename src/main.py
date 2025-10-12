import os

from loguru import logger

from src.cli import CLI
from src.storage import JSONStorage
from src.vacancy_api import HHClient

# Конфигурация логгера для файла
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "main.log")
logger.add(sink=log_file, level="DEBUG")

# Удаляем стандартный консольный sink
logger.remove()  # <- это убирает все существующие sinks, включая консоль

# Добавляем только файловый sink
logger.add(sink=log_file, level="DEBUG")

def main() -> int:
    """Координатор - связывает CLI"""
    cli = CLI()
    hh_client = HHClient()
    filename = os.path.join(current_dir, "..", "data", "vacancies.json")
    storage = JSONStorage(filename)

    while True:
        choice = cli.show_menu()

        if choice == "1. Показать сохраненные вакансии":
            loaded_vacancies = storage.read_as_vacancy_list()
            top_n = cli.ask_top_n()

            if top_n:
                loaded_vacancies.get_top_n(top_n)

            cli.display_vacancies(loaded_vacancies.vacancies)

        elif choice == "2. Сделать новый поиск вакансий":
            region_id = cli.ask_region_name(hh_client.region_names)
            query = cli.ask_search_query()
            min_val, max_val = cli.ask_filter_range()
            top_n = cli.ask_top_n()
            vacancy_list = hh_client.fetch_vacancies(query, region=region_id)
            filter_words = cli.ask_filter_by_word()

            if filter_words:
                vacancy_list.filter_by_words(filter_words)

            if min_val and max_val:
                vacancy_list.filter_by_salary_range(min_val, max_val)

            if top_n:
                vacancy_list.get_top_n(top_n)

            for vacancy in vacancy_list:
                storage.create(vacancy)

            cli.display_vacancies(vacancy_list.vacancies)

        elif choice == "3. Выход":
            return 0


if __name__ == "__main__":
    main()
