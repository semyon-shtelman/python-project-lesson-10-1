from typing import Any


def filter_by_state(transactions: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список транзакций по статусу.

    :param transactions: Список словарей с транзакциями
    :param state: Статус транзакций для фильтрации. По умолчанию "EXECUTED"

    :return: Новый список словарей, содержащий только транзакции с указанным статусом.
    :raises ValueError: Если подходящих транзакций не найдено
                        или входной список пуст.
    """
    transaction = [item for item in transactions if item.get("state") == state]
    if transaction:
        return transaction
    else:
        raise ValueError("Подходящих транзакций не найдено " "или входной список пуст.")


def sort_by_date(transactions: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует список транзакций по дате.

    :param transactions: Список словарей с транзакциями
    :param reverse: Если True(по умолчанию) - сортировка от новых к старым,
    если False - от старых к новым

    :return: Новый список транзакций, отсортированных по дате.
    :raises KeyError: Если в какой-либо транзакции отсутствует ключ 'date'.
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
