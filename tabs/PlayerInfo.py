from PyQt5 import QtWidgets

from tabs.TabInfo import *
from widgets.ColoredButtons import *
from workers.PlayerInfoWorker import *


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
        # Adding server info buttons
        copyButton = CopyButton(self.info)
        copyButton.clicked.connect(lambda: QtWidgets.QApplication.instance().clipboard().setText(self.info.cellWidget(2, 1).layout().itemAt(0).widget().text()))
        self.info.cellWidget(2, 1).layout().addWidget(copyButton)
        # Adding heatmap
        self.scrollLayout.addWidget(self.__createHeatmap())
        # Adding list of recent games
        self.scrollLayout.addWidget(self.__createGameList())
        self.scrollLayout.addStretch()
    

    def __createHeatmap(self):
        """Creates a heatmap table
        """
        self.heatmap = ColoredTable(self)
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
        self.heatmap.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for i in range(7):
            self.heatmap.insertRow(i)
            for j in range(self.heatmap.columnCount()):
                self.heatmap.setCellWidget(i, j, ColoredLabel(self.heatmap, None, "heatmap-0"))
        self.heatmap.setVerticalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.heatmap.setFixedHeight((self.heatmap.rowCount() + 1) * 30)
        return self.heatmap
    

    def __createGameList(self):
        """Creates a table with list of recent games
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
        self.gameList.setFixedHeight((Config.instance()["Settings"]["recentGamesCount"] +1) * 30)
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