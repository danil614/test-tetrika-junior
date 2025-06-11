from functools import wraps
from inspect import signature


def _matches_strict(value, expected_type) -> bool:
    """
    Проверка строгого соответствия типа аргумента ожидаемому типу.
    """
    return type(value) is expected_type


def strict(func):
    """
    Декоратор, валидирующий типы фактических аргументов вызова функции
    относительно аннотаций её параметров. При несоответствии бросается
    TypeError с понятным сообщением.
    """
    func_signature = signature(func)  # получаем сигнатуру функции
    annotations = func.__annotations__  # словарь аннотаций

    @wraps(func)
    def wrapper(*args, **kwargs):
        # связываем позиционные/именованные аргументы с параметрами функции
        bound_arguments = func_signature.bind(*args, **kwargs)

        # проверяем каждый переданный аргумент
        for name, value in bound_arguments.arguments.items():
            expected_type = annotations.get(name)

            # если у параметра нет аннотации — ничего не проверяем
            if expected_type is None:
                continue

            if not _matches_strict(value, expected_type):
                raise TypeError(
                    f"Argument '{name}' = {value!r} "
                    f"is of type {type(value).__name__}, "
                    f"expected {expected_type.__name__}"
                )

        # всё хорошо — вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    # Демонстрация работы декоратора
    print(sum_two(1, 2))  # >>> 3

    try:
        print(sum_two(1, 2.4))  # TypeError
    except TypeError as exc:
        print(type(exc).__name__, exc)
