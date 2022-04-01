from PyQt5 import QtWidgets, QtCore, QtGui
import os, enum

from Window import *
from Status import *
from ColoredWidgets import *
from Player import *
from PlayerInfoWorker import *
from Config import *
from OverviewWorkers import *



class PlayerInfoViewMode(enum.Enum):
    Load = 0
    Edit = 1
    Add = 2



class PlayerInfo(Window):
    """Class for showing detailed information about players
    """


    def __init__(self, overview, player: Player, mode: PlayerInfoViewMode = PlayerInfoViewMode.Load):
        """Initialising GUI

        Args:
            overview (Overview): Overview window instance
            player (Player): Player instance
            mode (PlayerInfoViewMode): View mode
        """
        self.__usedNames = {}
        self.__gamesPlayed = 0
        self.editing = False
        self.overview = overview
        self.player = player
        self.mode = mode
        super().__init__()
        if self.mode == PlayerInfoViewMode.Load:
            self.worker = PlayerInfoWorker(self)
            self.worker.start()
        elif self.mode == PlayerInfoViewMode.Edit or self.mode == PlayerInfoViewMode.Add:
            self.edit()
        if not self.mode == PlayerInfoViewMode.Load:
            self.__setEditEnabled()
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowTitle("Player information")
        if self.mode ==PlayerInfoViewMode.Load:
            self.resize(550, 700)
        else:
            self.resize(550, 180)
    

    def createLayout(self):
        """Creates window layout with widgets
        """
        # Creating the layout itself
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding simple information
        self.info = self.__createTable()
        self.info.setMaximumHeight(130)
        self.info.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.info.resizeRowsToContents()
        self.info.setShowGrid(False)
        self.__addSimpleInfo()
        layout.addWidget(self.info)
        # Adding the rest of widgets
        if self.mode == PlayerInfoViewMode.Load:
            self.table = self.__createTable()
            self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.__addWidgetsToTable()
            layout.addWidget(self.table)
        # Adding status
        if not self.mode == PlayerInfoViewMode.Load:
            layout.addStretch()
        self.status = Status(self)
        layout.addWidget(self.status)
    

    def __addSimpleInfo(self):
        """Creates labels for displaying simple information
        """
        for i in range(4):
            self.info.insertRow(i)
        headers = ["Player ID", "Player nickname", "Player description"]
        i = 0
        for header in headers:
            self.info.setCellWidget(i, 0, ColoredLabel(self.info, header))
            self.info.cellWidget(i, 0).setProperty("class", "right")
            i += 1
        # Adding editable text fields
        self.id = ColoredLabel(self.info, str(self.player["id"]))
        self.info.setCellWidget(0, 1, self.id)
        self.nick = ColoredLabel(self.info, self.player["nick"])
        self.nick.setProperty("class", "xolonium")
        self.info.setCellWidget(1, 1, self.nick)
        self.description = ColoredLabel(self.info, self.player["description"])
        self.description.setProperty("class", "xolonium")
        self.info.setCellWidget(2, 1, self.description)
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Profile button
        if self.mode == PlayerInfoViewMode.Load:
            profileButton = ColoredButton(self.info, "ri.file-user-fill", "blue")
            profileButton.clicked.connect(self.player.showProfile)
            buttonGroup.addWidget(profileButton)
        # PlayerInfo button
        if self.mode == PlayerInfoViewMode.Load:
            self.refreshButton = ColoredButton(self.info)
            self.refreshButton.clicked.connect(self.__refresh)
            buttonGroup.addWidget(self.refreshButton)
            self.updateRefreshButton()
        # Edit button
        self.editButton = ColoredButton(self.info)
        self.editButton.setObjectName("edit-" + str(self.player["id"]))
        self.editButton.clicked.connect(self.edit)
        buttonGroup.addWidget(self.editButton)
        self.updateEditButton()
        # Delete button
        if self.mode == PlayerInfoViewMode.Load:
            deleteButton = ColoredButton(self.info, "fa5s.trash-alt", "red")
            deleteButton.setObjectName("delete")
            deleteButton.clicked.connect(self.__removePlayer)
            buttonGroup.addWidget(deleteButton)
        # Close button
        if not self.mode == PlayerInfoViewMode.Load:
            closeButton = ColoredButton(self.info, "msc.chrome-close", "red")
            closeButton.clicked.connect(self.close)
            buttonGroup.addWidget(closeButton)
        buttonGroup.addStretch()
        self.info.setCellWidget(3, 0, actions, 1, 2)


    def __createTable(self) -> QtWidgets.QTableWidget:
        """Creating table layout

        Returns:
            QtWidgets.QTableWidget: Created table widget
        """
        # Setting up a table
        table = ColoredTable(self)
        table.setColumnCount(2)
        for i in range(table.columnCount()):
            table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        return table
    

    def __addWidgetsToTable(self):
        """Adding widgets to QTableView widget
        """
        headers = ["Current player name", "Playing since", "Last active", "Total time spent", 
            "Games in last 7 days [UTC]"]
        for header in headers:
            rowIndex = self.table.rowCount()
            self.table.insertRow(rowIndex)
            self.table.setCellWidget(rowIndex, 0, ColoredLabel(self.table, header, "dark-grey"))
        # Adding widgets to table
        widget = ColoredWidget()
        widget.setBackground("dark-grey")
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.name = ColoredLabel(self.table, None, "transparent")
        self.name.setProperty("class", "xolonium")
        layout.addWidget(self.name)
        copyButton = ColoredButton(self.info, "fa.copy", "blue")
        copyButton.clicked.connect(lambda: QtWidgets.QApplication.instance().clipboard().setText(self.name.text()))
        layout.addWidget(copyButton)
        widget.setLayout(layout)
        self.table.setCellWidget(0, 1, widget)
        self.since = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(1, 1, self.since)
        self.active = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(2, 1, self.active)
        self.time = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(3, 1, self.time)
        self.games = ColoredLabel(self.table, None, "dark-grey")
        self.games.setText("0")
        self.table.setCellWidget(4, 1, self.games)
        # Adding heatmap table
        self.table.insertRow(5)
        self.__createHeatmap()
        self.table.setCellWidget(5, 0, self.heatmap, 1, 2)
        # Recently used names
        self.table.insertRow(6)
        self.table.setCellWidget(6, 0, ColoredLabel(self.table, "Recently used names", "dark-grey"))
        self.names = ColoredTextarea(self.table)
        self.names.setMaximumHeight(150)
        self.names.setProperty("class", "xolonium no-border")
        self.names.setProperty("background", "dark-grey")
        self.names.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.names.setReadOnly(True)
        self.table.setCellWidget(6, 1, self.names)
        # List of recent games
        self.table.insertRow(7)
        self.__createGameList()
        self.table.setCellWidget(7, 0, self.gameList, 1, 2)
    

    def __createHeatmap(self):
        """Creates a heatmap table
        """
        self.heatmap = ColoredTable(self)
        self.heatmap.setBackground("dark-grey")
        self.heatmap.setProperty("class", "heatmap no-border")
        # Generating column headers
        columns = []
        for i in range(0, 24, Config.instance()["Settings"]["heatmapHourSpan"]):
            columns.append(str(i) + "-" + str(i + Config.instance()["Settings"]["heatmapHourSpan"]))
        # Setting columns
        self.heatmap.setColumnCount(len(columns))
        self.heatmap.setHorizontalHeaderLabels(columns)
        self.heatmap.horizontalHeader().setMinimumSectionSize(50)
        self.heatmap.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Generating rows
        self.heatmap.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for i in range(7):
            self.heatmap.insertRow(i)
            for j in range(self.heatmap.columnCount()):
                self.heatmap.setCellWidget(i, j, ColoredLabel(self.heatmap, None, "heatmap-0"))
        self.heatmap.setVerticalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.heatmap.setMinimumHeight(230)
    

    def __createGameList(self):
        """Creates a table with list of recent games
        """
        self.gameList = ColoredTable(self)
        self.gameList.setBackground("dark-grey")
        self.gameList.setProperty("class", "no-border")
        # Generating column headers
        columns = ["Date [UTC]", "Game mode", "Map name", "Actions"]
        # Setting columns
        self.gameList.setColumnCount(len(columns))
        self.gameList.setHorizontalHeaderLabels(columns)
        self.gameList.horizontalHeader().setMinimumSectionSize(30)
        for i in range(3):
            self.gameList.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.gameList.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.gameList.setMinimumHeight(230)
    

    def __removePlayer(self):
        """Attempts to remove player through Overview window instance
        """
        self.overview.removePlayer(self.player)
    

    def __refresh(self):
        """Refreshing player information
        """
        if self.worker is not None:
            if self.worker.isRunning():
                self.worker.cancel = True
                self.refreshButton.setEnabled(False)
            else:
                # Clearing label values
                self.__gamesPlayed = 0
                self.__usedNames.clear()
                self.games.setText("0")
                self.names.setText("")
                self.gameList.setRowCount(0)
                for i in range(self.heatmap.rowCount()):
                    for j in range(self.heatmap.columnCount()):
                        widget = self.heatmap.cellWidget(i, j)
                        widget.setText("")
                        widget.setBackground("heatmap-0")
                # Starting new worker
                self.worker = PlayerInfoWorker(self)
                self.worker.start()
    

    def showRecentGames(self, games: list):
        """Inserts new rows with game data into a gameList table

        Args:
            game (list): Game data list
        """
        for game in games:
            # Creating new row
            self.__showRecentGame(game)
    

    def __showRecentGame(self, game: dict):
        """Showing recent game by creating a new row in gameList table

        Args:
            game (dict): Game info
        """
        row = self.gameList.rowCount()
        if row >= Config.instance()["Settings"]["recentGamesCount"]:
            return
        self.gameList.insertRow(row)
        # Adding cells
        for i in range(3):
            self.gameList.setCellWidget(row, i, ColoredLabel(self.gameList))
        # Setting cell content
        date = datetime.datetime.strptime(game["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = date.strftime("%d.%m.%Y %H:%M:%S")
        self.gameList.cellWidget(row, 0).setText(date_str)
        self.gameList.cellWidget(row, 1).setText(game["game_type_cd"].upper())
        self.gameList.cellWidget(row, 2).setText(game["map_name"])
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Adding button for showing game in gameInfo window
        gameInfoButton = ColoredButton(self.table, "msc.graph", "yellow")
        gameInfoButton.clicked.connect(lambda: self.__openGameInfo(game["game_id"]))
        buttonGroup.addWidget(gameInfoButton)
        #gameInfoButton.clicked.connect(lambda: )
        self.gameList.setCellWidget(row, 3, actions)
        buttonGroup.addStretch()
    

    def __openGameInfo(self, id: int):
        """Opening game info window to view info about a game

        Args:
            id (int): Game id
        """
        self.overview.openGameInfo()
        self.overview.gameInfo.gameID.setText(str(id))
        self.overview.gameInfo.loadGameInfo()
    

    def updateRefreshButton(self):
        """Updates visuals of "Refresh" button
        """
        self.refreshButton.setEnabled(True)
        if self.worker is not None and self.worker.isRunning():
            self.refreshButton.setIcon("msc.chrome-close")
            self.refreshButton.setBackground("orange")
        else:
            self.refreshButton.setIcon("mdi6.reload")
            self.refreshButton.setBackground("yellow")
    

    def __editButtonSave(self, button):
        """Callback function for updating edit buttons to match "save" state

        Args:
            button (ColoredButton): Button object
        """
        button.setIcon("fa.save")
        button.setBackground("green")
    

    def __editButtonEdit(self, button):
        """Callback function for updating edit buttons to match "edit" state

        Args:
            button (ColoredButton): Button object
        """
        button.setIcon("fa5s.pencil-alt")
        button.setBackground("orange")


    def updateEditButton(self):
        """Updates visuals of "Refresh" button
        """
        if self.editing:
            executeCallbackOnButtons("edit-" + str(self.player["id"]), self.__editButtonSave)
        else:
            executeCallbackOnButtons("edit-" + str(self.player["id"]), self.__editButtonEdit)
    

    def showUsedNames(self, name: str):
        """Shows currently used names

        Args:
            name (str): Used name
        """
        # Adding name to dictionary
        if name in self.__usedNames:
            self.__usedNames[name] += 1
        else:
            self.__usedNames[name] = 1
        # Printing out names
        output = ""
        i = 0
        for usedName in self.__usedNames:
            i += 1
            output += usedName + " (" + str(self.__usedNames[usedName]) + ")"
            if not i == len(self.__usedNames):
                output += "<br>"
        self.names.setHtml(output)
    

    def showGames(self):
        """Shows number of games played within the last 7 days
        """
        self.__gamesPlayed += 1
        self.games.setText(str(self.__gamesPlayed) + " (~" + str(int(self.__gamesPlayed / 7)) + " games a day)")
    

    def updateHeatmapGames(self, row: int, column: int):
        """Updating number of games in a selected cell in heatmap

        Args:
            row (int): Row index
            column (int): Column index
        """
        widget = self.heatmap.cellWidget(row, column)
        if widget is not None:
            count = 0
            if len(widget.text()) > 0:
                count = int(widget.text()) + 1
            else:
                count = 1
            widget.setText(str(count))
            if count <= Config.instance()["Colors"]["heatmap"]["count"]:
                widget.setBackground("heatmap-" + str(count))
    

    def edit(self):
        """Editing player info
        """
        if self.editing:
            # Getting edited info
            if self.mode == PlayerInfoViewMode.Add:
                self.player["id"] = int(self.id.text())
            self.player["nick"] = self.nick.text()
            self.player["description"] = self.description.text()
            # Adding new player
            if self.mode == PlayerInfoViewMode.Add:
                self.overview.worker = OverviewAdder(self.overview, self.player)
                self.overview.worker.start()
                self.overview.worker.finished.connect(self.__saveEditedChanges)
            else:
                self.__saveEditedChanges()
            self.editing = False
        else:
            self.editing = True
        # Switching between labels and input fields
        if self.editing:
            if self.mode == PlayerInfoViewMode.Add:
                self.id = QtWidgets.QLineEdit(str(self.player["id"]), self)
                self.id.textChanged.connect(self.__setEditEnabled)
                self.info.setCellWidget(0, 1, self.id)
            self.nick = QtWidgets.QLineEdit(self.player["nick"], self)
            self.nick.textChanged.connect(self.__setEditEnabled)
            self.info.setCellWidget(1, 1, self.nick)
            self.description = QtWidgets.QLineEdit(self.player["description"], self)
            self.description.textChanged.connect(self.__setEditEnabled)
            self.info.setCellWidget(2, 1, self.description)
        else:
            if self.mode == PlayerInfoViewMode.Add:
                self.id = ColoredLabel(self.info, str(self.player["id"]))
                self.info.setCellWidget(0, 1, self.id)
            self.nick = ColoredLabel(self.info, self.player["nick"])
            self.info.setCellWidget(1, 1, self.nick)
            self.description = ColoredLabel(self.info, self.player["description"])
            self.info.setCellWidget(2, 1, self.description)
        self.nick.setProperty("class", "xolonium")
        self.description.setProperty("class", "xolonium")
        self.updateEditButton()
    

    def __saveEditedChanges(self):
        """Saves edited player information
        """
        # Setting edited info to Overview
        row = self.overview.getRow(self.player)
        if self.mode == PlayerInfoViewMode.Add:
            self.overview.table.cellWidget(row, 0).setText(str(self.player["id"]))
        self.overview.table.cellWidget(row, 1).setText(self.player["nick"])
        self.overview.table.cellWidget(row, 2).setText(self.player["description"])
        # Saving edited info to file
        Config.instance()["Players"] = json.loads( json.dumps(self.overview.players) )
        if Config.save("Players"):
            self.status.resultMessage("Saved player information", True)
        else:
            self.status.resultMessage("An error occured while saving player information", False)
        if self.mode == PlayerInfoViewMode.Edit:
            self.close()
        elif self.mode == PlayerInfoViewMode.Add:
            self.destroyed.connect(lambda: self.overview.openPlayerInfo(self.player))
            self.close()
    

    def __setEditEnabled(self):
        """Setting edit button "enabled" property based on input validity
        """
        self.editButton.setEnabled(self.__validateInputs())
    

    def __validateInputs(self):
        """Setting edit button "enabled" property based on input validity
        """
        # ID
        id = self.id.text()
        nick = self.nick.text()
        # Checking input validity
        if (id is None or id == "") and (nick is None or nick == ""):
            self.status.message("Waiting for inputs")
            return False
        else:
            if id is None or id == "" or nick is None or nick == "":
                self.status.resultMessage("Both ID and nickname cannot be empty", False)
                return False
            if id.isnumeric():
                id = int(id)
            else:
                self.status.resultMessage("Player ID has to be a number", False)
                return False
            # Checking if the ID is already in use
            for player in self.overview.players:
                if self.mode == PlayerInfoViewMode.Add and player["id"] == id:
                    self.status.resultMessage("This ID is already being used", False)
                    return False
            self.status.resultMessage("Ready to save player information", True)
        return True
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        # Closing window
        if key == QtCore.Qt.Key_Escape:
            self.close()
        # Loading players
        elif (key == QtCore.Qt.Key_R and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier) or key == QtCore.Qt.Key_F5:
            self.__refresh()
    

    def closeEvent(self, event):
        """Synchronizing information before closing the window

        Args:
            event: Closing event
        """
        self.editing = False
        self.updateEditButton()
        super().closeEvent(event, True)