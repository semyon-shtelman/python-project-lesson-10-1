from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.csv_excel_manager import get_transactions_csv, get_transactions_excel


@pytest.fixture
def mock_data():
    return [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
    ]


def test_get_transaction_csv_success(mock_data):
    """Тест успешного чтения CSV файла"""

    with patch("builtins.open", mock_open()) as mock_file, patch("csv.DictReader") as mock_dict_reader:

        mock_dict_reader.return_value = mock_data

        result = get_transactions_csv("test.csv")

        assert result == mock_data
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert len(result) == 2

        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")


def test_get_transaction_csv_file_not_found():
    """Тест обработки отсутствующего файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_transactions_csv("nonexistent.csv")

        assert result == []
        assert len(result) == 0


def test_get_transaction_csv_empty_file():
    """Тест чтения пустого CSV файла"""
    with patch("builtins.open", mock_open()), patch("csv.DictReader") as mock_dict_reader:

        mock_dict_reader.return_value = []

        result = get_transactions_csv("empty.csv")

        assert result == []
        assert len(result) == 0


def test_get_transaction_csv_general_error():
    """Тест обработки общей ошибки"""
    with patch("builtins.open", side_effect=Exception("Read error")):
        result = get_transactions_csv("corrupted.csv")

        assert result == []


def test_get_transactions_excel_success(mock_data):
    """Тест успешного чтения Excel файла"""

    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = MagicMock()
        mock_df.to_dict.return_value = mock_data
        mock_read_excel.return_value = mock_df

        result = get_transactions_excel("test.xlsx")

        assert result == mock_data
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert len(result) == 2

        mock_read_excel.assert_called_once_with("test.xlsx")


def test_get_transactions_excel_file_not_found():
    """Тест обработки отсутствующего Excel файла"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError()):
        result = get_transactions_excel("nonexistent.xlsx")

        assert result == []


def test_get_transactions_excel_general_error():
    """Тест обработки общей ошибки Excel"""
    with patch("pandas.read_excel", side_effect=Exception("Excel read error")):
        result = get_transactions_excel("corrupted.xlsx")

        assert result == []


def test_get_transactions_excel_empty_data():
    """Тест чтения пустого Excel файла"""
    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = MagicMock()
        mock_df.to_dict.return_value = []
        mock_read_excel.return_value = mock_df

        result = get_transactions_excel("empty.xlsx")

        assert result == []
        assert len(result) == 0
