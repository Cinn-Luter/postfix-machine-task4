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


class Node:
    """Узел односвязного списка: данные и ссылка на следующий узел."""

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """Стек на односвязном списке. Вершина это голова списка."""

    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self.size += 1

    def pop(self):
        if self.head is None:
            raise IndexError("стек пустой")
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data

    def peek(self):
        if self.head is None:
            raise IndexError("стек пустой")
        return self.head.data

    def is_empty(self):
        return self.head is None

    def print_stack(self):
        items = []
        node = self.head
        while node is not None:
            items.append(str(node.data))
            node = node.next
        print("стек сверху вниз:", " ".join(items))
