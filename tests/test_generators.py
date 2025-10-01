import pytest

from src.generators import (filter_by_currency,
                            transaction_descriptions,
                            card_number_generator)

@pytest.fixture
def transactions():
    return (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)

def test_filter_by_currency_usd(transactions):
    usd_gen = filter_by_currency(transactions, "USD")
    usd_list = list(usd_gen)

    assert len(usd_list) == 3
    for tr in usd_list:
        assert tr["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_rub(transactions):
    rub_gen = filter_by_currency(transactions, "RUB")
    rub_list = list(rub_gen)

    assert len(rub_list) == 2
    for tr in rub_list:
        assert tr["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_none(transactions):
    gbp_gen = filter_by_currency(transactions, "GBP")
    gbp_list = list(gbp_gen)

    assert gbp_list == []
    
    
def test_transaction_descriptions(transactions):
    gen = transaction_descriptions(transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"
    assert next(gen) == "Перевод организации"

    try:
        next(gen)
        assert False, "Должен был возникнуть StopIteration"
    except StopIteration:
        pass
