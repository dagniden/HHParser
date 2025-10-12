from unittest.mock import MagicMock, patch

from src.main import main


@patch("src.main.CLI")
@patch("src.main.HHClient")
@patch("src.main.JSONStorage")
def test_main_exit(mock_storage_cls: MagicMock, mock_hhclient_cls: MagicMock, mock_cli_cls: MagicMock) -> None:
    # Настраиваем CLI
    mock_cli = MagicMock()
    mock_cli.show_menu.side_effect = ["3. Выход"]  # имитируем сразу выход
    mock_cli_cls.return_value = mock_cli

    # Настраиваем HHClient и JSONStorage (не используются, но нужны)
    mock_hhclient_cls.return_value = MagicMock()
    mock_storage_cls.return_value = MagicMock()

    # Запускаем main()
    result = main()

    # Проверяем, что вернулся 0
    assert result == 0

    # Проверяем, что меню было показано ровно 1 раз
    mock_cli.show_menu.assert_called_once()


@patch("src.main.CLI")
@patch("src.main.HHClient")
@patch("src.main.JSONStorage")
def test_main_show_saved(mock_storage_cls: MagicMock, mock_hhclient_cls: MagicMock, mock_cli_cls: MagicMock) -> None:
    mock_cli = MagicMock()
    mock_cli.show_menu.side_effect = ["1. Показать сохраненные вакансии", "3. Выход"]
    mock_cli.ask_top_n.return_value = None
    mock_cli.display_vacancies.return_value = None
    mock_cli_cls.return_value = mock_cli

    mock_storage = MagicMock()
    mock_storage.read_as_vacancy_list.return_value = MagicMock(vacancies=[])
    mock_storage_cls.return_value = mock_storage

    mock_hhclient_cls.return_value = MagicMock()

    main()

    mock_storage.read_as_vacancy_list.assert_called_once()
    mock_cli.display_vacancies.assert_called_once()
