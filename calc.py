from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import operator


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calculator.ui', self)
        self.READY = 0
        self.INPUT = 1
        # запуски всех кнопок
        for n in range(0, 10):
            getattr(self, 'btn_n%s' % n).pressed.connect(lambda x=n: self.input_number(x))

        self.btn_add.pressed.connect(lambda: self.operation(operator.add))
        self.btn_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.btn_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.btn_div.pressed.connect(lambda: self.operation(operator.truediv))
        self.btn_pc.pressed.connect(self.operation_pc)
        self.btn_equal.pressed.connect(self.equals)
        self.btn_ac.pressed.connect(self.reset)
        self.btn_m.pressed.connect(self.memory_store)
        self.btn_mr.pressed.connect(self.memory_recall)

        self.memory = 0
        self.reset()
        self.show()

    def display(self): # отображение чисел
        self.lcdNumber.display(self.stack[-1])

    def reset(self): # очистка стека
        self.state = self.READY # Разграничивает поступившие и выполнившие запросы
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def memory_store(self): # Хранение памяти
        self.memory = self.lcdNumber.value()

    def memory_recall(self): # Повторный вызов
        self.state = self.INPUT
        self.stack[-1] = self.memory
        self.display()

    def input_number(self, x): # Добавление чисел в стек
        if self.state == self.READY:
            self.state = self.INPUT
            self.stack[-1] = x
        else:
            self.stack[-1] = self.stack[-1] * 10 + x
        self.display()

    def operation(self, op):
        if self.current_op:  # Содержит текущую ситуацию
            self.equals()
        self.stack.append(0)
        self.state = self.INPUT
        self.current_op = op

    def operation_pc(self): # Отдельно для процентов
        self.state = self.INPUT
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        # Если новые данные не введены, повторяем
        if self.state == self.READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op
            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = self.READY
                self.display()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Calculator")
    window = Calculator()
    app.exec_()
