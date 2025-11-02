import pytest

from src.decorators import log


def test_log_success_to_file():
    """Проверяет успешный вызов функции с логом в файл"""

    log_file = "test_log_success.txt"

    @log(filename=log_file)
    def add(x, y):
        return x + y

    add(1, 2)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert f"{add.__name__} ok" in content


def test_log_error_to_file():
    """Проверяет запись ошибки в файл"""

    log_file = "test_log_error.txt"

    @log(filename=log_file)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert ("divide error: ZeroDivisionError. "
            "Inputs: (1, 0), {}") in content


def test_log_success_to_console(capsys):
    """Проверяет успешный вывод в консоль"""

    @log()
    def add(x, y):
        return x + y

    add(1, 2)
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_error_to_console(capsys):
    """Проверяет логирование ошибок в консоль"""

    @log()
    def fail_func(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        fail_func(1, 0)

    captured = capsys.readouterr()
    assert captured.out == "fail_func error: ZeroDivisionError. Inputs: (1, 0), {}\n"
