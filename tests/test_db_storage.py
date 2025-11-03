"""Тесты для DBStorage"""


from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.storage import DBStorage


@pytest.fixture
def mock_config_file() -> str:
    """Моковый конфиг файл"""
    return """[postgresql]
host=localhost
database=parser_db
user=postgres
password=test_password

[postgresql_service]
host=localhost
database=postgres
user=postgres
password=test_password
"""


def test_get_config(mock_config_file: str) -> None:
    """Тест чтения конфигурации"""
    with patch("builtins.open", mock_open(read_data=mock_config_file)):
        with patch("os.path.dirname", return_value="/fake/path"):
            config = DBStorage._get_config("database.ini", "postgresql")

            assert config["host"] == "localhost"
            assert config["database"] == "parser_db"
            assert config["user"] == "postgres"
            assert config["password"] == "test_password"


def test_get_config_missing_section() -> None:
    """Тест чтения конфигурации с отсутствующей секцией"""
    mock_content = "[other_section]\nkey=value"

    with patch("builtins.open", mock_open(read_data=mock_content)):
        with patch("os.path.dirname", return_value="/fake/path"):
            with pytest.raises(Exception, match="Секция параметров подключения к базе данных не найдена"):
                DBStorage._get_config("database.ini", "postgresql")


def test_init() -> None:
    """Тест инициализации DBStorage"""
    with patch.object(DBStorage, "_get_config") as mock_get_config:
        mock_get_config.return_value = {
            "host": "localhost",
            "database": "parser_db",
            "user": "postgres",
            "password": "test",
        }

        db_storage = DBStorage()

        assert db_storage.connection_params["host"] == "localhost"
        assert db_storage.connection_params["database"] == "parser_db"
        mock_get_config.assert_called_once_with("database.ini", "postgresql")


@patch("src.storage.psycopg2.connect")
def test_get_connection(mock_connect: MagicMock) -> None:
    """Тест создания соединения с БД"""
    with patch.object(DBStorage, "_get_config") as mock_get_config:
        mock_get_config.return_value = {
            "host": "localhost",
            "database": "parser_db",
            "user": "postgres",
            "password": "test",
        }

        db_storage = DBStorage()
        conn = db_storage._get_connection()

        mock_connect.assert_called_once_with(host="localhost", database="parser_db", user="postgres", password="test")


@patch("src.storage.psycopg2.connect")
def test_execute_query(mock_connect: MagicMock) -> None:
    """Тест выполнения INSERT/UPDATE/DELETE запроса"""
    # Setup
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    with patch.object(DBStorage, "_get_config") as mock_get_config:
        mock_get_config.return_value = {"host": "localhost", "database": "test_db", "user": "user", "password": "pass"}

        db_storage = DBStorage()

        # Act
        result = db_storage.execute_query("INSERT INTO test VALUES (%s)", (1,))

        # Assert
        assert result == 1
        mock_cursor.execute.assert_called_once_with("INSERT INTO test VALUES (%s)", (1,))
        mock_connection.commit.assert_called_once()


@patch("src.storage.psycopg2.connect")
def test_fetch_query(mock_connect: MagicMock) -> None:
    """Тест выполнения SELECT запроса"""
    # Setup
    expected_result = [{"id": 1, "name": "Test"}]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = expected_result
    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    with patch.object(DBStorage, "_get_config") as mock_get_config:
        mock_get_config.return_value = {"host": "localhost", "database": "test_db", "user": "user", "password": "pass"}

        db_storage = DBStorage()

        # Act
        result = db_storage.fetch_query("SELECT * FROM test WHERE id = %s", (1,))

        # Assert
        assert result == expected_result
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test WHERE id = %s", (1,))


@patch("src.storage.psycopg2.connect")
def test_initialize_database(mock_connect: MagicMock) -> None:
    """Тест инициализации базы данных"""
    # Setup mocks
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # БД не существует
    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    with patch.object(DBStorage, "_get_config") as mock_get_config:
        mock_get_config.return_value = {
            "host": "localhost",
            "database": "postgres",
            "user": "user",
            "password": "pass",
        }

        with patch.object(DBStorage, "_create_tables") as mock_create_tables:
            # Act
            DBStorage.initialize_database()

            # Assert - должны были вызваться методы создания БД и таблиц
            assert mock_cursor.execute.call_count >= 2  # Проверка существования + создание БД/таблиц


def test_create_tables() -> None:
    """Тест создания таблиц"""
    mock_cursor = MagicMock()

    # Act
    DBStorage._create_tables(mock_cursor)

    # Assert
    mock_cursor.execute.assert_called_once()
    # Проверяем, что SQL содержит CREATE TABLE
    sql_call = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE companies" in sql_call
    assert "CREATE TABLE vacancies" in sql_call
    assert "INSERT INTO companies" in sql_call
