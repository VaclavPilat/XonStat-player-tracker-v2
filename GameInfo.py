from Window import *
from Status import *
from ColoredWidgets import *
from GameInfoWorker import *



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
    

    def showPlayer(self, id: int, name: str, nickname: str, score: int):
        """Adds a row with player information into table

        Args:
            id (int): Player ID
            name (str): Player name (at the time this game happened)
            nickname (str): Player nickname (if this player is being tracked)
            score (int): Player score
        """
        # Creating a new row inside the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Adding labels
        for i in range(5):
            self.table.setCellWidget(row, i, ColoredLabel(self.table))
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
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Add button
        addButton = ColoredButton(self.table, "fa.user-plus", "green")
        #addButton.clicked.connect(player.showProfile)
        buttonGroup.addWidget(addButton)
        # Load button
        loadButton = ColoredButton(self.table, "msc.graph", "yellow")
        #loadButton.clicked.connect(lambda: self.openPlayerInfo(player))
        buttonGroup.addWidget(loadButton)
        buttonGroup.addStretch()
        self.table.setCellWidget(row, 4, actions)


    def __loadGameInfo(self):
        """Starts (or stops) Worker instance for loading game data
        """
        #self.showPlayer(137012, "<nade type='napalm' />", "napalm", 154)
        if self.worker is None or not self.worker.isRunning():
            self.table.setRowCount(0)
            self.worker = GameInfoWorker(self)
            self.worker.start()
        else:
            self.worker.cancel = True