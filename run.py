# Plotting imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
# Utilities imports
import numpy as np
import sys
import re

from PySide2.QtGui import QFont, QColor, QPalette
from PySide2.QtCore import Slot
# import some of class from PySide2 & QtWidgets
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
# allowed operators in a program
supported_operators = [
    'x',
    '/',
    '+',
    '*',
    '^',
    '-'
]

# converstion string as input from user to mathematical function
replacements = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}
DEFAULT_FONT = QFont("Calibri", 15)
X_RANGE = (-1000000, 10000000)
DEFAULT_FUNCTION = "x^2"
DEFAULT_RANGE = (-20, 20)

# Evaluates the string and returns a function of x


def validation(string):
    # find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in supported_operators:
            raise ValueError(
                f"Function of 'x' only allowed ,e.g: 5*x^3 + 2*x. \n Supported Operators: {', '.join(supported_operators)}"
            )
    for old, new in replacements.items():
        string = string.replace(old, new)
    if "x" not in string:
        string = f"{string}+0*x"

    # TODO : rest of validation ==> Exp Sin Cos
    def func(x):
        return eval(string)

    return func


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(100, 0, 0))
        self.setPalette(palette)

        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(12, 12)))
        self.axes = self.view.figure.subplots()

        # min and max values of x
        self.mn = QDoubleSpinBox()
        self.mx = QDoubleSpinBox()
        self.mn.setPrefix("min x: ")
        self.mx.setPrefix("max x: ")
        self.mn.setFont(DEFAULT_FONT)
        self.mx.setFont(DEFAULT_FONT)
        self.mn.setRange(*X_RANGE)
        self.mx.setRange(*X_RANGE)
        self.mn.setValue(DEFAULT_RANGE[0])
        self.mx.setValue(DEFAULT_RANGE[1])

        self.function = QLineEdit()
        self.function.setFont(DEFAULT_FONT)
        self.function.setText(DEFAULT_FUNCTION)
        self.func_label = QLabel(text="f(x): ")
        self.func_label.setFont(DEFAULT_FONT)
        self.submit = QPushButton(text="calculate")
        self.submit.setFont(DEFAULT_FONT)

        #  Create layout
        input_layout1 = QHBoxLayout()
        input_layout1.addWidget(self.func_label)
        input_layout1.addWidget(self.function)
        input_layout1.addWidget(self.submit)

        input_layout2 = QHBoxLayout()
        input_layout2.addWidget(self.mn)
        input_layout2.addWidget(self.mx)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.view)
        vlayout.addLayout(input_layout1)
        vlayout.addLayout(input_layout2)
        self.setLayout(vlayout)

        self.error_dialog = QMessageBox()
        self.error_dialog.setFont(DEFAULT_FONT)

        # connect inputs with on_change method
        self.mn.valueChanged.connect(lambda _: self.on_change(1))
        self.mx.valueChanged.connect(lambda _: self.on_change(2))
        self.submit.clicked.connect(lambda _: self.on_change(3))

        self.on_change(0)

    @Slot()
    def on_change(self, idx):  # idx is needed to identify what value is changed
        """ Update the plot with the current input values """
        mn = self.mn.value()
        mx = self.mx.value()

        # warning: min x can't be greater than or equal to max x
        if idx == 1 and mn >= mx:
            self.mn.setValue(mx-1)
            self.error_dialog.setText("'Min x' should be less than 'Max x'.")
            self.error_dialog.show()
            return

        # warning: max x can't be less than or equal to min x
        if idx == 2 and mx <= mn:
            self.mx.setValue(mn+1)
            self.error_dialog.setText(
                "'Max x' should be greater than 'Min x'.")
            self.error_dialog.show()
            return

        x = np.linspace(mn, mx)
        try:
            y = validation(self.function.text())(x)
        except ValueError as e:
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(e))
            self.error_dialog.show()
            return

        self.axes.clear()
        self.axes.plot(x, y)
        self.view.draw()


if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    w = PlotWidget()
    w.show()
    sys.exit(app.exec_())
