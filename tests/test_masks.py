import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_get_mask_card_number_various(card_number, expected):
    """Тест валидных 16-значных номеров карт"""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_format_correctness():
    """Тест правильности формата маски"""
    result = get_mask_card_number(1234567890123456)
    parts = result.split()
    assert len(parts) == 4  # Должно быть 4 группы
    assert parts[0] == "1234"  # Первые 4 цифры
    assert parts[1] == "56**"  # Следующие 2 цифры + **
    assert parts[2] == "****"  # Звездочки
    assert parts[3] == "3456"  # Последние 4 цифры


@pytest.mark.parametrize(
    "invalid_type",
    [
        "1234567890123456",  # строка
        "0012345678901234",  # строка с нулями
        1234567890123456.0,  # float
        [1234567890123456],  # список
        {"card": 1234567890123456},  # словарь
        None,  # None
        True,  # bool
    ],
)
def test_get_mask_card_number_invalid_input_types(invalid_type):
    """Тест на неверный тип входных данных"""
    with pytest.raises(TypeError) as exc_info:
        get_mask_card_number(invalid_type)
    assert str(exc_info.value) == "Номер карты должен быть целым числом"


@pytest.mark.parametrize(
    "invalid_length",
    [
        0,  # 1 число
        1234567,  # 7 цифр
        123456789012345,  # 15 цифр
        12345678901234567890,  # 20 цифр
    ],
)
def test_get_mask_card_nuber_invalid_length(invalid_length):
    """Тест на не верную длину номера карты"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_length)
    assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"


# ------------get_mask_account--------------


@pytest.mark.parametrize(
    "account_number, expected",
    [
        (12345678901234567890, "**7890"),
        (11112222333344445555, "**5555"),
        (99998888777766664444, "**4444"),
    ],
)
def test_get_mask_account_various(account_number, expected):
    """Тест валидных 20-значных номеров счета"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_type",
    [
        "1234567890123456",  # строка
        "0012345678901234",  # строка с нулями
        1234567890123456.0,  # float
        [1234567890123456],  # список
        {"card": 1234567890123456},  # словарь
        None,  # None
        True,  # bool
    ],
)
def test_get_mask_account_invalid_input_types(invalid_type):
    """Тест на неверный тип входных данных"""
    with pytest.raises(TypeError) as exc_info:
        get_mask_account(invalid_type)
    assert str(exc_info.value) == "Номер счета должен быть целым числом"


@pytest.mark.parametrize(
    "invalid_length",
    [
        0,  # 1 цифра
        1234567,  # 7 цифр
        123456789012345,  # 15 цифр
        1234567890123456789,  # 19 цифр
    ],
)
def test_get_mask_account_invalid_length(invalid_length):
    """Тест на не верную длину номера счета"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_length)
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"
