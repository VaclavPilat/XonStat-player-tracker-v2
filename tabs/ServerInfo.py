from tabs.TabInfo import *


class ServerInfo(TabInfo):
    """Class for showing server information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Server ID
        """
        super().__init__(parent, identifier)
        self.name = "Server Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter server ID")
        # Creating an info table
        self.scrollLayout.addWidget(self.createInfoTable(["Server name", "IP address", "Port", "Created on"]))
        # Adding widgets to layout
        self.scrollLayout.addWidget(self.__createGameList())
    

    def __createGameList(self) -> ColoredTable:
        """Creates a table with list of recent games

        Returns:
            ColoredTable: Colored table instance
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
        return self.gameList
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            return
        if super().startLoading():
            self.scrollArea.setEnabled(True)
            if (self.worker.isFinished() or not self.worker.isRunning()):
                self.worker.start()
        else:
            self.scrollArea.setEnabled(False)