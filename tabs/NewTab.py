from PyQt5 import QtWidgets, QtCore, QtGui


class NewTab(QtWidgets.QWidget):
    """Class for a new tab page
    """


    def __init__(self):
        """Init
        """
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        label = QtWidgets.QLabel(self)
        label.setText("aaaaa")
        self.layout.addWidget(label)