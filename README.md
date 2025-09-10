# Python Project Lesson 10-1

Учебный проект по работе с транзакциями: фильтрация и сортировка.

## Возможности

- **Фильтрация транзакций по статусу**  
  Функция `filter_by_state` оставляет только те операции, у которых статус совпадает с заданным (по умолчанию — `EXECUTED`).

- **Сортировка транзакций по дате**  
  Функция `sort_by_date` сортирует список операций от новых к старым (по умолчанию) или наоборот.

## Установка

С клонируйте репозиторий и установите зависимости:

```
git clone https://github.com/semyon-shtelman/python-project-lesson-10-1.git
cd python-project-lesson-10-1
pip install -r requirements.txt
```
## Использование

Пример работы с функциями:
```
from processing import filter_by_state, sort_by_date

transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2025-09-01"},
    {"id": 2, "state": "CANCELED", "date": "2025-08-20"},
    {"id": 3, "state": "EXECUTED", "date": "2025-09-05"},
]

# Фильтрация только выполненных операций
executed = filter_by_state(transactions)
print(executed)
# [{'id': 1, 'state': 'EXECUTED', 'date': '2025-09-01'},
#  {'id': 3, 'state': 'EXECUTED', 'date': '2025-09-05'}]

# Сортировка по дате (от новых к старым)
sorted_tx = sort_by_date(executed)
print(sorted_tx)
# [{'id': 3, ...}, {'id': 1, ...}]

```