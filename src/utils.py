import json
import logging
from typing import Any

from requests import Response

from src.external_api import currency_conversion

logging.basicConfig(
    level=logging.DEBUG,
    filename="../logs/utils.log",
    filemode="w",
    format="%(levelname)s:%(filename)s:%(message)s:%(asctime)s",
)

logger = logging.getLogger()


def open_json_file(path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях."""
    logger.info(f"Attempting to open json file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            logger.debug(f"file {path} successfully opened")
            try:
                data_transactions = json.load(f)
                logger.debug(f"json parsed successfully, got {type(data_transactions)}")
                if isinstance(data_transactions, list):
                    logger.info("Successful reading of JSON file with transaction")
                    return data_transactions
                else:
                    logger.warning(f"Expected list but got {type(data_transactions)}")
                    return []
            except json.JSONDecodeError as ex:
                logger.error(f"JSON decode error in file {path}: {ex}")
                return []
    except FileNotFoundError as ex:
        logger.error(ex)
        return []


def get_transaction_amount(transaction: dict[str, Any]) -> float | None | Response | Any:
    """Возвращает сумму транзакции в рублях."""
    logger.debug("Starting transaction amount processing")

    try:
        operation_amount = transaction.get("operationAmount", {})

        if not operation_amount:
            logger.info("No operationAmount found in transaction")
            return 0.0

        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")
        amount_value = operation_amount.get("amount")

        if not currency_code or not amount_value:
            return 0.0

        if currency_code == "RUB":
            logger.debug(f"Transaction in RUB, returning amount: {amount_value}")
            return amount_value

        logger.info(f"Converting transaction from {currency_code} to RUB")
        converted_amount = currency_conversion(transaction)

        if converted_amount is not None:
            logger.debug(f"Successfully converted amount: {converted_amount} RUB")
            return converted_amount
        else:
            logger.warning(f"Currency conversion failed for {currency_code}")
            return 0.0

    except (ValueError, TypeError) as ex:
        logger.error(ex)
        return 0.0
    except Exception as ex:
        logger.exception(ex)
        return 0.0
