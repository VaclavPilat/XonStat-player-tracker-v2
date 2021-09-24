from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from ColoredWidget import *

class ColoredButton(QPushButton, ColoredWidget):
    """Creating easily stylable buttons
    """


    def __init__(self, parent: QWidget, text: str, color: str = "grey", enabled: bool = True):
        """Initializes a button

        Args:
            parent (QWidget): Parent of this button
            text (str): Button text
            color (str): Button background color
            enabled (bool): Setting if this button is enabled
        """
        super().__init__(text, parent)
        self.setBackground(color)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setEnabled(enabled)