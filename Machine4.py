# Чуносов Денис ИТ-1
# Задача 4
# Абстрактная вычислительная машина имеет один регистр и шесть инструкций:
#   LD A - загрузить операнд A в регистр
#   ST A - выгрузить регистр в переменную A
#   AD A - прибавить A к регистру
#   SB A - вычесть A из регистра
#   ML A - умножить регистр на A
#   DV A - разделить регистр на A
# Дано выражение в постфиксной форме из однобуквенных операндов и операций
# +, -, *, /. Вывести инструкции машины для вычисления выражения. Результат
# остаётся в регистре, для временных переменных используются имена Tn.

import os

from stack import Stack
from checker import Checker

# знак операции и его обозначение в машине
SIGNS = {"+": "AD", "-": "SB", "*": "ML", "/": "DV"}


class Machine4:
    """
    Перевод выражения из постфиксной записи в инструкции машины с одним
    регистром. Промежуточные результаты помещаются во временные переменные Tn,
    потому что регистр один. Пример: для ABC*+DE-/ получаем
    LD B, ML C, ST T1, LD A, AD T1, ST T1, LD D, SB E, ST T2, LD T1, DV T2.
    """

    def __init__(self):
        self.expr = ""
        self.folder = os.path.dirname(__file__)
        print(Machine4.__doc__)

    def input_data(self):
        while True:
            print("\nВыберите способ ввода:")
            print("1 - из input.txt")
            print("2 - вручную")
            choice = input("Ваш выбор: ")

            if choice == "1":
                path = os.path.join(self.folder, "input.txt")
                try:
                    Checker.check_file(path)
                    with open(path, "r", encoding="utf-8") as f:
                        expr = f.readline()
                except ValueError as e:
                    print(f"!!! Ошибка: {e} !!!")
                    continue
            elif choice == "2":
                expr = input("Введите выражение в постфиксной записи: ")
            else:
                print("!!! Ошибка: введите 1 или 2 !!!")
                continue

            expr = expr.strip()
            try:
                Checker.validate(expr)
            except ValueError as e:
                print(f"!!! Ошибка: {e} !!!")
                continue

            self.expr = expr
            return

    @staticmethod
    def generate(expr):
        stack = Stack()
        code = []
        temps = 0  # сколько временных Tn сейчас лежит в стеке

        for ch in expr:
            if ch in SIGNS:
                right = stack.pop()
                left = stack.pop()
                # длина имени больше 1 бывает только у Tn. Убираем
                # переменную со стека - номер снова свободен.
                if len(right) > 1:
                    temps -= 1
                if len(left) > 1:
                    temps -= 1
                code.append("LD  " + left)
                code.append(SIGNS[ch] + "  " + right)
                temps += 1
                temp = "T" + str(temps)
                code.append("ST  " + temp)
                stack.push(temp)
            else:
                stack.push(ch)

        if code:
            code.pop()  # последний результат оставляем в регистре, ST лишний
        else:
            code.append("LD  " + stack.pop())  # одна буква, просто загружаем её
        return code

    def solve(self):
        code = Machine4.generate(self.expr)

        print(f"\nВыражение: {self.expr}")
        print("Инструкции машины:")
        for line in code:
            print(line)

        self.write_output(code)

    def write_output(self, code):
        path = os.path.join(self.folder, "output.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(code) + "\n")
        print("Файл создан: output.txt")
