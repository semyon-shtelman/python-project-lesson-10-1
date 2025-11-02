from functools import wraps


def log(filename=None):
    """
    Декоратор log для логирования выполнения функции.

    При успешном выполнении функции:
        - Выводит в консоль или пишет в файл строку "<имя_функции> ok"

    При возникновении ошибки:
        - Выводит в консоль или пишет в файл строку
          "<имя_функции> error: <тип_ошибки>. Inputs: <args>, <kwargs>"
        - Пробрасывает оригинальное исключение дальше
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                message = f"{function.__name__} ok"
                if filename:
                    with open(filename, "a", encoding="UTF-8") as f:
                        f.write(message + "\n")
                else:
                    print(message)
                return result

            except Exception as e:
                message_error = f"{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a", encoding="UTF-8") as f:
                        f.write(message_error + "\n")
                else:
                    print(message_error)
                raise

        return wrapper

    return decorator
