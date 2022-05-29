from PyQt5 import QtWidgets, QtCore, QtGui

from windows.Window import *
from widgets.ColoredWidgets import *
from widgets.ColoredButtons import *
from tabs.NewTab import *


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
        # Creating tab widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.removeTab)
        # Adding new tab
        self.addNewTab()
        # Adding corner buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(5, 2, 5, 3)
        # Tab button
        tabButton = TabButton(self)
        tabButton.clicked.connect(self.addNewTab)
        buttonGroup.addWidget(tabButton)
        # Adding widget with corner buttons
        self.tabWidget.setCornerWidget(actions)
    

    def addTab(self, page: QtWidgets.QWidget, title: str):
        """Adds a new tab

        Args:
            page (QtWidgets.QWidget): Tab content
            title (str): Tab title
        """
        self.tabWidget.addTab(page, title)


    def addNewTab(self):
        """Adding a new tab
        """
        self.addTab(NewTab(self), "New Tab")
        self.tabWidget.setCurrentIndex(self.tabWidget.count() -1)


    def removeTab(self, index: int, recursive: bool = False):
        """Removing tab and the page under the selected index

        Args:
            index (int): Tab index
            recursive (bool): Is the removal recursive?
        """
        if self.tabWidget.count() == 1 and isinstance(self.tabWidget.widget(0), NewTab):
            return
        if self.tabWidget.currentIndex() >= 0:
            widget = self.tabWidget.widget(index)
            widget.deleteLater()
            self.tabWidget.removeTab(index)
        if not recursive and self.tabWidget.currentIndex() < 0:
            self.addNewTab()
    

    def removeTabs(self):
        """Removes all tabs
        """
        while not (self.tabWidget.count() == 1 and isinstance(self.tabWidget.widget(0), NewTab)):
            self.removeTab(self.tabWidget.currentIndex(), True)
        if self.tabWidget.count == 0:
            self.addNewTab()
    

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
                self.removeTabs()
            # Adding a new tab
            if key == QtCore.Qt.Key_T or key == QtCore.Qt.Key_N:
                self.addNewTab()