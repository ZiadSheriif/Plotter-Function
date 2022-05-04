# Plotting imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
# Utilities imports
import numpy as np
import sys
import re

from PySide2.QtGui import QFont,QColor,QPalette
from PySide2.QtCore import Slot
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

supported_operators = [
    'x',
    '/',
    '+',
    '*',
    '^',
    '-'
]