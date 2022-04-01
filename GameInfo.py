from Window import *
from Status import *
from ColoredWidgets import *
from GameInfoWorker import *
from Player import *
from PlayerInfo import *



class GameInfo(Window):
    """Class for showing information about a game
    """


    def __init__(self, overview):
        """Initialising GUI

        Args:
            overview (Overview): Overview window instance
        """
        self.overview = overview
        super().__init__()
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowTitle("Game information")
        self.resize(950, 600)
    

    def createLayout(self):
        """Creates window layout with widgets
        """
        # Creating the layout itself
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding widgets to layout
        layout.addLayout(self.__createTopWidgets())
        layout.addWidget(self.__createInfoTable())
        layout.addWidget(self.__createTable())
        self.status = Status(self)
        layout.addWidget(self.status)
    

    def __createTopWidgets(self) -> QtWidgets.QHBoxLayout:
        """Creates a box layout with search bar and a few buttons

        Returns:
            QtWidgets.QHBoxLayout: Created layout
        """
        layout = QtWidgets.QHBoxLayout()
        # Creating field for game ID
        self.gameID = QtWidgets.QLineEdit(self)
        self.gameID.setPlaceholderText("Enter game ID or link to game info on XonStat")
        layout.addWidget(self.gameID)
        # Creating button for loading game info
        self.loadButton = ColoredButton(self, "mdi6.reload", "yellow", True)
        self.loadButton.clicked.connect(self.loadGameInfo)
        layout.addWidget(self.loadButton)
        return layout
    

    def __createInfoTable(self) -> ColoredTable:
        """Creates a table with game information

        Returns:
            ColoredTable: ColoredTable instance
        """
        self.infoTable = ColoredTable(self)
        # Setting table headers settings
        self.infoTable.setColumnCount(4)
        self.infoTable.setRowCount(1)
        self.infoTable.setMaximumHeight(35)
        self.infoTable.setShowGrid(False)
        self.infoTable.horizontalHeader().hide()
        for i in range(self.infoTable.columnCount()):
            self.infoTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.infoTable.verticalHeader().hide()
        self.infoTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Server name
        self.serverName = ColoredLabel(self.infoTable)
        self.infoTable.setCellWidget(0, 0, self.serverName)
        # Map name
        self.mapName = ColoredLabel(self.infoTable)
        self.infoTable.setCellWidget(0, 1, self.mapName)
        # Game mode
        self.gameMode = ColoredLabel(self.infoTable)
        self.infoTable.setCellWidget(0, 2, self.gameMode)
        # Game time
        self.gameTime = ColoredLabel(self.infoTable)
        self.infoTable.setCellWidget(0, 3, self.gameTime)
        # Setting wiidget text align
        for i in range(self.infoTable.columnCount()):
            self.infoTable.cellWidget(0, i).setProperty("class", "center")
        self.infoTable.setEnabled(False)
        return self.infoTable

    
    def __createTable(self) -> ColoredTable:
        """Creates a table for list of players

        Returns:
            ColoredTable: Table widget
        """
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["Player ID", "Player name", "Nickname", "Score", "Actions"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setMinimumSectionSize(30)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 3):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(3, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.table.setEnabled(False)
        return self.table
    

    def showPlayer(self, id: int, name: str, score: int, color: str):
        """Adds a row with player information into table

        Args:
            id (int): Player ID
            name (str): Player name (at the time this game happened)
            score (int): Player score
            color (str): Row background color
        """
        # Checking if player exists
        player = self.__checkPlayerExistence(id)
        if player is not None:
            nickname = player["nick"]
        else:
            nickname = ""
            if not color == None:
                color = "dark-" + color
        # Creating a new row inside the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Adding labels
        for i in range(5):
            self.table.setCellWidget(row, i, ColoredLabel(self.table, None, color))
        # Adding label text
        self.table.cellWidget(row, 0).setText(str(id))
        self.table.cellWidget(row, 1).setText(name)
        self.table.cellWidget(row, 2).setText(nickname)
        for i in range(1, 3):
            self.table.cellWidget(row, i).setProperty("class", "xolonium")
        self.table.cellWidget(row, 3).setText(str(score))
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        actions.setBackground(color)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        if id >= 6:
            # Profile button
            profileButton = BrowserButton(self.table)
            profileButton.clicked.connect(lambda: webbrowser.open("https://stats.xonotic.org/player/" + str(id), new=2))
            buttonGroup.addWidget(profileButton)
            if nickname:
                # Load button
                infoButton = WindowButton(self.table)
                infoButton.clicked.connect(lambda: self.overview.openPlayerInfo(player))
                buttonGroup.addWidget(infoButton)
                # Edit button
                editButton = ColoredButton(self.table, "fa5s.pencil-alt", "orange")
                editButton.setObjectName("edit-" + str(player["id"]))
                editButton.clicked.connect(lambda: self.overview.openPlayerInfo(player, PlayerInfoViewMode.Edit))
                buttonGroup.addWidget(editButton)
                # Delete button
                deleteButton = DeleteButton(self.table)
                deleteButton.setObjectName("delete")
                deleteButton.clicked.connect(lambda: self.overview.removePlayer(player))
                buttonGroup.addWidget(deleteButton)
            else:
                # Add button
                addButton = AddButton(self.table)
                addButton.clicked.connect(lambda: self.overview.openPlayerInfo(Player({"id": id, "nick": name, "description": ""}), PlayerInfoViewMode.Add))
                buttonGroup.addWidget(addButton)
        buttonGroup.addStretch()
        self.table.setCellWidget(row, 4, actions)
    

    def __checkPlayerExistence(self, id: int) -> Player:
        """Checking if player is already tracked

        Args:
            id (int): Player id

        Returns:
            Player: Player instance
        """
        for player in self.overview.players:
            if player["id"] == id:
                return player
        return None


    def loadGameInfo(self):
        """Starts (or stops) Worker instance for loading game data
        """
        if self.worker is None or not self.worker.isRunning():
            self.table.setRowCount(0)
            self.worker = GameInfoWorker(self)
            self.worker.start()
        else:
            self.worker.cancel = True
    

    def showGroupName(self, name: str):
        """Shows group name

        Args:
            name (str): Player group name
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        label = ColoredLabel(self.table, name)
        label.setProperty("class", "center")
        self.table.setCellWidget(row, 0, label, 1, self.table.columnCount())
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        # Accessing game id field
        if key == QtCore.Qt.Key_Escape:
            self.gameID.clear()
            self.gameID.setFocus()
        # Loading game info
        elif (key == QtCore.Qt.Key_R and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier) or key == QtCore.Qt.Key_F5 or key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            self.loadGameInfo()