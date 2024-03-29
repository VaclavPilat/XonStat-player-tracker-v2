from tabs.TabInfo import *
from workers.GameInfoWorker import *
from widgets.ColoredButtons import *
from misc.Config import *
from misc.Functions import *
from dialogs.AddPlayerDialog import *
from dialogs.DeletePlayerDialog import *
from dialogs.EditPlayerDialog import *


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
        # Creating an info table
        self.scrollLayout.addWidget(self.createInfoTable(["Date and time", "Server name", "Map mame", "Game mode", "Duration"]))
        # Adding info buttons
        browserButton = BrowserButton(self)
        browserButton.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/game/" + str(self.id)))
        self.info.cellWidget(0, 1).layout().addWidget(browserButton)
        # Adding server info buttons
        serverBrowser = BrowserButton(self)
        serverBrowser.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/server/" + str(getNumberFromString(self.info.cellWidget(2, 1).layout().itemAt(0).widget().text()))))
        self.info.cellWidget(2, 1).layout().addWidget(serverBrowser)
        serverInfo = WindowButton(self)
        serverInfo.clicked.connect(lambda: self.parent.openServerInfo(getNumberFromString(self.info.cellWidget(2, 1).layout().itemAt(0).widget().text())))
        self.info.cellWidget(2, 1).layout().addWidget(serverInfo)
        # Adding map info buttons
        mapBrowser = BrowserButton(self)
        mapBrowser.clicked.connect(lambda: openInBrowser("https://stats.xonotic.org/map/" + str(getNumberFromString(self.info.cellWidget(3, 1).layout().itemAt(0).widget().text()))))
        self.info.cellWidget(3, 1).layout().addWidget(mapBrowser)
        mapInfo = WindowButton(self)
        mapInfo.clicked.connect(lambda: self.parent.openMapInfo(getNumberFromString(self.info.cellWidget(3, 1).layout().itemAt(0).widget().text())))
        self.info.cellWidget(3, 1).layout().addWidget(mapInfo)
        # Adding widgets to layout
        self.scrollLayout.addWidget(self.__createTable())
        # Adding stretch
        self.scrollLayout.addStretch()

    
    def __createTable(self) -> ColoredFixedTable:
        """Creates a table for list of players

        Returns:
            ColoredFixedTable: Table widget
        """
        self.players = ColoredFixedTable(self)
        # Setting columns
        headers = ["Player ID", "Ping", "Player name", "Nickname", "Description", "Score", "Actions"]
        self.players.setColumnCount( len(headers) )
        self.players.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.players.verticalHeader().hide()
        self.players.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(2, 5):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(5, len(headers)):
            self.players.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        return self.players
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = GameInfoWorker(self)
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
    

    def showPlayer(self, identifier: int, name: str, score: int, color: str, ping: str):
        """Adds a row with player information into table

        Args:
            identifier (int): Player ID
            name (str): Player name (at the time this game happened)
            score (int): Player score
            color (str): Row background color
            ping (str): Average ping
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
        for i in range(6):
            self.players.setCellWidget(row, i, ColoredLabel(self.players, None, color))
        # Adding label text
        self.players.cellWidget(row, 0).setText(str(identifier))
        self.players.cellWidget(row, 1).setText(ping)
        self.players.cellWidget(row, 2).setText(name)
        self.players.cellWidget(row, 3).setText(nickname)
        self.players.cellWidget(row, 4).setText(description)
        self.players.cellWidget(row, 5).setText(str(score))
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
        self.players.setCellWidget(row, 6, actions)
    

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