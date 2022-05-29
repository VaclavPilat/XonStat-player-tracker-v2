from PyQt5 import QtWidgets, QtCore, QtGui

from windows.Window import *
from widgets.ColoredWidgets import *


class MainWindow(Window):
    """Class for showing a main window with tabs
    """


    def __init__(self):
        """Init
        """
        super().__init__()
    

    def setProperties(self):
        """Setting window properties
        """
        self.setWindowTitle()
        self.resize(1300, 800)
    

    def createLayout(self):
        """Creates window layout with widgets
        """
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.removeTab)

        for i in range(10):
            self.addTab(QtWidgets.QWidget(), str(i))
    

    def addTab(self, page: QtWidgets.QWidget, title: str):
        """Adds a new tab

        Args:
            page (QtWidgets.QWidget): Tab content
            title (str): Tab title
        """
        self.tabWidget.addTab(page, title)


    def removeTab (self, index: int):
        """Removing tab and the page under the selected index

        Args:
            index (int): _description_
        """
        if self.tabWidget.currentIndex() >= 0:
            widget = self.tabWidget.widget(index)
            widget.deleteLater()
            self.tabWidget.removeTab(index)
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        # Accessing search bar
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Closing current tab
            if key == QtCore.Qt.Key_W:
                self.removeTab(self.tabWidget.currentIndex())
            # Closing all tabs
            if key == QtCore.Qt.Key_Q:
                while self.tabWidget.currentIndex() >= 0:
                    self.removeTab(self.tabWidget.currentIndex())