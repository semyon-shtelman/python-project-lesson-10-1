import os

import requests
from dotenv import load_dotenv

load_dotenv()


def currency_conversion(amount, currency):
    """Конвертирует сумму из одной валюты в другую."""

    api_key = os.getenv("API_KEY")
    url = "https://api.apilayer.com/currency_data/convert"

    payload = {"amount": amount, "from": currency, "to": "RUB"}

    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("result")
        return None
    except requests.exceptions.RequestException:
        return None
