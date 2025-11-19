import pytest
from src.search import process_bank_search, process_bank_operations


def test_process_bank_search_empty_data():
    """Тест с пустым списком данных"""
    result = process_bank_search([], "test")
    assert result == []


def test_process_bank_search_empty_search_string():
    """Тест с пустой строкой поиска"""
    data = [{"description": "test operation"}]
    result = process_bank_search(data, "")
    assert result == []


def test_process_bank_search_both_empty():
    """Тест с пустыми данными и строкой поиска"""
    result = process_bank_search([], "")
    assert result == []


def test_process_bank_search_successful():
    """Тест успешного поиска"""
    data = [
        {"description": "Payment for grocery store"},
        {"description": "Salary transfer"},
        {"description": "Grocery shopping"}
    ]
    result = process_bank_search(data, "grocery")
    assert len(result) == 2
    assert result[0]["description"] == "Payment for grocery store"
    assert result[1]["description"] == "Grocery shopping"


def test_process_bank_search_case_insensitive():
    """Тест поиска без учета регистра"""
    data = [
        {"description": "Payment for GROCERY store"},
        {"description": "Salary transfer"},
        {"description": "grocery shopping"}
    ]
    result = process_bank_search(data, "GrocerY")
    assert len(result) == 2
    assert result[0]["description"] == "Payment for GROCERY store"
    assert result[1]["description"] == "grocery shopping"


def test_process_bank_search_partial_match():
    """Тест частичного совпадения (слово внутри другого слова)"""
    data = [
        {"description": "Payment for groceries"},  # "grocery" внутри "groceries"
        {"description": "Grocery shopping"},  # точное совпадение
        {"description": "Salary transfer"}
    ]
    result = process_bank_search(data, "grocery")
    # Ожидаем только точные совпадения, не частичные внутри слов
    assert len(result) == 1
    assert result[0]["description"] == "Grocery shopping"


def test_process_bank_search_no_description_field():
    """Тест с операциями без поля description"""
    data = [
        {"amount": 100},
        {"description": "Valid operation"},
        {"other_field": "value"}
    ]
    result = process_bank_search(data, "valid")
    assert len(result) == 1
    assert result[0]["description"] == "Valid operation"


def test_process_bank_search_special_characters():
    """Тест с специальными символами в строке поиска"""
    data = [
        {"description": "Payment (special) for items"},
        {"description": "Regular payment"}
    ]
    result = process_bank_search(data, "(special)")
    assert len(result) == 1
    assert result[0]["description"] == "Payment (special) for items"


def test_process_bank_search_no_matches():
    """Тест когда нет совпадений"""
    data = [
        {"description": "Payment for groceries"},
        {"description": "Salary transfer"}
    ]
    result = process_bank_search(data, "restaurant")
    assert result == []


def test_process_bank_operations_empty_data():
    """Тест с пустым списком данных"""
    result = process_bank_operations([], ["food", "transport"])
    assert result == {}


def test_process_bank_operations_empty_categories():
    """Тест с пустым списком категорий"""
    data = [{"description": "Payment for food"}]
    result = process_bank_operations(data, [])
    assert result == {}


def test_process_bank_operations_both_empty():
    """Тест с пустыми данными и категориями"""
    result = process_bank_operations([], [])
    assert result == {}


def test_process_bank_operations_successful_count():
    """Тест успешного подсчета операций"""
    data = [
        {"description": "Payment for food at restaurant"},
        {"description": "Transport taxi payment"},
        {"description": "Food delivery service"},
        {"description": "Salary payment"}
    ]
    categories = ["food", "transport", "salary"]
    result = process_bank_operations(data, categories)

    assert result == {"food": 2, "transport": 1, "salary": 1}


def test_process_bank_operations_case_insensitive():
    """Тест подсчета без учета регистра"""
    data = [
        {"description": "Payment for FOOD"},
        {"description": "Transport payment"},
        {"description": "food delivery"}
    ]
    categories = ["Food", "TRANSPORT"]
    result = process_bank_operations(data, categories)

    assert result == {"Food": 2, "TRANSPORT": 1}


def test_process_bank_operations_whole_word_matching():
    """Тест поиска целых слов"""
    data = [
        {"description": "Fast food restaurant"},
        {"description": "Food delivery"},
        {"description": "Fastfood chain"}  # Не должно совпасть с "food"
    ]
    categories = ["food"]
    result = process_bank_operations(data, categories)

    assert result == {"food": 2}  # Только первые два


def test_process_bank_operations_no_description():
    """Тест с операциями без описания"""
    data = [
        {"amount": 100},
        {"description": "Food payment"},
        {"other_field": "value"}
    ]
    categories = ["food"]
    result = process_bank_operations(data, categories)

    assert result == {"food": 1}


def test_process_bank_operations_multiple_matches():
    """Тест когда операция попадает в несколько категорий"""
    data = [
        {"description": "Food and transport payment"},
        {"description": "Transport for food delivery"}
    ]
    categories = ["food", "transport"]
    result = process_bank_operations(data, categories)

    assert result == {"food": 2, "transport": 2}


def test_process_bank_operations_no_matches():
    """Тест когда нет совпадений по категориям"""
    data = [
        {"description": "Payment for groceries"},
        {"description": "Salary transfer"}
    ]
    categories = ["restaurant", "entertainment"]
    result = process_bank_operations(data, categories)

    assert result == {"restaurant": 0, "entertainment": 0}



def test_process_bank_operations_empty_string_category():
    """Тест с пустой строкой в категориях"""
    data = [{"description": "Payment"}]
    categories = [""]
    result = process_bank_operations(data, categories)

    assert result == {"": 0}