import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "banking_data, extended",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card_valid_data(banking_data, extended):
    assert mask_account_card(banking_data) == extended


@pytest.mark.parametrize(
    "invalid_data",
    [
        "Just text",  # нет цифр
        "",  # пустая строка
        "1234567812345678",  # только цифры
        "Maestro",  # только текст
        "Maestro 1234abcd5678efgh",  # буквы вместо цифр
    ],
)
def test_mask_account_card_empty_line(invalid_data):
    with pytest.raises(ValueError):
        assert mask_account_card(invalid_data)


# ---------------get_date--------------------


@pytest.mark.parametrize(
    "date, expected",
    [
        # Стандартные форматы
        ("2024-03-15T10:30:00", "15.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2024-01-01T00:00:00", "01.01.2024"),
    ],
)
def test_get_date_valid_date(date, expected):
    """Тестирование правильности преобразования даты"""
    assert get_date(date) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "",  # пустая строка
        "   ",  # только пробелы
        "invalid_date",  # не дата
        "2024-02-30",  # несуществующая дата
        "2024-13-15T10:30:00",  # не существующий месяц
        "2024-03-32T10:30:00",  # не существующий день
        None,  # вообще не строка
    ],
)
def test_get_date_invalid(invalid_date):
    with pytest.raises(ValueError):
        get_date(invalid_date)
