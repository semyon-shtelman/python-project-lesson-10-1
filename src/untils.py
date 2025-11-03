import json
from typing import Any


def open_json_file(path: str) -> list[dict[str, Any]]:
    """ Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            try:
                data_transaction = json.load(f)
                if isinstance(data_transaction, list):
                    return data_transaction
                else:
                    return []
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []

