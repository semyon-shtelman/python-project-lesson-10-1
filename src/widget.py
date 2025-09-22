from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Возвращает строку с замаскированным номером.
    Для карт и счетов используется разные типы маскировки"""
    if not isinstance(account_card, str) or not account_card.strip():
        raise ValueError("Пустая строка")

    account_card_number = "".join([i for i in account_card if i.isdigit()])
    account_card_name = "".join([i for i in account_card if not i.isdigit()])

    if not account_card_name:
        raise ValueError("Не указан тип платежной системы")

    elif len(account_card_number) == 16:
        return f"{account_card_name}{get_mask_card_number(int(account_card_number))}"

    elif len(account_card_number) == 20:
        return f"{account_card_name}{get_mask_account(int(account_card_number))}"
    else:
        raise ValueError("Некорректная длина номера")


def get_date(date: str) -> str:
    """Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"""

    if not isinstance(date, str):
        raise ValueError
    try:
        date_time = datetime.fromisoformat(date)
    except ValueError:
        raise ValueError("Некорректная дата")
    return date_time.strftime("%d.%m.%Y")
