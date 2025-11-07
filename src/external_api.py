import os

import requests
from dotenv import load_dotenv

load_dotenv()


def currency_conversion(transaction):
    """Конвертирует сумму из одной валюты в другую."""

    api_key = os.getenv("API_KEY")
    url = "https://api.apilayer.com/currency_data/convert"

    operation_amount = transaction["operationAmount"]

    currency_info = operation_amount["currency"]
    currency_code = currency_info["code"]
    amount_value = operation_amount["amount"]

    payload = {"amount": amount_value, "from": currency_code, "to": "RUB"}

    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code == 200:
            result = response.json()
            conversion_result = result.get("result")
            if conversion_result is not None:
                return float(conversion_result)
        return None
    except requests.exceptions.RequestException:
        return None
