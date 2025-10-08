from functools import wraps


def log(filename=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = function(*args)
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
