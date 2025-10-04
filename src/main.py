import os
import timeit

from loguru import logger

from src.vacancy_api import HHClient

# Конфигурация логгера
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "main.log")
logger.add(sink=log_file, level="DEBUG")

data = [
    {
        "id": "113",
        "parent_id": None,
        "name": "Россия",
        "areas": [
            {
                "id": "1620",
                "parent_id": "113",
                "name": "Республика Марий Эл",
                "areas": [
                    {"id": "4228", "parent_id": "1620", "name": "Виловатово", "areas": [], "utc_offset": "+03:00"},
                    {"id": "1621", "parent_id": "1620", "name": "Волжск", "areas": [], "utc_offset": "+03:00"},
                    {"id": "1622", "parent_id": "1620", "name": "Звенигово", "areas": [], "utc_offset": "+03:00"},
                ],
            }
        ],
    }
]


def parse_regions(data):
    region_names = {}
    for item in data:
        region_names[item["name"]] = int(item["id"])

        if item["areas"]:
            children_names = parse_regions(item["areas"])
            region_names.update(children_names)

    return region_names


def main():

    hh = HHClient()
    vacancies_list = hh.fetch_vacancies("руководитель")
    logger.debug(f"Получено вакансий количество: {len(vacancies_list)}")

    # print(hh.region_names)

    elapsed_time = timeit.timeit(hh.fetch_regions, number=1)
    # print(hh.region_names)
    print(f"Время выполнения запроса 2: {elapsed_time} секунд")

    elapsed_time = timeit.timeit(hh.fetch_regions, number=1)
    print(f"Время выполнения запроса 3: {elapsed_time} секунд")


if __name__ == "__main__":
    main()
