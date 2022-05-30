from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class PlayerList(Tab):
    """Class for a showing list of currently tracked players
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