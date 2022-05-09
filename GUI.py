# Utilities imports
from validator import*
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np

from PySide2.QtGui import QFont, QColor, QPalette
from PySide2.QtCore import Slot


# import some of class from PySide2 & QtWidgets
from PySide2.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from validator import validation
fonts = QFont("Calibri", 15)
ranges = (-1000, 1000)
defRange = (-10, 10)


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")
        palette = self.palette()
        # color of window
        palette.setColor(QPalette.Window, QColor(10, 161, 221))
        self.setPalette(palette)

        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(20, 20)))
        self.axes = self.view.figure.subplots()

        # min and max values of x
        self.min = QDoubleSpinBox()
        self.max = QDoubleSpinBox()
        self.min.setPrefix("Min X: ")
        self.max.setPrefix("Max X: ")
        self.min.setFont(fonts)
        self.max.setFont(fonts)
        self.min.setRange(*ranges)
        self.max.setRange(*ranges)
        self.min.setValue(defRange[0])
        self.max.setValue(defRange[1])

        self.function = QLineEdit()
        self.function.setFont(fonts)
        self.func_label = QLabel(text="F(x): ")
        self.function.setText("x^2")
        self.func_label.setFont(fonts)
        self.plot = QPushButton(text="Plot")
        self.plot.setFont(fonts)

        #  Create layout
        layout1 = QHBoxLayout()
        layout1.addWidget(self.func_label)
        layout1.addWidget(self.function)
        layout1.addWidget(self.plot)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.min)
        layout2.addWidget(self.max)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.view)
        vlayout.addLayout(layout1)
        vlayout.addLayout(layout2)
        self.setLayout(vlayout)

        self.error_dialog = QMessageBox()
        self.error_dialog.setFont(fonts)

        # connect inputs with on_change method
        self.min.valueChanged.connect(lambda _: self.on_change(1))
        self.max.valueChanged.connect(lambda _: self.on_change(2))
        self.plot.clicked.connect(lambda _: self.on_change(3))

        self.on_change(0)

    @Slot()
    def on_change(self, val):  # val is needed to identify what value is changed
        mn = self.min.value()
        mx = self.max.value()

        # warning: min x can't be greater than or equal to max x
        if val == 1 and mn >= mx:
            self.mn.setValue(mx-1)
            self.error_dialog.setText("'Min x' should be less than 'Max x'.")
            self.error_dialog.show()
            return

        # warning: max x can't be less than or equal to min x
        if val == 2 and mx <= mn:
            self.max.setValue(mn+1)
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
