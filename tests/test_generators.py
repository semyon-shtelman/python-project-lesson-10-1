import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# -------------------- TESTS: filter_by_currency --------------------


@pytest.mark.parametrize(
    "currency_code, expected",
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(currency_code, expected, transactions):
    """
    Проверяет, что filter_by_currency возвращает только те транзакции,
    у которых код валюты совпадает с переданным.
    """
    result = list(filter_by_currency(transactions, currency_code))
    result_ids = [item["id"] for item in result]
    assert result_ids == expected


# -------------------- TESTS: transaction_descriptions --------------------


def test_transaction_descriptions_basic(transactions):
    gen = transaction_descriptions(transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"
    assert next(gen) == "Перевод организации"

    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {"id": 1, "description": "Перевод"},
                {"id": 2, "description": "Пополнение"},
                {"id": 3, "description": "Снятие"},
            ],
            ["Перевод", "Пополнение", "Снятие"],
        ),
        ([{"id": 1, "description": "Перевод"}, {"id": 2}, {"id": 3, "description": "Снятие"}], ["Перевод", "Снятие"]),
        ([], []),
        ([{"id": 1}, {"id": 2}, {"id": 3}], []),
    ],
)
def test_transaction_descriptions(transactions, expected):
    """
    Проверяет работу transaction_descriptions на разных наборах входных данных:
    - все элементы с описанием
    - часть элементов без описания
    - пустой список
    - список без описаний
    """
    gen = transaction_descriptions(transactions)
    result = list(gen)
    assert result == expected


# -------------------- TESTS: card_number_generator --------------------


def test_card_number_generator_count():
    """
    Проверяет, что card_number_generator возвращает правильное количество номеров
    при заданном диапазоне.
    """
    gen = card_number_generator(1, 5)
    result = list(gen)
    assert len(result) == 5


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (7, 7, ["0000 0000 0000 0007"]),
        (98, 100, ["0000 0000 0000 0098", "0000 0000 0000 0099", "0000 0000 0000 0100"]),
    ],
)
def test_card_number_generator_param(start, stop, expected):
    """
    Проверяет card_number_generator с параметризацией:
    - диапазон из нескольких элементов
    - диапазон из одного элемента
    - диапазон с переходом через десятки/сотни
    """
    gen = card_number_generator(start, stop)
    result = list(gen)
    assert result == expected
