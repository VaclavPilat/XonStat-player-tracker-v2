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
        """Creating tab layout
        """
        # Creating search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by player name")
        #self.searchBar.textChanged.connect(self.__search)
        self.layout.addWidget(self.searchBar)
        # Adding widgets to layout
        self.layout.addWidget(self.__createTable())

    
    def __createTable(self) -> ColoredFixedTable:
        """Creates a table for list of players

        Returns:
            ColoredFixedTable: Table widget
        """
        self.players = ColoredTable(self)
        # Setting columns
        headers = ["Player ID", "Player name", "Nickname", "Description", "Actions"]
        self.players.setColumnCount( len(headers) )
        self.players.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.players.verticalHeader().hide()
        self.players.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.players.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 4):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(4, len(headers)):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        return self.players