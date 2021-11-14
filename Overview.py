from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from Window import *
from Status import *
from OverviewWorkers import *
from AddPlayer import *
from ColoredWidgets import *
from PlayerInfo import *
import qtawesome as qta



class Overview(Window):
    """Class for creating a window that contains a table with currently tracked players 
    """


    def __init__(self):
        """Initialising GUI and a worker thread
        """
        self.players = [] # List of players
        super().__init__()
        self.worker = OverviewLoader(self)
        self.worker.start()
        self.worker.finished.connect(self.__updatePlayers)
    

    def setProperties(self):
        """Setting winow properties
        """
        # Setting window title and size
        self.setWindowTitle("Overview")
        self.resize(1300, 800)
    

    def createLayout(self):
        """Creates widnow layout with widgets
        """
        # Creating the layout itself
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding widgets to layout
        layout.addLayout(self.__createTopWidgets())
        layout.addWidget(self.__createTable())
        self.status = Status(self)
        layout.addWidget(self.status)
    

    def __createTopWidgets(self) -> QHBoxLayout:
        """Creates a box layout with search bar and a few buttons

        Returns:
            QHBoxLayout: Created layout
        """
        layout = QHBoxLayout()
        # Creating search bar
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by player ID, nickname or current player name")
        self.searchBar.textChanged.connect(self.__search)
        layout.addWidget(self.searchBar)
        # Creating button for refreshing table
        self.refreshButton = ColoredButton(self, None, None, False)
        self.refreshButton.clicked.connect(self.__updatePlayers)
        layout.addWidget(self.refreshButton)
        # Creating button for adding new player
        self.addButton = ColoredButton(self, qta.icon("fa.user-plus", color="#DDD"), "green", False)
        self.addButton.clicked.connect(self.__openAddPlayer)
        layout.addWidget(self.addButton)
        #return search
        return layout


    def __createTable(self) -> QTableWidget:
        """Creating table layout

        Returns:
            QTableWidget: Created table widget
        """
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["ID", "Player nickname", "Current player name", "Last played", 
                        "Actions"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for i in range(1, 3):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        for i in range(3, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        return self.table

    
    def showPlayer(self, player: Player):
        """Adds a single row with player data to table

        Args:
            player (Player): Player instance
        """
        # Creating a new row inside the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Adding labels
        for i in range(4):
            self.table.setCellWidget(row, i, ColoredLabel(self.table, "", "dark-grey"))
        # Adding label text
        self.table.cellWidget(row, 0).setText(str(player["id"]))
        self.table.cellWidget(row, 1).setText(player["nick"])
        self.table.cellWidget(row, 2).setProperty("class", "xolonium")
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        # Up button
        upButton = ColoredButton(self.table, qta.icon("ei.caret-up", color="#DDD"), "grey")
        buttonGroup.addWidget(upButton)
        # Down button
        downButton = ColoredButton(self.table, qta.icon("ei.caret-down", color="#DDD"), "grey")
        buttonGroup.addWidget(downButton)
        # Profile button
        profileButton = ColoredButton(self.table, qta.icon("ri.file-user-fill", color="#DDD"), "blue")
        profileButton.clicked.connect(player.showProfile)
        buttonGroup.addWidget(profileButton)
        # PlayerInfo button
        infoButton = ColoredButton(self.table, qta.icon("msc.graph", color="#DDD"), "yellow")
        infoButton.clicked.connect(lambda: self.__openPlayerInfo(player))
        buttonGroup.addWidget(infoButton)
        # Delete button
        deleteButton = ColoredButton(self.table, qta.icon("fa5s.trash-alt", color="#DDD"), "red")
        deleteButton.setObjectName("deleteButton")
        deleteButton.clicked.connect(lambda: self.__removePlayer(player))
        buttonGroup.addWidget(deleteButton)
        self.table.setCellWidget(row, 4, actions)

    
    def updatePlayer(self, player: Player):
        """Print out player variables into table

        Args:
            player (Player): Player instance
        """
        # Adding label for current player name
        widget = self.table.cellWidget(self.getRow(player), 2)
        if not player.error == None:
            widget.setText(player.error)
            widget.setAlignment(Qt.AlignCenter)
        else:
            widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            widget.setText(player.name)
        # Adding label for the last time this player was active
        widget = self.table.cellWidget(self.getRow(player), 3)
        if not player.error == None:
            widget.setText(None)
            widget.setColor(None)
        else:
            widget.setText(player.active)
            widget.setColor(player.getActiveColor())
    

    def __updatePlayers(self):
        """Attempts to update player variables
        """
        if len(self.players) > 0:
            if self.worker.isRunning():
                self.worker.cancel = True
                self.refreshButton.setEnabled(False)
            else:
                self.worker = OverviewUpdater(self)
                self.worker.start()
    

    def updateRefreshButton(self):
        """Updates visuals of "Refresh" button
        """
        if self.worker.isRunning():
            self.refreshButton.setIcon(qta.icon("mdi6.close", color="#DDD"))
            self.refreshButton.setBackground("orange")
        else:
            self.refreshButton.setIcon(qta.icon("mdi6.reload", color="#DDD"))
            self.refreshButton.setBackground("yellow")


    def __openAddPlayer(self):
        """Opening a window for adding a new player
        """
        self.addButton.setEnabled(False)
        self.refreshButton.setEnabled(False)
        self.__addPlayerWindow = AddPlayer(self)
    

    def __openPlayerInfo(self, player: Player):
        """Opens PlayerInfo window if it doen't exist

        Args:
            player (Player): Player instance
        """
        if player.window is None:
            player.window = PlayerInfo(player)
            player.window.destroyed.connect(lambda: self.__deletePlayerInfo(player))
        else:
            player.window.raise_()
            player.window.activateWindow()
    

    def __getOpenWindowCount(self):
        """Counts currently open PlayerInfo windows
        """
        openWindowCount = 0
        for player in self.players:
            if player.window is not None:
                openWindowCount += 1
        print("Current window count: " + str(openWindowCount))
        return openWindowCount

    
    def __deletePlayerInfo(self, player: Player):
        """Deleting closed PlayerInfo window

        Args:
            player (Player): Player instance
        """
        player.window = None
        if self.closing and self.__getOpenWindowCount() == 0:
            self.close()
    

    def __search(self, text: str):
        """Hiding and showing rows in the table based on input

        Args:
            text (str): Serched text
        """
        for row in range(self.table.rowCount()):
            containsText = False
            for column in range(0, 3):
                widget = self.table.cellWidget(row, column)
                if not widget == None and type(widget) == ColoredLabel:
                    # Checking if this label contins HTML
                    if "<" in widget.text().lower():
                        labelText = re.sub(re.compile('<.*?>'), '', widget.text().lower())
                    else:
                        labelText = widget.text().lower()
                    if text.lower() in labelText:
                        containsText = True
                        break
            self.table.setRowHidden(row, not containsText)
    
    
    def getRow(self, player: Player) -> int:
        """Returns index of a row that contains selected player's data

        Args:
            player (Player): Player instance

        Returns:
            int: Row index
        """
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, 0)
            if not widget == None:
                if widget.text() == str(player["id"]):
                    return row
        return -1
    

    def __removePlayer(self, player: Player):
        """Attempts to remove a player

        Args:
            player (Player): Player instance
        """
        try:
            answer = QMessageBox.question(self, 'XonStat player tracker', "Are you sure you want to delete player \n" \
                + "\"" + player["nick"] + "\" (ID " + str(player["id"]) + ") ?", QMessageBox.Yes | QMessageBox.Cancel)
            if answer == QMessageBox.Yes:
                self.worker = OverviewRemover(self, player)
                self.worker.start()
        except:
            self.status.resultMessage("An error occured while removing \"" + player["nick"] + "\" (ID " + str(player["id"]) + ")", False)
            self.setButtonsEnabled("deleteButton", True)
    

    def hidePlayer(self, player: Player):
        """Removes a row from table that contains data about selected player

        Args:
            player (Player): [description]
        """
        self.table.removeRow(self.getRow(player))
    

    def closeEvent(self, event):
        """Event called right before closing

        Args:
            event: Event
        """
        # Closing child windows
        for player in self.players:
            if player.window is not None:
                player.window.close()
        # Closing self
        super().closeEvent(event, False)
        if self.closing and self.__getOpenWindowCount() == 0:
            if self.worker.isFinished():
                self.close()
            else:
                self.worker.finished.connect(self.close)
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        # Accessing search bar
        if key == Qt.Key_Return or key == Qt.Key_Enter or ((event.modifiers() & Qt.ControlModifier) and key == Qt.Key_F):
            self.searchBar.setFocus()
        elif key == Qt.Key_Escape:
            self.searchBar.clear()
            self.searchBar.setFocus()
        # Loading players
        elif (key == Qt.Key_R and QApplication.keyboardModifiers() == Qt.ControlModifier) or key == Qt.Key_F5:
            self.__updatePlayers()