import unittest

from task1.solution import strict


class TestStrictDecorator(unittest.TestCase):
    def test_ok_int(self):
        @strict
        def inc(x: int) -> int:
            return x + 1

        self.assertEqual(inc(2), 3)

    def test_fail_type(self):
        @strict
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        with self.assertRaises(TypeError):
            greet(42)  # передали int вместо str

    def test_bool(self):
        @strict
        def negate(flag: bool) -> bool:
            return not flag

        self.assertTrue(negate(False))

        # True является subclass int, но должен считаться ошибкой при ожидании int
        with self.assertRaises(TypeError):
            @strict
            def needs_int(x: int) -> int:
                return x

            needs_int(True)

    def test_multiple_args_and_kwargs(self):
        @strict
        def concat(a: str, b: str) -> str:
            return a + b

        self.assertEqual(concat("foo", "bar"), "foobar")
        with self.assertRaises(TypeError):
            concat("foo", 123)

        @strict
        def power(base: int, exp: int) -> int:
            return base ** exp

        self.assertEqual(power(base=2, exp=3), 8)
        with self.assertRaises(TypeError):
            power(base=2, exp=3.0)
