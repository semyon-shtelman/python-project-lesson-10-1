# Проект: Фильтрация данных
## Цель проекта
Проект предоставляет набор утилит для обработки и анализа банковских транзакций. Включает функции для фильтрации, форматирования и маскирования данных транзакций.
## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/semyon-shtelman/python-project-lesson-10-1.git
cd python-project-lesson-10-1
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:
## Основные модули и функции
Модуль widget.py - Основные функции обработки
from src.widget import mask_account_card, get_date
```
# Маскирование номеров карт и счетов
masked_card = mask_account_card("Visa Platinum 7000792289606361")
# Visa Platinum 7000 79** **** 6361

masked_account = mask_account_card("Счет 73654108430135874305")
# Счет **4305

# Форматирование даты
formatted_date = get_date("2024-01-15T10:30:00.000")
# 15.01.2024
```
Модуль mask.py - Функции маскирования
```
from src.mask import mask_card_number, mask_account_number

masked_card = mask_card_number("7000792289606361")  # 7000 79** **** 6361
masked_account = mask_account_number("73654108430135874305")  # **4305
```
Модуль processing.py - Обработка транзакций
```
from src.processing import filter_by_state, sort_by_date

# Фильтрация транзакций по статусу
executed_transactions = filter_by_state(transactions, 'EXECUTED')

# Сортировка транзакций по дате
sorted_transactions = sort_by_date(transactions, reverse=True)
```
## Тестирование

В проекте используется **pytest** для автоматического тестирования функций.

### Запуск тестов
Установите зависимости (если pytest ещё не установлен):
```
# bash
pip install pytest
pytest
```
## Документация:

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).
