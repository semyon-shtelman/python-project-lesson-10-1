import sys

from src.csv_excel_manager import get_transactions_csv, get_transactions_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import open_json_file
from src.widget import get_date, mask_account_card


def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Шаг 1: Выбор файла с транзакциями
    transactions = select_and_load_transactions()
    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        return


    # Шаг 2: Фильтрация по статусу
    filtered_transactions = filter_by_status_interactive(transactions)
    if not filtered_transactions:
        print("Не найдено ни одной транзакции с выбранным статусом.")
        return

    # Шаг 3: Дополнительные фильтры и сортировка
    final_transactions = apply_additional_filters(filtered_transactions)

    # Шаг 4: Вывод результатов
    display_transactions(final_transactions)


def select_and_load_transactions() -> list[dict]:
    """Выбор и загрузка транзакций из файла."""

    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")
        print("4. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return open_json_file("../data/operations.json")
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            return get_transactions_csv("../data/transactions.csv")
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return get_transactions_excel("../data/transactions_excel.xlsx")
        elif choice == "4":
            print("До свидания!")
            sys.exit(0)
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 4.")


def filter_by_status_interactive(transactions: list[dict]) -> list[dict]:
    """Фильтрация транзакций по статусу."""

    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(available_statuses)}")

        status = input("Статус: ").strip().upper()

        if status in available_statuses:
            try:
                filtered = filter_by_state(transactions, status)
                print(f"Операции отфильтрованы по статусу '{status}'")
                return filtered
            except Exception:
                return []
        else:
            print(f"Статус операции '{status}' недоступен.")


def apply_additional_filters(transactions: list[dict]) -> list[dict]:
    """Применение дополнительных фильтров и сортировки."""

    result_transactions = transactions.copy()

    # Сортировка по дате
    result_transactions = apply_date_sorting(result_transactions)

    # Фильтрация по валюте
    result_transactions = apply_currency_filter(result_transactions)

    # Фильтрация по описанию
    result_transactions = apply_description_filter(result_transactions)

    return result_transactions


def apply_date_sorting(transactions: list[dict]) -> list[dict]:
    """Применение сортировки по дате."""

    sort_choice = input("\nОтсортировать операции по дате? (Да/Нет): ").strip().lower()

    if sort_choice in ["да", "yes"]:
        order_choice = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

        if "возр" in order_choice:
            return sort_by_date(transactions)
        else:
            return sort_by_date(transactions, reverse=False)

    return transactions


def apply_currency_filter(transactions: list[dict]) -> list[dict]:
    """Фильтрация по валюте."""

    currency_choice = input("\nВыводить только рублевые транзакции? (Да/Нет): ").strip().lower()

    if currency_choice in ["да", "yes"]:
        return list(filter_by_currency(transactions, "RUB"))

    return transactions


def apply_description_filter(transactions: list[dict]) -> list[dict]:
    """Фильтрация по описанию."""
    filter_choice = (
        input("\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").strip().lower()
    )

    if filter_choice in ["да", "yes"]:
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            return process_bank_search(transactions, search_word)

    return transactions


def display_transactions(transactions: list[dict]) -> None:
    """Отображение отфильтрованных транзакций."""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        formatted = format_transaction_for_display(transaction)
        print(formatted)
        print()


def format_transaction_for_display(transaction: dict) -> str:
    """Форматирование транзакции для отображения."""
    date = get_date(transaction.get("date", "Нет даты"))
    description = transaction.get("description", "Нет описания")

    amount = transaction.get("amount", 0)
    amount = round(float(amount))
    if not amount:
        amount = transaction.get("operationAmount").get("amount", 0)
        amount = round(float(amount))

    currency = transaction.get("currency_code", "")
    if not currency:
        currency = transaction.get("operationAmount").get("currency").get("code", "")

    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    def from_to() -> str:
        """Формирует строку с выводом откуда и куда был совершён перевод"""
        if from_account and to_account:
            try:
                from_formatted = mask_account_card(from_account)
                to_formatted = mask_account_card(to_account)
                return f"{from_formatted} -> {to_formatted}"
            except Exception:
                return ""
        elif to_account:
            try:
                to_formatted = mask_account_card(to_account)
                return f"{to_formatted}"
            except Exception:
                return ""
        return ""

    return f"{date} {description}\n{from_to()}\nСумма: {amount} {currency}"


if __name__ == "__main__":
    main()
