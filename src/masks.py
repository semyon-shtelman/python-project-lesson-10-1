def get_mask_card_number(card_number: int) -> str:
    """Возвращает маску номера карты в формате
    XXXX XX** **** XXXX, где X — это цифра номера"""
    number_str = str(card_number)
    return f"{number_str[:4]} {number_str[4:6]}{'**'} {'****'} {number_str[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Возвращает маску номера счета в формате
    **XXXX, где X — это цифра номера"""
    number_str = str(account_number)
    return f"{'**'}{number_str[-4:]}"
