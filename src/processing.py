from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по статусу.

    :param transactions: Список словарей с транзакциями
    :param state: Статус транзакций для фильтрации. По умолчанию "EXECUTED"

    :return: Новый список словарей, содержащий только транзакции с указанным статусом.
    Если подходящих транзакций нет, возвращается пустой список.
    """
    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список транзакций по дате.

    :param transactions: Список словарей с транзакциями
    :param reverse: Если True(по умолчанию) - сортировка от новых к старым,
    если False - от старых к новым

    :return: Отсортированный список транзакций по дате. Если подходящих транзакций нет,
    KeyError: Если в какой-либо транзакции отсутствует ключ 'date'.
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
