def get_mask_card_number(card_number: int) -> str:
    """Возвращает маску номера карты в формате
    XXXX XX** **** XXXX, где X — это цифра номера"""
    if type(card_number) is not int:
        raise TypeError("Номер карты должен быть целым числом")

    number_str = str(card_number)

    if len(number_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{number_str[:4]} {number_str[4:6]}** **** {number_str[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Возвращает маску номера счета в формате
    **XXXX, где X — это цифра номера"""

    if type(account_number) is not int:
        raise TypeError("Номер счета должен быть целым числом")

    number_str = str(account_number)

    if len(number_str) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    return f"{'**'}{number_str[-4:]}"
