import os

from loguru import logger

from src.cli import CLI
from src.db_manager import DBManager
from src.vacancy_api import HHClient

# Конфигурация логгера для файла
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "main.log")
logger.add(sink=log_file, level="DEBUG")

# Удаляем стандартный консольный sink
logger.remove()

# Добавляем только файловый sink
logger.add(sink=log_file, level="DEBUG")


def main() -> int:
    """Координатор - связывает CLI"""
    cli = CLI()
    hh_client = HHClient()

    db_manager = DBManager()
    companies_id = db_manager.get_companies_id()

    while True:
        choice = cli.show_menu()

        if choice == "1. Показать сохраненные вакансии":
            vacancies = db_manager.get_all_vacancies()
            cli.display_db_results(vacancies)

        elif choice == "2. Сделать новый поиск вакансий":
            region_id = cli.ask_region_name(hh_client.region_names)
            query = cli.ask_search_query()
            min_val, max_val = cli.ask_filter_range()
            top_n = cli.ask_top_n()
            filter_words = cli.ask_filter_by_word()

            for company_id in companies_id:
                vacancy_list = hh_client.fetch_vacancies(query, company_id, region_id)

                if filter_words:
                    vacancy_list.filter_by_words(filter_words)

                if min_val and max_val:
                    vacancy_list.filter_by_salary_range(min_val, max_val)

                if top_n:
                    vacancy_list.get_top_n(top_n)

                db_manager.save_vacancies(vacancy_list)
                cli.display_vacancies(vacancy_list.vacancies)

        elif choice == "3. Показать список компаний в базе и количество вакансий у каждой":
            res = db_manager.get_companies_and_vacancies_count()
            cli.display_db_results(res)

        elif choice == "4. Показать среднюю зарплату по всем вакансиям":
            res = db_manager.get_avg_salary()
            cli.display_db_results(res)

        elif choice == "5. Показать вакансии с зарплатой выше средней":
            res = db_manager.get_vacancies_with_higher_salary()
            cli.display_db_results(res)

        elif choice == "6. Показать вакансии, содержащие ключевое слово в названии":
            keyword = input("Введите ключевое слово для отбора: ")
            res = db_manager.get_vacancies_with_keyword(keyword)
            cli.display_db_results(res)

        elif choice == "7. Выход":
            return 0


if __name__ == "__main__":
    main()
