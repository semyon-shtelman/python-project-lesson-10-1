import json
from typing import Any

from requests import Response

from src.external_api import currency_conversion


def open_json_file(path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            try:
                data_transactions = json.load(f)
                if isinstance(data_transactions, list):
                    return data_transactions
                else:
                    return []
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []


def get_transaction_amount(transaction: dict[str, Any]) -> float | None | Response | Any:
    """Возвращает сумму транзакции в рублях."""

    try:
        operation_amount = transaction.get("operationAmount", {})
        if not operation_amount:
            return 0.0

        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")
        amount_value = operation_amount.get("amount")

        if not currency_code or not amount_value:
            return 0.0

        if currency_code == "RUB":
            return amount_value

        converted_amount = currency_conversion(amount_value, currency_code)

        if converted_amount is not None:
            return converted_amount
        else:
            return 0.0

    except (ValueError, TypeError):
        return 0.0
    except Exception:
        return 0.0
