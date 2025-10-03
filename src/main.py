import os

from loguru import logger

from src.vacancy_api import HHClient

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "main.log")
logger.add(sink=log_file, level="DEBUG")


def main():
    hh = HHClient(text="Разработчик")
    vacancies_list = hh.get_vacancies()
    logger.debug(f"Получено вакансий количество: {len(vacancies_list)}")

    hh.get_areas()


if __name__ == "__main__":
    main()
