from Window import *
from Status import *
from ColoredWidgets import *



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
        self.resize(800, 600)
    

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


    def __loadGameInfo(self):
        """Starts a Worker instance for loading game data
        """
        pass