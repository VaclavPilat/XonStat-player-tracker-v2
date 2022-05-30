from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class GameInfo(Tab):
    """Class for showing game information
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
    

    def createLayout(self):
        self.layout.addStretch()
        pass