from PyQt5 import QtWidgets, QtCore
import qtawesome as qta

from tabs.Tab import *


class Settings(Tab):
    """Class for a settings tab
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Settings"
    

    def createLayout(self):
        self.layout.addStretch()