from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout
from Window import *
from Status import *
from ColoredWidgets import *
from Player import *
from PlayerInfoWorker import *



class PlayerInfo(Window):
    """Class for showing detailed information about players
    """


    def __init__(self, player: Player):
        """Initialising GUI

        Args:
            player (Player): Player instance
        """
        self.player = player
        super().__init__()
        self.worker = PlayerInfoWorker(self)
        self.worker.start()
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowTitle("Player information")
        self.resize(450, 500)
    

    def createLayout(self):
        """Creates widnow layout with widgets
        """
        # Creating the layout itself
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding top widgets
        playerNick = ColoredLabel(self, self.player["nick"])
        playerNick.setProperty("type", "header")
        layout.addWidget(playerNick)
        playerID = ColoredLabel(self, "ID#" + str(self.player["id"]))
        playerID.setProperty("type", "subheader")
        layout.addWidget(playerID)
        # Adding a scrollable grid
        self.scrollArea = QScrollArea(self)
        layout.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContent = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaContent)
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.__fillGrid()
        # Setting gridLayout row stretch
        for i in range(self.gridLayout.rowCount()):
            self.gridLayout.setRowStretch(i, 0)
        self.gridLayout.setRowStretch(self.gridLayout.rowCount(), 1)
        # Adding status
        self.status = Status(self)
        layout.addWidget(self.status)


    def __fillGrid(self):
        """Adding widgets to gridLayout
        """
        # Adding headers
        headers = ["Current player name", "Playing since", "Last active", "Games played this week", 
            "Recently used names", "Activity heatmap"]
        for i in range(len(headers)):
            self.gridLayout.addWidget(ColoredLabel(self, headers[i]), i, 0)
        # Adding empty labels
        self.name = ColoredLabel(self)
        self.gridLayout.addWidget(self.name, 0, 1)
        self.since = ColoredLabel(self)
        self.gridLayout.addWidget(self.since, 1, 1)
        self.active = ColoredLabel(self)
        self.gridLayout.addWidget(self.active, 2, 1)
        self.games = ColoredLabel(self)
        self.gridLayout.addWidget(self.games, 3, 1)