import csv
import json
from typing import Any

import pandas as pd


def get_transactions_csv(csv_file_path: str) -> list[dict[str, Any]]:
    """
    Считывает финансовые операции из CSV файла и
    возвращает список словарей с транзакциями
    """
    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter=";")
            transactions = [transaction for transaction in csv_reader]
            return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def get_transactions_excel(excel_file_path: str) -> list[dict[str, Any]]:
    """
    Считывает финансовые операции из excel файла и
    возвращает список словарей с транзакциями
    """
    try:
        df = pd.read_excel(excel_file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {excel_file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []
