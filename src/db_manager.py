from src.storage import DBStorage


class DBManager:
    def __init__(self):
        DBStorage.initialize_database()
        self.db = DBStorage()

    def get_companies_and_vacancies_count():
        pass

    def get_all_vacancies():
        pass

    def get_avg_salary():
        pass

    def get_vacancies_with_higher_salary():
        pass

    def get_vacancies_with_keyword():
        pass

if __name__ == "__main__":
    db_manager = DBManager()