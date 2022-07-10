from PyQt5 import QtWidgets

from tabs.TabInfo import *
from widgets.ColoredButtons import *
from workers.PlayerInfoWorker import *
from dialogs.AddPlayerDialog import *
from dialogs.DeletePlayerDialog import *
from dialogs.EditPlayerDialog import *


class PlayerInfo(TabInfo):
    """Class for showing player information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Player ID
        """
        super().__init__(parent, identifier)
        self.name = "Player Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter player ID")
        self.scrollLayout.addWidget(self.createInfoTable(["Player nickname", "Player description", "Current player name", "Playing since", "Last active", "Total time spent playing", "Games played this week"]))
        # Adding info buttons
        browserButton = BrowserButton(self)
        browserButton.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/player/" + str(self.id)))
        self.info.cellWidget(0, 1).layout().addWidget(browserButton)
        # Adding buttons based on player existence
        if checkPlayerExistence(self.id) is not None:
            # Edit button
            editButton = EditButton(self)
            editButton.clicked.connect(lambda: EditPlayerDialog(self.parent, self.id))
            self.info.cellWidget(1, 1).layout().addWidget(editButton)
            # Delete button
            deleteButton = DeleteButton(self)
            deleteButton.clicked.connect(lambda: DeletePlayerDialog(self.parent, self.id))
            self.info.cellWidget(1, 1).layout().addWidget(deleteButton)
        else:
            # Add player button
            addButton = AddButton(self)
            addButton.clicked.connect(lambda: AddPlayerDialog(self.parent, self.id))
            self.info.cellWidget(1, 1).layout().addWidget(addButton)
        # Adding server info buttons
        copyButton = CopyButton(self.info)
        copyButton.clicked.connect(lambda: QtWidgets.QApplication.instance().clipboard().setText(self.info.cellWidget(3, 1).layout().itemAt(0).widget().text()))
        self.info.cellWidget(3, 1).layout().addWidget(copyButton)
        # Adding a table for game mode statistics
        self.scrollLayout.addWidget(self.__createGameStats())
        # Adding heatmap
        self.scrollLayout.addWidget(self.__createHeatmap())
        # Adding list of recent games
        self.scrollLayout.addWidget(self.__createGameList())
        # Adding stretch
        self.scrollLayout.addStretch()


    def __createGameStats(self) -> ColoredFixedTable:
        """Creates a table for game mode statistics

        Returns:
            ColoredFixedTable: Colored table instance
        """
        self.gameStats = ColoredFixedTable(self)
        self.gameStats.verticalHeader().hide()
        # Setting columns
        columns = ["Game mode", "Games played", "Win rate [%]", "K/D ratio", "Time spent [hours]", "Last played"]
        self.gameStats.setColumnCount(len(columns))
        self.gameStats.setHorizontalHeaderLabels(columns)
        self.gameStats.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        return self.gameStats

    
    def __createHeatmap(self) -> ColoredFixedTable:
        """Creates a heatmap table

        Returns:
            ColoredFixedTable: Colored table instance
        """
        self.heatmap = ColoredFixedTable(self)
        self.heatmap.setProperty("class", "heatmap")
        # Generating column headers
        columns = []
        for i in range(0, 24, Config.instance()["Settings"]["heatmapHourSpan"]):
            columns.append(str(i) + "-" + str(i + Config.instance()["Settings"]["heatmapHourSpan"]))
        # Setting columns
        self.heatmap.setColumnCount(len(columns))
        self.heatmap.setHorizontalHeaderLabels(columns)
        self.heatmap.horizontalHeader().setMinimumSectionSize(50)
        self.heatmap.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Generating rows
        for i in range(7):
            self.heatmap.insertRow(i)
            for j in range(self.heatmap.columnCount()):
                self.heatmap.setCellWidget(i, j, ColoredLabel(self.heatmap, None, "heatmap-0"))
        self.heatmap.setVerticalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        return self.heatmap
    

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
            self.worker = PlayerInfoWorker(self)
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
        for i in range(self.heatmap.rowCount()):
            for j in range(self.heatmap.columnCount()):
                self.heatmap.cellWidget(i, j).setText("")
                self.heatmap.cellWidget(i, j).setBackground("heatmap-0")
        self.setInfoContent(6, "")
        self.gameStats.setRowCount(0)
    

    def setInfoTextColor(self, row: int, color: str):
        """Setting text color of a content label in an info table

        Args:
            row (int): Row index
            color (str): Color class
        """
        self.info.cellWidget(row, 1).layout().itemAt(0).widget().setColor(color)
    

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


    def updateHeatmap(self, row: int, column: int):
        """Updates data in a heatmap table

        Args:
            row (int): Row index
            column (int): Column index
        """
        widget = self.heatmap.cellWidget(row, column)
        # Getting current game count
        currentText = widget.text()
        if currentText is not None and len(currentText) > 0:
            currentCount = int(currentText)
        else:
            currentCount = 0
        # Updating current count
        currentCount += 1
        currentText = str(currentCount)
        widget.setText(currentText)
        if currentCount <= 10:
            widget.setBackground("heatmap-" + currentText)
    

    def showGameStats(self, dataList: list, dataDict: dict):
        """Shows information about game modes

        Args:
            dataList (list): List of game mode stats
            dataDict (dict): Dict with game mode stats
        """
        for gameMode in dataList:
            name = gameMode["game_type_cd"]
            if name == "overall":
                continue
            row = self.gameStats.rowCount()
            self.gameStats.insertRow(row)
            for column in range(self.gameStats.columnCount()):
                self.gameStats.setCellWidget(row, column, ColoredLabel(self.gameStats))
            self.gameStats.cellWidget(row, 0).setText(name.upper())
            self.gameStats.cellWidget(row, 1).setText(str(gameMode["games"]))
            self.gameStats.cellWidget(row, 2).setText(str(round(gameMode["win_pct"], 2)))
            self.gameStats.cellWidget(row, 3).setText(str(round(dataDict[name]["k_d_ratio"], 2)))
            self.gameStats.cellWidget(row, 4).setText(str(round(dataDict[name]["total_playing_time"] / 3600, 1)))
            self.gameStats.cellWidget(row, 5).setText(dataDict[name]["last_played_fuzzy"])
            self.gameStats.cellWidget(row, 5).setColor(getActiveColor(dataDict[name]["last_played_fuzzy"]))