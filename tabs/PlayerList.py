from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *
from widgets.ColoredWidgets import *
from widgets.ColoredButtons import *
from workers.PlayerListWorker import *


class PlayerList(Tab):
    """Class for a showing list of currently tracked players
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Player List"
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by player ID, nickname, description or current player name")
        self.searchBar.textChanged.connect(self.__search)
        self.layout.addWidget(self.searchBar)
        # Creating table for tracked players
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["ID", "Player nickname", "Player description", "Current player name", "Last played", 
                        "Actions"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setMinimumSectionSize(30)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 4):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(4, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table)

    
    def showPlayer(self, player: dict):
        """Adds a single row with player data to table

        Args:
            player (dics): Player info
        """
        # Creating a new row inside the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Adding labels
        for i in range(5):
            self.table.setCellWidget(row, i, ColoredLabel(self.table, "", "dark-grey"))
        # Adding label text
        self.table.cellWidget(row, 0).setText(str(player["id"]))
        self.table.cellWidget(row, 1).setText(player["nick"])
        self.table.cellWidget(row, 2).setText(player["description"])
        # Adding buttons
        actions = ColoredWidget()
        actions.setBackground("dark-grey")
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Profile button
        profileButton = BrowserButton(self.table)
        buttonGroup.addWidget(profileButton)
        # PlayerInfo button
        infoButton = WindowButton(self.table)
        buttonGroup.addWidget(infoButton)
        # Stacked widget with edit and save button
        editButton = EditButton(self.table)
        buttonGroup.addWidget(editButton)
        # Delete button
        deleteButton = DeleteButton(self.table)
        buttonGroup.addWidget(deleteButton)
        buttonGroup.addStretch()
        self.table.setCellWidget(row, 5, actions)
    

    def __search(self, text: str):
        """Hiding and showing rows in the table based on input

        Args:
            text (str): Serched text
        """
        for row in range(self.table.rowCount()):
            containsText = False
            for column in range(0, 4):
                widget = self.table.cellWidget(row, column)
                if not widget == None and type(widget) == ColoredLabel:
                    # Checking if this label contins HTML
                    labelText = self.__parseTextFromLabel(widget)
                    if text.lower() in labelText:
                        containsText = True
                        break
            self.table.setRowHidden(row, not containsText)
    

    def startLoading(self):
        """Starting page (re)loading
        """
        self.worker = PlayerListWorker(self)
        self.worker.start()