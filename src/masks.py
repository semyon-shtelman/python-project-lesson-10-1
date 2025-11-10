import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="../logs/masks.log",
    filemode="w",
    format="%(levelname)s:%(filename)s:%(message)s:%(asctime)s",
)

logger = logging.getLogger()


def get_mask_card_number(card_number: int) -> str:
    """Возвращает маску номера карты в формате
    XXXX XX** **** XXXX, где X — это цифра номера"""
    logger.debug(f"Starting card number masking for: {card_number}")

    if type(card_number) is not int:
        error_msg = "Номер карты должен быть целым числом"
        logger.error(f"{error_msg}. Got type: {type(card_number)}")
        raise TypeError(error_msg)

    number_str = str(card_number)
    logger.debug(f"Converted card number to string: {number_str}")

    if len(number_str) != 16:
        error_msg = "Номер карты должен содержать 16 цифр"
        logger.debug(f"{error_msg}. Got length: {len(number_str)}")
        raise ValueError(error_msg)

    masked_card_number = f"{number_str[:4]} {number_str[4:6]}** **** {number_str[-4:]}"
    logger.info(f"Successfully masked card number: {masked_card_number}")
    return masked_card_number


def get_mask_account(account_number: int) -> str:
    """Возвращает маску номера счета в формате
    **XXXX, где X — это цифра номера"""
    logger.debug(f"starting account number masking for: {account_number}")

    if type(account_number) is not int:
        error_msg = "Номер счета должен быть целым числом"
        logger.error(f"{error_msg}. Got type: {type(account_number)}")
        raise TypeError(error_msg)

    number_str = str(account_number)
    logger.debug(f"Converted card number to string: {number_str}")

    if len(number_str) != 20:
        error_message = "Номер счета должен содержать 20 цифр"
        logger.error(f"{error_message}. Got length: {len(number_str)}")
        raise ValueError(error_message)

    masked_account_number = f"{'**'}{number_str[-4:]}"
    logger.info(f"Successfully masked account number: {masked_account_number}")
    return masked_account_number
