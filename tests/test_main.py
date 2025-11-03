from unittest.mock import MagicMock, patch

from src.main import main


@patch("src.main.DBManager")
@patch("src.main.CLI")
@patch("src.main.HHClient")
@patch("src.main.JSONStorage")
def test_main_exit(
    mock_storage_cls: MagicMock,
    mock_hhclient_cls: MagicMock,
    mock_cli_cls: MagicMock,
    mock_dbmanager_cls: MagicMock,
) -> None:
    # Настраиваем CLI
    mock_cli = MagicMock()
    mock_cli.show_menu.side_effect = ["7. Выход"]  # имитируем сразу выход
    mock_cli_cls.return_value = mock_cli

    # Настраиваем HHClient и JSONStorage (не используются, но нужны)
    mock_hhclient = MagicMock()
    mock_hhclient.region_names = {"Москва": 1}
    mock_hhclient_cls.return_value = mock_hhclient
    mock_storage_cls.return_value = MagicMock()

    # Настраиваем DBManager
    mock_dbmanager = MagicMock()
    mock_dbmanager.get_companies_id.return_value = [15478, 1122462]
    mock_dbmanager_cls.return_value = mock_dbmanager

    # Запускаем main()
    result = main()

    # Проверяем, что вернулся 0
    assert result == 0

    # Проверяем, что меню было показано ровно 1 раз
    mock_cli.show_menu.assert_called_once()


@patch("src.main.DBManager")
@patch("src.main.JSONStorage")
@patch("src.main.HHClient")
@patch("src.main.CLI")
def test_main_show_saved(
    mock_cli_cls: MagicMock,
    mock_hhclient_cls: MagicMock,
    mock_storage_cls: MagicMock,
    mock_dbmanager_cls: MagicMock,
) -> None:
    """Тест проверяет, что main() корректно работает с опцией показа сохраненных вакансий"""
    mock_cli = MagicMock()
    mock_cli.show_menu.side_effect = ["1. Показать сохраненные вакансии", "7. Выход"]
    mock_cli_cls.return_value = mock_cli

    mock_storage = MagicMock()
    mock_storage_cls.return_value = mock_storage

    mock_hhclient = MagicMock()
    mock_hhclient.region_names = {"Москва": 1}
    mock_hhclient_cls.return_value = mock_hhclient

    mock_dbmanager = MagicMock()
    mock_dbmanager.get_companies_id.return_value = [15478, 1122462]
    mock_dbmanager.get_all_vacancies.return_value = []
    mock_dbmanager_cls.return_value = mock_dbmanager

    result = main()

    # Проверяем, что main завершился корректно
    assert result == 0
    # Проверяем, что меню было показано
    assert mock_cli.show_menu.call_count == 2
    # Проверяем, что display_db_results был вызван с результатами из БД
    mock_cli.display_db_results.assert_called_once_with([])
