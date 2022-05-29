from PyQt5 import QtWidgets, QtCore, QtGui

from widgets.Status import *


class Tab(QtWidgets.QWidget):
    """Class for a new tab page
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (Tab): Parent tab
        """
        self.parent = parent
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.createLayout()
        self.status = Status(self)
        self.layout.addWidget(self.status)
    

    def createLayout(self):
        """Method for creating layout
        """
        pass