from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class ServerInfo(Tab):
    """Class for showing server information
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Server Info"
    

    def createLayout(self):
        self.layout.addStretch()
        pass