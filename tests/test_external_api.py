import sys
from unittest.mock import Mock, patch

import pytest

sys.path.append("src")
from src.external_api import currency_conversion


@pytest.fixture
def data_transaction():
    return {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
    }


@patch("external_api.requests.get")
def test_currency_conversion(mock_requests_get, data_transaction):
    """Тест успешной конвертации"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 8138.00}
    mock_requests_get.return_value = mock_response

    result = currency_conversion(data_transaction)

    assert result == 8138.00
    mock_requests_get.assert_called_once()


@patch("external_api.requests.get")
def test_currency_conversion_api_error_status(mock_requests_get, data_transaction):
    """Тест ошибки на стороне сервера"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    result = currency_conversion(data_transaction)

    assert result is None


@patch("external_api.requests.get")
def test_missing_result_field(mock_requests_get, data_transaction):
    """Нет нужного ключа(result)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}  # Нет result
    mock_requests_get.return_value = mock_response

    result = currency_conversion(data_transaction)

    assert result is None
