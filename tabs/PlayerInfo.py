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
        # Creating scroll area
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollWidget = QtWidgets.QWidget(scrollArea)
        scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)
        scrollWidget.setLayout(scrollLayout)
        scrollArea.setWidget(scrollWidget)
        # Creating an info table
        scrollLayout.addWidget(self.createInfoTable(["Player nickname", "Player description", "Current player name", "Playing since", "Last active", "Total time spent playing", "Games played this week"]))
        # Adding server info buttons
        copyButton = CopyButton(self.info)
        copyButton.clicked.connect(lambda: QtWidgets.QApplication.instance().clipboard().setText(self.info.cellWidget(2, 1).layout().itemAt(0).widget().text()))
        self.info.cellWidget(2, 1).layout().addWidget(copyButton)
        # Adding heatmap
        scrollLayout.addWidget(self.__createHeatmap())
        # Adding list of recent games
        scrollLayout.addWidget(self.__createGameList())
        scrollLayout.addStretch()
        self.layout.addWidget(scrollArea)
    

    def __createHeatmap(self):
        """Creates a heatmap table
        """
        self.heatmap = ColoredTable(self)
        self.heatmap.setBackground("dark-grey")
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
        self.gameList.setBackground("dark-grey")
        # Generating column headers
        columns = ["Date and time [UTC]", "Mode", "Map", "Actions"]
        # Setting columns
        self.gameList.setColumnCount(len(columns))
        self.gameList.setHorizontalHeaderLabels(columns)
        self.gameList.horizontalHeader().setMinimumSectionSize(100)
        self.gameList.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 3):
            self.gameList.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.gameList.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.gameList.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.gameList.setFixedHeight((Config.instance()["Settings"]["recentGamesCount"] +1) * 30)
        return self.gameList
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = GameInfoWorker(self)
        if super().startLoading():
            self.info.setEnabled(True)
            if (self.worker.isFinished() or not self.worker.isRunning()):
                self.worker.start()
        else:
            self.info.setEnabled(False)
    

    def setInfoTextColor(self, row: int, color: str):
        """Setting text color of a content label in an info table

        Args:
            row (int): Row index
            color (str): Color class
        """
        self.info.cellWidget(row, 1).layout().itemAt(0).widget().setColor(color)