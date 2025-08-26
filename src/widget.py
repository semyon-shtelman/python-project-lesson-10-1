from masks import get_mask_card_number, get_mask_account


def mask_account_card(account_card: str) -> str:
    """Возвращает строку с замаскированным номером.
     Для карт и счетов используется разные типы маскировки"""
    account_card_number = "".join([i for i in account_card if i.isdigit()])
    if len(account_card_number) <= 16:
        return f"{account_card[:-16]}{get_mask_card_number(int(account_card_number))}"
    else:
        return f"{account_card[:-20]}{get_mask_account(int(account_card_number))}"


def get_date(date: str) -> str:
    """Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"""
    date = date[:10]
    return f"{date[-2:]}.{date[5:7]}.{date[:4]}"
