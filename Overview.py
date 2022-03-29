from PyQt5 import QtWidgets, QtCore, QtGui

from Window import *
from Status import *
from OverviewWorkers import *
from ColoredWidgets import *
from PlayerInfo import *
from Functions import *
from GameInfo import *



class Overview(Window):
    """Class for creating a window that contains a table with currently tracked players 
    """


    def __init__(self):
        """Initialising GUI and a worker thread
        """
        self.players = [] # List of players
        self.gameInfo = None
        super().__init__()
        self.worker = OverviewLoader(self)
        self.worker.start()
        self.worker.finished.connect(self.__updatePlayers)
        self.__doc = QtGui.QTextDocument() # TextDocument class for parsing text from HTML
    

    def setProperties(self):
        """Setting winow properties
        """
        # Setting window title and size
        self.setWindowTitle("Overview")
        self.resize(1300, 800)
    

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
        # Creating search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by player ID, nickname, description or current player name")
        self.searchBar.textChanged.connect(self.__search)
        layout.addWidget(self.searchBar)
        # Creating button for refreshing table
        self.refreshButton = ColoredButton(self, None, None, False)
        self.refreshButton.clicked.connect(self.__updatePlayers)
        layout.addWidget(self.refreshButton)
        # Creating button for adding new player
        self.addButton = ColoredButton(self, "fa.user-plus", "green", False)
        self.addButton.clicked.connect(lambda: self.openPlayerInfo(Player(), PlayerInfoViewMode.Add))
        layout.addWidget(self.addButton)
        # Creating button for loading game info
        self.gameInfoButton = ColoredButton(self, "fa.users", "yellow", True)
        self.gameInfoButton.clicked.connect(self.__openGameInfo)
        layout.addWidget(self.gameInfoButton)
        return layout


    def __createTable(self) -> QtWidgets.QTableWidget:
        """Creating table layout

        Returns:
            QtWidgets.QTableWidget: Created table widget
        """
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["ID", "Player nickname", "Player description", "Current player name", "Last played", 
                        "Actions"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setMinimumSectionSize(30)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1, 4):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        for i in range(4, len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
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
        for i in range(5):
            self.table.setCellWidget(row, i, ColoredLabel(self.table, "", "dark-grey"))
        # Adding label text
        self.table.cellWidget(row, 0).setText(str(player["id"]))
        self.table.cellWidget(row, 1).setText(player["nick"])
        self.table.cellWidget(row, 2).setText(player["description"])
        for i in range(1, 4):
            self.table.cellWidget(row, i).setProperty("class", "xolonium")
        # Adding buttons
        actions = ColoredWidget()
        actions.setBackground("dark-grey")
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Profile button
        profileButton = ColoredButton(self.table, "ri.file-user-fill", "blue")
        profileButton.clicked.connect(player.showProfile)
        buttonGroup.addWidget(profileButton)
        # PlayerInfo button
        infoButton = ColoredButton(self.table, "msc.graph", "yellow")
        infoButton.clicked.connect(lambda: self.openPlayerInfo(player))
        buttonGroup.addWidget(infoButton)
        # Edit button
        editButton = ColoredButton(self.table, "fa5s.pencil-alt", "orange")
        editButton.setObjectName("edit-" + str(player["id"]))
        editButton.clicked.connect(lambda: self.openPlayerInfo(player, PlayerInfoViewMode.Edit))
        buttonGroup.addWidget(editButton)
        # Delete button
        deleteButton = ColoredButton(self.table, "fa5s.trash-alt", "red")
        deleteButton.setObjectName("delete")
        deleteButton.clicked.connect(lambda: self.removePlayer(player))
        buttonGroup.addWidget(deleteButton)
        buttonGroup.addStretch()
        self.table.setCellWidget(row, 5, actions)

    
    def updatePlayer(self, player: Player):
        """Print out player variables into table

        Args:
            player (Player): Player instance
        """
        row = self.getRow(player)
        # Adding label for current player name
        widget = self.table.cellWidget(row, 3)
        if not player.error == None:
            widget.setText(player.error)
            widget.setAlignment(QtCore.Qt.AlignCenter)
        else:
            widget.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            widget.setText(player.name)
        # Adding label for the last time this player was active
        widget = self.table.cellWidget(row, 4)
        if not player.error == None:
            widget.setText(None)
            widget.setColor(None)
        else:
            widget.setText(player.active)
            widget.setColor(player.getActiveColor())
        # Setting row color b ased on current name
        if player.error == None:
            current = self.__parseTextFromHTML(player.name)
            # Setting row color for anonymous players
            if current == "Anonymous Player".lower():
                self.table.setRowColor(row, "dark-grey")
                return
            # Setting row color if current name equals to a stored one
            nick = self.__parseTextFromHTML(player["nick"])
            description = self.__parseTextFromHTML(player["description"])
            if current in nick or current in description or (nick in current) or (description in current and len(description) > 0):
                self.table.setRowColor(row, "dark-blue")
            else:
                self.table.setRowColor(row)
    

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
            self.refreshButton.setIcon("msc.chrome-close")
            self.refreshButton.setBackground("orange")
        else:
            self.refreshButton.setIcon("mdi6.reload")
            self.refreshButton.setBackground("yellow")
    

    def openPlayerInfo(self, player: Player, mode: PlayerInfoViewMode = PlayerInfoViewMode.Load):
        """Opens PlayerInfo window if it doen't exist

        Args:
            player (Player): Player instance
            mode (PlayerInfoViewMode): View mode
        """
        if player.window is None:
            player.window = PlayerInfo(self, player, mode)
            player.window.destroyed.connect(lambda: self.__deletePlayerInfo(player))
            if mode == PlayerInfoViewMode.Add:
                self.addButton.setEnabled(False)
                player.window.destroyed.connect(lambda: self.addButton.setEnabled(True))
        else:
            player.window.raise_()
            player.window.activateWindow()
            if mode == PlayerInfoViewMode.Edit:
                player.window.edit()
    

    def __openGameInfo(self):
        """Opens GameInfo window
        """
        if self.gameInfo is None:
            self.gameInfo = GameInfo(self)
            self.gameInfo.destroyed.connect(self.__deleteGameInfo)
        else:
            self.gameInfo.raise_()
            self.gameInfo.activateWindow()
    

    def __deleteGameInfo(self):
        """Deletes GameInfo window
        """
        self.gameInfo = None
    

    def __getOpenWindowCount(self):
        """Counts currently open PlayerInfo windows
        """
        openWindowCount = 0
        for player in self.players:
            if player.window is not None:
                openWindowCount += 1
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
            for column in range(0, 4):
                widget = self.table.cellWidget(row, column)
                if not widget == None and type(widget) == ColoredLabel:
                    # Checking if this label contins HTML
                    labelText = self.__parseTextFromLabel(widget)
                    if text.lower() in labelText:
                        containsText = True
                        break
            self.table.setRowHidden(row, not containsText)
    

    def __parseTextFromLabel(self, widget: ColoredLabel) -> str:
        """Returns string with widget text contents without HTML tags

        Args:
            widget (ColoredLabel): Rich text label

        Returns:
            str: Parsed label contents
        """
        return self.__parseTextFromHTML(widget.text())
    

    def __parseTextFromHTML(self, text: str) -> str:
        """Returns parsed text from a string with HTML

        Args:
            text (str): Rich text (HTML)

        Returns:
            str: Parsed text without HTML
        """
        self.__doc.setHtml(text)
        return self.__doc.toPlainText().lower()
    
    
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
    

    def removePlayer(self, player: Player):
        """Attempts to remove a player

        Args:
            player (Player): Player instance
        """
        if self.worker is None or not self.worker.isRunning():
            try:
                answer = QtWidgets.QMessageBox.question(self, 'XonStat player tracker', "Are you sure you want to delete player \n" \
                    + "\"" + player["nick"] + "\" (ID " + str(player["id"]) + ") ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
                if answer == QtWidgets.QMessageBox.Yes:
                    self.worker = OverviewRemover(self, player)
                    self.worker.start()
            except:
                self.status.resultMessage("An error occured while removing \"" + player["nick"] + "\" (ID " + str(player["id"]) + ")", False)
                setButtonsEnabled("delete", True)
                printException()

    
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
        # Closing other windows
        for window in QtWidgets.QApplication.topLevelWidgets():
            if type(window) == GameInfo or (type(window) == PlayerInfo and window.mode == PlayerInfoViewMode.Add):
                window.close()
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
        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter or ((event.modifiers() & QtCore.Qt.ControlModifier) and key == QtCore.Qt.Key_F):
            self.searchBar.setFocus()
        elif key == QtCore.Qt.Key_Escape:
            self.searchBar.clear()
            self.searchBar.setFocus()
        # Loading players
        elif (key == QtCore.Qt.Key_R and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier) or key == QtCore.Qt.Key_F5:
            self.__updatePlayers()