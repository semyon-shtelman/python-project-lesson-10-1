import json
from unittest.mock import mock_open, patch

from src.utils import get_transaction_amount, open_json_file


def test_open_json_file_success_list():
    """Тест успешного чтения JSON файла со списком транзакций"""
    test_data = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02", "amount": 200},
    ]

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = open_json_file("transactions.json")

        assert result == test_data
        assert isinstance(result, list)
        assert len(result) == 2


def test_open_json_file_success_empty_list():
    """Тест успешного чтения JSON файла с пустым списком"""
    test_data = []

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = open_json_file("transactions.json")

        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0


def test_open_json_file_not_list_returns_empty():
    """Тест когда JSON содержит не список, а словарь"""
    test_data = {"id": 1, "amount": 100}  # словарь вместо списка

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = open_json_file("transactions.json")

        assert result == []
        assert isinstance(result, list)


def test_open_json_file_invalid_json():
    """Тест с невалидным JSON"""
    invalid_json = "this is not valid json {"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        result = open_json_file("transactions.json")

        assert result == []
        assert isinstance(result, list)


def test_open_json_file_file_not_found():
    """Тест когда файл не существует"""
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        result = open_json_file("nonexistent.json")

        assert result == []
        assert isinstance(result, list)


# -----------get_transaction_amount------------


def test_get_transaction_amount_rub_currency():
    """Тест успешного возврата суммы транзакции в рублях"""
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    assert get_transaction_amount(transaction) == "100.50"


def test_get_transaction_amount_api():
    """Тест обращения к API если валюта не в рублях"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    with patch("src.utils.currency_conversion") as mock_conv:
        mock_conv.return_value = 8138.00
        result = get_transaction_amount(transaction)
        assert result == 8138.00
        mock_conv.assert_called_with(transaction)


def test_get_transaction_amount_no_transaction():
    """Тест отсутствия транзакций"""
    assert get_transaction_amount({}) == 0.0
    assert get_transaction_amount({"other": "data"}) == 0.0


def test_get_transaction_amount_conversion_fails():
    """Тест не успешной конвертации валюты"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    with patch("src.utils.currency_conversion") as mock_conv:
        mock_conv.return_value = None
        assert get_transaction_amount(transaction) == 0.0
