from PyQt5 import QtWidgets

from tabs.Tab import *
from workers.SearchWorker import *
from widgets.ColoredButtons import *
from dialogs.AddPlayerDialog import *
from dialogs.DeletePlayerDialog import *
from dialogs.EditPlayerDialog import *


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
        self.searchBar.editingFinished.connect(self.startLoading)
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
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if len(self.searchBar.text()) > 0:
            if self.worker is None:
                self.worker = SearchWorker(self)
            if self.worker.isFinished() or not self.worker.isRunning():
                self.worker.start()


    def clearOldInformation(self):
        """Removes old information to make space for new ones
        """
        self.players.setRowCount(0)
    

    def showPlayer(self, identifier: int, name: str):
        """Adds a row with player information into table

        Args:
            identifier (int): Player ID
            name (str): Current player name
        """
        # Checking if player exists
        player = checkPlayerExistence(identifier)
        if player is not None:
            nickname = player["nick"]
            description = player["description"]
            color = "dark-blue"
        else:
            nickname = ""
            description = ""
            color = None
        # Creating a new row inside the table
        row = self.players.rowCount()
        self.players.insertRow(row)
        # Adding labels
        for i in range(5):
            self.players.setCellWidget(row, i, ColoredLabel(self.players, None, color))
        # Adding label text
        self.players.cellWidget(row, 0).setText(str(identifier))
        self.players.cellWidget(row, 1).setText(name)
        self.players.cellWidget(row, 2).setText(nickname)
        self.players.cellWidget(row, 3).setText(description)
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        actions.setBackground(color)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        if identifier >= 6:
            # Profile button
            profileButton = BrowserButton(self.players)
            profileButton.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/player/" + str(identifier)))
            buttonGroup.addWidget(profileButton)
            # Load button
            infoButton = WindowButton(self.players)
            infoButton.clicked.connect(lambda: self.parent.openPlayerInfo(identifier))
            buttonGroup.addWidget(infoButton)
            # Adding buttons based on if the player is already bing tracked
            if player is not None:
                # Edit button
                editButton = EditButton(self.players)
                editButton.clicked.connect(lambda: EditPlayerDialog(self.parent, identifier))
                buttonGroup.addWidget(editButton)
                # Delete button
                deleteButton = DeleteButton(self.players)
                deleteButton.clicked.connect(lambda: DeletePlayerDialog(self.parent, identifier))
                buttonGroup.addWidget(deleteButton)
            else:
                # Add button
                addButton = AddButton(self.players)
                addButton.clicked.connect(lambda: AddPlayerDialog(self.parent, identifier))
                buttonGroup.addWidget(addButton)
        buttonGroup.addStretch()
        self.players.setCellWidget(row, 4, actions)