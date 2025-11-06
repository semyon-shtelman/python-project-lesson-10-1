import sys
from unittest.mock import Mock, patch

sys.path.append("src")
from src.external_api import currency_conversion


@patch("external_api.requests.get")
def test_currency_conversion(mock_requests_get):
    """Тест успешной конвертации"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 8138.00}
    mock_requests_get.return_value = mock_response

    result = currency_conversion(100, "USD")

    assert result == 8138.00
    mock_requests_get.assert_called_once()


@patch("external_api.requests.get")
def test_currency_conversion_api_error_status(mock_requests_get):
    """Тест ошибки на стороне сервера"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    result = currency_conversion(100, "USD")

    assert result is None


@patch("external_api.requests.get")
def test_missing_result_field(mock_requests_get):
    """Нет нужного ключа(result)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}  # Нет result
    mock_requests_get.return_value = mock_response

    result = currency_conversion(100, "USD")

    assert result is None
