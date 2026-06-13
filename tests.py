# Чуносов Денис ИТ-1
# Вспомогательный файл с тестами, для сдачи не нужен.
# Запуск: python tests.py

import os

from Machine4 import Machine4
from checker import Checker
from stack import Stack

passed = 0
failed = 0


def check(name, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"OK    {name}")
    else:
        failed += 1
        print(f"FAIL  {name}  {details}")


def check_generate(name, expr, expected):
    actual = Machine4.generate(expr)
    check(name, actual == expected, f"ожидалось {expected}, получено {actual}")


def check_valid(name, expr):
    try:
        Checker.validate(expr)
        check(name, True)
    except ValueError as e:
        check(name, False, f"неожиданная ошибка: {e}")


def check_invalid(name, expr):
    try:
        Checker.validate(expr)
        check(name, False, "ошибка не обнаружена")
    except ValueError:
        check(name, True)


# стек
s = Stack()
check("стек: новый пуст", s.is_empty() and s.size == 0)
s.push("A")
s.push("B")
check("стек: push/peek", s.peek() == "B" and s.size == 2)
check("стек: pop LIFO", s.pop() == "B" and s.pop() == "A")
check("стек: снова пуст", s.is_empty())
try:
    s.pop()
    check("стек: pop из пустого", False, "исключения не было")
except IndexError:
    check("стек: pop из пустого", True)

# generate
check_generate(
    "пример из PDF: ABC*+DE-/",
    "ABC*+DE-/",
    [
        "LD  B", "ML  C", "ST  T1",
        "LD  A", "AD  T1", "ST  T1",
        "LD  D", "SB  E", "ST  T2",
        "LD  T1", "DV  T2",
    ],
)
check_generate("операция +", "AB+", ["LD  A", "AD  B"])
check_generate("операция -", "AB-", ["LD  A", "SB  B"])
check_generate("операция *", "AB*", ["LD  A", "ML  B"])
check_generate("операция /", "AB/", ["LD  A", "DV  B"])
check_generate(
    "темп слева: AB+C*",
    "AB+C*",
    ["LD  A", "AD  B", "ST  T1", "LD  T1", "ML  C"],
)
check_generate(
    "переиспользование темпов: AB*CD*EF*-+",
    "AB*CD*EF*-+",
    [
        "LD  A", "ML  B", "ST  T1",
        "LD  C", "ML  D", "ST  T2",
        "LD  E", "ML  F", "ST  T3",
        "LD  T2", "SB  T3", "ST  T2",
        "LD  T1", "AD  T2",
    ],
)
check_generate("один операнд", "A", ["LD  A"])
check_generate("операнд-буква T", "TA+", ["LD  T", "AD  A"])
check_generate("строчные операнды", "ab+", ["LD  a", "AD  b"])

# validate: корректные
check_valid("валидно: пример из PDF", "ABC*+DE-/")
check_valid("валидно: один операнд", "A")
check_valid("валидно: длинная цепочка", "ab*cd*+ef*-")

# validate: некорректные
check_invalid("пустая строка", "")
check_invalid("два операнда без операции", "AB")
check_invalid("операции не хватает операндов", "A+")
check_invalid("одна операция без операндов", "+")
check_invalid("операция в начале", "+AB")
check_invalid("лишний операнд в конце", "AB+C")
check_invalid("лишняя операция в конце", "AB++")
check_invalid("цифра в выражении", "A1+")
check_invalid("пробел внутри выражения", "A B+")
check_invalid("недопустимый символ", "AB&")
check_invalid("инфиксная запись", "A+B")

# check_file: существование и пустота
folder = os.path.dirname(__file__)
missing = os.path.join(folder, "net_takogo_fayla.txt")
try:
    Checker.check_file(missing)
    check("файл: которого нет", False, "ошибки не было")
except ValueError:
    check("файл: которого нет", True)

empty = os.path.join(folder, "empty_test.txt")
open(empty, "w").close()
try:
    Checker.check_file(empty)
    check("файл: пустой", False, "ошибки не было")
except ValueError:
    check("файл: пустой", True)
os.remove(empty)

check_file_ok = os.path.join(folder, "input.txt")
try:
    Checker.check_file(check_file_ok)
    check("файл: input.txt на месте и не пустой", True)
except ValueError as e:
    check("файл: input.txt на месте и не пустой", False, str(e))

print(f"\nИтого: пройдено {passed}, провалено {failed}")
if failed:
    raise SystemExit(1)
