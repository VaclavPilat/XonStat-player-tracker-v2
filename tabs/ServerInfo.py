from tabs.TabInfo import *
from widgets.ColoredButtons import *
from workers.ServerInfoWorker import *


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
        # Adding widgets to layout
        self.scrollLayout.addWidget(self.__createGameList())
        self.scrollLayout.addStretch()
    

    def __createGameList(self) -> ColoredTable:
        """Creates a table with list of recent games

        Returns:
            ColoredTable: Colored table instance
        """
        self.gameList = ColoredTable(self)
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
        self.gameList.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        self.gameList.setRowCount(0)
    

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
        self.gameList.setFixedHeight((self.gameList.rowCount() + 1) * 30)