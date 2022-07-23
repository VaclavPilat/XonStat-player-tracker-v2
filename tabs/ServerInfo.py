from tabs.TabInfo import *
from widgets.ColoredButtons import *
from workers.ServerInfoWorker import *
from dialogs.AddPlayerDialog import *
from dialogs.DeletePlayerDialog import *
from dialogs.EditPlayerDialog import *


class ServerInfo(TabInfo):
    """Class for showing server information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Server ID
        """
        super().__init__(parent, identifier)
        self.name = "Server Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter server ID")
        # Creating an info table
        self.scrollLayout.addWidget(self.createInfoTable(["Server name", "IP address", "Port", "Added on"]))
        # Adding info buttons
        browserButton = BrowserButton(self)
        browserButton.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/server/" + str(self.id)))
        self.info.cellWidget(0, 1).layout().addWidget(browserButton)
        # Adding widgets to layout
        self.scrollLayout.addWidget(self.__createTable())
        self.scrollLayout.addWidget(self.__createGameList())
        # Adding stretch
        self.scrollLayout.addStretch()

    
    def __createTable(self) -> ColoredFixedTable:
        """Creates a table for list of players

        Returns:
            ColoredFixedTable: Table widget
        """
        self.players = ColoredFixedTable(self)
        # Setting columns
        headers = ["Player ID", "Player name", "Nickname", "Description", "Score", "Actions"]
        self.players.setColumnCount( len(headers) )
        self.players.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.players.verticalHeader().hide()
        self.players.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 4):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(4, len(headers)):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        return self.players
    

    def __createGameList(self) -> ColoredFixedTable:
        """Creates a table with list of recent games

        Returns:
            ColoredFixedTable: Colored table instance
        """
        self.gameList = ColoredFixedTable(self)
        # Generating column headers
        columns = ["Date and time [UTC]", "Server", "Mode", "Map", "Actions"]
        # Setting columns
        self.gameList.setColumnCount(len(columns))
        self.gameList.setHorizontalHeaderLabels(columns)
        self.gameList.horizontalHeader().setMinimumSectionSize(100)
        self.gameList.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.gameList.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.gameList.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.gameList.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.gameList.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.gameList.verticalHeader().hide()
        return self.gameList
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = ServerInfoWorker(self)
        if super().startLoading():
            self.scrollArea.setEnabled(True)
            if (self.worker.isFinished() or not self.worker.isRunning()):
                self.worker.start()
        else:
            self.scrollArea.setEnabled(False)


    def clearOldInformation(self):
        """Removes old information to make space for new ones
        """
        super().clearOldInformation()
        self.players.setRowCount(0)
        self.gameList.setRowCount(0)
    

    def showPlayer(self, identifier: int, name: str, score: int, color: str):
        """Adds a row with player information into table

        Args:
            identifier (int): Player ID
            name (str): Player name (at the time this game happened)
            score (int): Player score
            color (str): Row background color
        """
        # Checking if player exists
        player = checkPlayerExistence(identifier)
        if player is not None:
            nickname = player["nick"]
            description = player["description"]
        else:
            nickname = ""
            description = ""
            if not color == None:
                color = "dark-" + color
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
        self.players.cellWidget(row, 4).setText(str(score))
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
        self.players.setCellWidget(row, 5, actions)
    

    def showRecentGame(self, game: dict):
        """Showing recent game by creating a new row in gameList table

        Args:
            game (dict): Game info
        """
        row = self.gameList.rowCount()
        if row >= Config.instance()["Settings"]["recentGamesCount"]:
            return
        self.gameList.insertRow(row)
        # Adding cells
        for i in range(4):
            self.gameList.setCellWidget(row, i, ColoredLabel(self.gameList))
        # Setting cell content
        date = datetime.datetime.strptime(game["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = date.strftime("%d.%m.%Y %H:%M:%S")
        self.gameList.cellWidget(row, 0).setText(date_str)
        self.gameList.cellWidget(row, 1).setText(game["server_name"])
        self.gameList.cellWidget(row, 2).setText(game["game_type_cd"].upper())
        self.gameList.cellWidget(row, 3).setText(game["map_name"])
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Button for showing the selected game in browser
        browserButton = BrowserButton(self.gameList)
        browserButton.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/game/" + str(game["game_id"])))
        buttonGroup.addWidget(browserButton)
        # Adding button for showing game in gameInfo window
        gameInfoButton = WindowButton(self.gameList)
        gameInfoButton.clicked.connect(lambda: self.parent.openGameInfo(game["game_id"]))
        buttonGroup.addWidget(gameInfoButton)
        self.gameList.setCellWidget(row, 4, actions)
        buttonGroup.addStretch()