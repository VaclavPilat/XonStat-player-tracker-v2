from PyQt5 import QtWidgets, QtCore, QtGui

from windows.Window import *
from widgets.ColoredWidgets import *
from widgets.ColoredButtons import *
from tabs.NewTab import *
from tabs.PlayerList import *
from tabs.XonStatHome import *
from tabs.Search import *
from tabs.PlayerInfo import *
from tabs.GameInfo import *
from tabs.ServerInfo import *
from tabs.MapInfo import *


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
        self.setMinimumSize(900, 600)
        self.resize(1300, 800)
    

    def createLayout(self):
        """Creates window layout with widgets
        """
        # Creating tab widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.tabCloseRequested.connect(self.removeTab)
        # Adding new tab
        self.openNewTab()
        # Adding corner buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(5, 2, 5, 3)
        # Tab button
        tabButton = TabButton(self)
        tabButton.clicked.connect(self.openNewTab)
        buttonGroup.addWidget(tabButton)
        # Adding widget with corner buttons
        self.tabWidget.setCornerWidget(actions)
    

    def __addTab(self, page: Tab):
        """Adds a new tab

        Args:
            page (QtWidgets.QWidget): Tab content
        """
        self.tabWidget.addTab(page, page.name)
        index = self.tabWidget.count() -1
        self.tabWidget.setCurrentIndex(index)
        print("Added " + type(page).__name__ + " at index " + str(index))
    

    def __insertTab(self, page: Tab, index: int):
        """Inserts a new tab at a selected position

        Args:
            page (QtWidgets.QWidget): Tab content
            index (int): Tab index
        """
        self.tabWidget.insertTab(index, page, page.name)
        self.tabWidget.setCurrentIndex(index)
        print("Inserted " + type(page).__name__ + " at index " + str(index))


    def openNewTab(self):
        """Attempts to add a New Tab
        """
        for i in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(i), NewTab):
                self.tabWidget.setCurrentIndex(i)
                return
        self.__addTab(NewTab(self))
    

    def openPlayerList(self):
        """Attempts to add a new PlayerList tab
        """
        for i in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(i), PlayerList):
                self.tabWidget.setCurrentIndex(i)
                return
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(PlayerList(self), index)
        else:
            self.__addTab(PlayerList(self))
    

    def openXonStatHome(self):
        """Attempts to add a new XonStatHome tab
        """
        for i in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(i), XonStatHome):
                self.tabWidget.setCurrentIndex(i)
                return
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(XonStatHome(self), index)
        else:
            self.__addTab(XonStatHome(self))
    

    def openSearch(self):
        """Attempts to add a new Search tab
        """
        for i in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(i), Search):
                self.tabWidget.setCurrentIndex(i)
                return
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(Search(self), index)
        else:
            self.__addTab(Search(self))
    

    def openPlayerInfo(self):
        """Attempts to add a new PlayerInfo tab
        """
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(PlayerInfo(self), index)
        else:
            self.__addTab(PlayerInfo(self))
    

    def openGameInfo(self):
        """Attempts to add a new GameInfo tab
        """
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(GameInfo(self), index)
        else:
            self.__addTab(GameInfo(self))
    

    def openServerInfo(self):
        """Attempts to add a new ServerInfo tab
        """
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(ServerInfo(self), index)
        else:
            self.__addTab(ServerInfo(self))
    

    def openMapInfo(self):
        """Attempts to add a new MapInfo tab
        """
        if isinstance(self.tabWidget.currentWidget(), NewTab):
            index = self.tabWidget.currentIndex()
            self.removeTab(index, True, False)
            self.__insertTab(MapInfo(self), index)
        else:
            self.__addTab(MapInfo(self))


    def removeTab(self, index: int, preventAdding: bool = False, preventClosing: bool = True):
        """Removing tab and the page under the selected index

        Args:
            index (int): Tab index
            preventAdding (bool): Should it prevent adding new tab?
            preventClosing (bool): Should it prevent closing the last tab?
        """
        if preventClosing and self.tabWidget.count() == 1 and isinstance(self.tabWidget.widget(0), NewTab):
            return
        if self.tabWidget.count() > 0:
            widget = self.tabWidget.widget(index)
            print("Removed " + type(widget).__name__ + " at index " + str(index))
            widget.deleteLater()
            self.tabWidget.removeTab(index)
        if not preventAdding and self.tabWidget.currentIndex() < 0:
            self.openNewTab()
    

    def removeTabs(self):
        """Removes all tabs
        """
        while not (self.tabWidget.count() == 1 and isinstance(self.tabWidget.widget(0), NewTab)) and self.tabWidget.count() > 0:
            self.removeTab(self.tabWidget.currentIndex(), True)
        if self.tabWidget.count() == 0:
            self.openNewTab()
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Closing current tab
            if key == QtCore.Qt.Key_W:
                self.removeTab(self.tabWidget.currentIndex())
            # Closing all tabs
            elif key == QtCore.Qt.Key_Q:
                self.removeTabs()
            # Adding a new tab
            elif key == QtCore.Qt.Key_T or key == QtCore.Qt.Key_N:
                self.openNewTab()