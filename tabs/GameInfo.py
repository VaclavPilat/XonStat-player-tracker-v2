from pydoc import describe
import webbrowser

from tabs.TabInfo import *
from workers.GameInfoWorker import *
from widgets.ColoredButtons import *
from misc.Config import *


class GameInfo(TabInfo):
    """Class for showing game information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Game ID
        """
        super().__init__(parent, identifier)
        self.name = "Game Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter game ID")
        # Adding widgets to layout
        self.layout.addWidget(self.__createInfo())
        self.layout.addWidget(self.__createTable())
    

    def __createInfo(self) -> ColoredTable:
        """Creates a table with game information

        Returns:
            ColoredTable: ColoredTable instance
        """
        self.info = ColoredTable(self)
        # Setting table headers settings
        self.info.setColumnCount(2)
        self.info.setShowGrid(False)
        self.info.horizontalHeader().hide()
        for i in range(self.info.columnCount()):
            self.info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.info.verticalHeader().hide()
        self.info.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Adding rows
        headings = ["Date and time [UTC]", "Server name", "Map mame", "Game mode", "Duration"]
        for heading in headings:
            row = self.info.rowCount()
            self.info.insertRow(row)
            self.info.setCellWidget(row, 0, ColoredLabel(self, heading + ":", "dark-grey"))
            self.info.cellWidget(row, 0).setAlignment(QtCore.Qt.AlignRight)
            # Adding content widgets
            widget = ColoredWidget()
            widget.setBackground("dark-grey")
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            label = ColoredLabel(self, None, "transparent")
            layout.addWidget(label)
            self.info.setCellWidget(row, 1, widget)
        # Setting fixed table height
        self.info.setMaximumHeight(self.info.rowCount() * 30)
        return self.info

    
    def __createTable(self) -> ColoredTable:
        """Creates a table for list of players

        Returns:
            ColoredTable: Table widget
        """
        self.players = ColoredTable(self)
        # Setting columns
        headers = ["Player ID", "Player name", "Nickname", "Description", "Score", "Actions"]
        self.players.setColumnCount( len(headers) )
        self.players.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.players.verticalHeader().hide()
        self.players.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.players.verticalHeader().setMinimumSectionSize(30)
        self.players.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 4):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(4, len(headers)):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        return self.players
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = GameInfoWorker(self)
        if super().startLoading() and (self.worker.isFinished() or not self.worker.isRunning()):
            self.worker.start()
    

    def showPlayer(self, identifier: int, name: str, score: int, color: str):
        """Adds a row with player information into table

        Args:
            identifier (int): Player ID
            name (str): Player name (at the time this game happened)
            score (int): Player score
            color (str): Row background color
        """
        # Checking if player exists
        player = self.__checkPlayerExistence(identifier)
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
            profileButton.clicked.connect(lambda: webbrowser.open("https://stats.xonotic.org/player/" + str(identifier), new=2))
            buttonGroup.addWidget(profileButton)
            # Load button
            infoButton = WindowButton(self.players)
            infoButton.clicked.connect(lambda: self.parent.openPlayerInfo(identifier))
            buttonGroup.addWidget(infoButton)
        buttonGroup.addStretch()
        self.players.setCellWidget(row, 5, actions)
    

    def showGroupName(self, name: str):
        """Shows group name

        Args:
            name (str): Player group name
        """
        row = self.players.rowCount()
        self.players.insertRow(row)
        label = ColoredLabel(self.players, name)
        label.setProperty("class", "center")
        self.players.setCellWidget(row, 0, label, 1, self.players.columnCount())
    

    def __checkPlayerExistence(self, identifier: int) -> dict:
        """Attempts to find the player in a config file

        Args:
            identifier (int): Player ID

        Returns:
            dict: JSON of player
        """
        if Config.instance().load("Players"):
            for player in Config.instance()["Players"]:
                if identifier == player["id"]:
                    return player
        return None