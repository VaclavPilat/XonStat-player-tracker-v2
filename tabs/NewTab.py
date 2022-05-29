from PyQt5 import QtWidgets, QtCore, QtGui

from tabs.Tab import *


class NewTab(Tab):
    """Class for a new tab page
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
    

    def createLayout(self):
        label = QtWidgets.QLabel(self)
        label.setText("aaaaa")
        self.layout.addWidget(label)