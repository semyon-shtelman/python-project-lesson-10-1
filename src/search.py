import re
from collections import defaultdict


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует список банковских операций по наличию строки поиска в описании."""

    if not search or not data:
        return []

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
    except re.error:
        return []

    filtered_data = []

    for operation in data:
        if operation.get("description") and pattern.search(operation["description"]):
            filtered_data.append(operation)

    return filtered_data


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по заданным категориям на основе описания."""
    if not data or not categories:
        return {}

    category_count = defaultdict(int)

    patterns = {category: re.compile(r"\b" + re.escape(category) + r"\b", re.IGNORECASE) for category in categories}

    for operation in data:
        description = operation.get("description", "")
        if not description:
            continue

        for category, pattern in patterns.items():
            if pattern.search(description):
                category_count[category] += 1
    return dict(category_count)
