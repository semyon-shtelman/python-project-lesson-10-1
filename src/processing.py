def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует транзакции по статусу выполнения"""
    return [item for item in transactions if item["state"] == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """Фильтрует транзакции по дате выполнения"""
    return sorted(transactions, key=lambda x: "".join([item for item in x["date"]]), reverse=reverse)
