from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class XonStatHome(Tab):
    """Class for showing a tab with information from XonStat homepage
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "XonStat home"
    

    def createLayout(self):
        self.layout.addStretch()
        pass