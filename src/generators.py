from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency_code: str) -> Iterator[dict[str, Any]]:
    """
    Возвращает итератор по транзакциям, где код валюты совпадает с заданным.

    :param transactions: Список словарей с транзакциями
    :param currency_code: код валюты (например, "USD")
    :return: итератор по транзакциям
    """
    return (
        x for x in transactions if x.get("operationAmount", {}).get("currency", {}).get("code", "") == currency_code
    )


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.

    :param transactions: Список словарей с транзакциями
    :yield: строка с описанием операции
    """
    for x in transactions:
        description = x.get("description")
        if description is not None:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров карт в диапазоне [start, start].
    Каждый номер форматируется как '0000 0000 0000 000X'.
    """
    for num in range(start, stop + 1):
        card_number = ("0" * max(0, 16 - len(str(num)))) + str(num)
        formatted = " ".join(card_number[i:i + 4] for i in range(0, 16, 4))
        yield formatted
