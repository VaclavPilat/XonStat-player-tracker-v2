from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class PlayerInfo(Tab):
    """Class for showing player information
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