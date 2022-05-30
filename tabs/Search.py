from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class Search(Tab):
    """Class for searching players, servers, maps...
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Search"
    

    def createLayout(self):
        self.layout.addStretch()
        pass