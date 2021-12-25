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
        self.loadButton.clicked.connect(self.__loadGameInfo)
        layout.addWidget(self.loadButton)
        return layout

    
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
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setMinimumSectionSize(30)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 3):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(3, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
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
        self.table.cellWidget(row, 1).setProperty("class", "xolonium")
        self.table.cellWidget(row, 2).setText(nickname)
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
            profileButton = ColoredButton(self.table, "ri.file-user-fill", "blue")
            profileButton.clicked.connect(lambda: webbrowser.open("https://stats.xonotic.org/player/" + str(id), new=2))
            buttonGroup.addWidget(profileButton)
            if nickname:
                # Load button
                infoButton = ColoredButton(self.table, "msc.graph", "yellow")
                infoButton.clicked.connect(lambda: self.overview.openPlayerInfo(player))
                buttonGroup.addWidget(infoButton)
                # Edit button
                editButton = ColoredButton(self.table, "fa5s.pencil-alt", "orange")
                editButton.setObjectName("edit-" + str(player["id"]))
                editButton.clicked.connect(lambda: self.overview.openPlayerInfo(player, PlayerInfoViewMode.Edit))
                buttonGroup.addWidget(editButton)
            else:
                # Add button
                addButton = ColoredButton(self.table, "fa.user-plus", "green")
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


    def __loadGameInfo(self):
        """Starts (or stops) Worker instance for loading game data
        """
        if self.worker is None or not self.worker.isRunning():
            self.table.setRowCount(0)
            self.worker = GameInfoWorker(self)
            self.worker.start()
        else:
            self.worker.cancel = True