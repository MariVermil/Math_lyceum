import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtCore import *
import operator
from random import choice, randrange


class Main_program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        # Добавляем изображение
        self.pixmap = QPixmap('mathmem.jpg')
        self.pic_mem1.setPixmap(self.pixmap)
        # Включаем кнопки
        self.btn_calculator.clicked.connect(self.calculators)
        self.btn_oral_count.clicked.connect(self.oral_count)
        #self.btn_theory.clicked.connect(self.theories)
        self.btn_practice.clicked.connect(self.practices)

    def calculators(self):
        self.w1 = Calculator()
        self.w1.show()

    def oral_count(self):
        self.w2 = Oral_count()
        self.w2.show()

    #def theories(self):
        #self.w3 = Theory()
        #self.w3.show()

    def practices(self):
        self.w4 = Practice()
        self.w4.show()


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calculator.ui', self)
        self.status = 0
        self.enter = 1
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
        self.state = self.status # Разграничивает поступившие и выполнившие запросы
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def input_number(self, x): # Добавление чисел в стек
        if self.state == self.status:
            self.state = self.enter
            self.stack[-1] = x
        else:
            self.stack[-1] = self.stack[-1] * 10 + x
        self.display()

    def operation(self, op):
        if self.current_op:  # Содержит текущую ситуацию
            self.equals()
        self.stack.append(0)
        self.state = self.enter
        self.current_op = op

    def operation_pc(self): # Отдельно для процентов
        self.state = self.enter
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        # Если новые данные не введены, повторяем
        if self.state == self.status and self.last_operation:
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
                self.state = self.status
                self.display()

    def memory_store(self): # Хранение памяти
        self.memory = self.lcdNumber.value()

    def memory_recall(self): # Повторный вызов
        self.state = self.enter
        self.stack[-1] = self.memory
        self.display()


class Oral_count(QMainWindow):
    def __init__(self):
        super().__init__()
        self.example = ''
        uic.loadUi('chot.ui', self)
        self.pixmap3 = QPixmap('important_text')
        self.important_text.setPixmap(self.pixmap3)
        self.doing_example()
        self.btn_ok.clicked.connect(self.answer)
        self.btn_next.clicked.connect(self.doing_example)

    def doing_example(self): # Вывод выражения
        self.random_example()
        self.problem.setText(self.example)

    def random_example(self): # Составление выражения
        a = ['+', '-', '*', '//']
        mark = choice(a)
        if mark == "+":
            self.example = str(randrange(-1000, 1000)) + ' ' + '+' + ' ' + str(randrange(-1000, 1000))
        elif mark == "-":
            self.example = str(randrange(-1000, 1000)) + ' ' + '-' + ' ' + str(randrange(-1000, 1000))
        elif mark == "*":
            self.example = str(randrange(0, 100)) + ' ' + '*' + ' ' + str(randrange(0, 100))
        else:
            x = randrange(1, 100)
            y = randrange(1, 100)
            self.example = str(x * y) + ' ' + '//' + ' ' + str(y)

    def answer(self): # Проверка ответа
        text = self.ans.text()  # Получим текст из поля ввода
        if text == str(eval(self.example)):
            self.pixmap1 = QPixmap('true.jpg')
            self.ans_program.setPixmap(self.pixmap1)
        else:
            self.pixmap2 = QPixmap('false.jpg')
            self.ans_program.setPixmap(self.pixmap2)


class Practice(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('practice.ui', self)
        self.initUI()

        def initUI(self):
            # Добавляем изображение
            self.pixmap1 = QPixmap('mathmem2.jpg')
            self.pic_mem2.setPixmap(self.pixmap1)
            # Включаем кнопки
            self.btn_1.clicked.connect(self.pract_1)
            self.btn_2.clicked.connect(self.pract_2)
            self.btn_3.clicked.connect(self.pract_3)
            self.btn_4.clicked.connect(self.pract_4)
            self.btn_5.clicked.connect(self.pract_5)
            self.btn_6.clicked.connect(self.pract_6)
            self.btn_7.clicked.connect(self.pract_7)
            self.btn_8.clicked.connect(self.pract_8)
            self.btn_9.clicked.connect(self.pract_9)
            self.btn_10.clicked.connect(self.pract_10)
            self.btn_11.clicked.connect(self.pract_11)
            self.btn_12.clicked.connect(self.pract_12)
            self.btn_choice.clicked.connect(self.pract_choice)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_program()
    ex.show()
    sys.exit(app.exec())