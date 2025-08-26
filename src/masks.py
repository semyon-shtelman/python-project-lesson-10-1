def get_mask_card_number(card_number: int) -> str:
    """Возвращает маску номера карты в формате
    XXXX XX** **** XXXX, где X — это цифра номера"""
    card_number_str = str(card_number)
    replace_number = card_number_str[6:-4]
    formatted_text = card_number_str.replace(replace_number, "******")
    formatted_text = [formatted_text[i : i + 4] for i in range(0, len(formatted_text), 4)]
    return " ".join(formatted_text)


def get_mask_account(account_number: int) -> str:
    """Возвращает маску номера счета в формате
    **XXXX, где X — это цифра номера"""
    account_number_str = str(account_number)
    replace_number = account_number_str[:-4]
    formatted_text = account_number_str.replace(replace_number, "**")
    return formatted_text
