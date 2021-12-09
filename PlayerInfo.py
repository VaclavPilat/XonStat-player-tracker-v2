from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTextEdit, QLineEdit
from PyQt5.QtGui import QPixmap
from Window import *
from Status import *
from ColoredWidgets import *
from Player import *
from PlayerInfoWorker import *
from Config import *
from OverviewWorkers import *
import os, enum



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
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding simple information
        self.info = self.__createTable()
        self.info.setMaximumHeight(130)
        self.info.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.info.resizeRowsToContents()
        self.info.setShowGrid(False)
        self.__addSimpleInfo()
        layout.addWidget(self.info)
        # Adding the rest of widgets
        if self.mode == PlayerInfoViewMode.Load:
            self.table = self.__createTable()
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
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
        self.id = QLineEdit(str(self.player["id"]), self)
        self.id.setEnabled(False)
        self.id.textChanged.connect(self.__setEditEnabled)
        self.info.setCellWidget(0, 1, self.id)
        self.nick = QLineEdit(self.player["nick"], self)
        self.nick.setEnabled(False)
        self.nick.textChanged.connect(self.__setEditEnabled)
        self.info.setCellWidget(1, 1, self.nick)
        self.description = QLineEdit(self.player["description"], self)
        self.description.setEnabled(False)
        self.description.textChanged.connect(self.__setEditEnabled)
        self.info.setCellWidget(2, 1, self.description)
        # Adding buttons
        actions = ColoredWidget()
        buttonGroup = QHBoxLayout()
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
        self.editButton.clicked.connect(self.edit)
        buttonGroup.addWidget(self.editButton)
        self.updateEditButton()
        # Delete button
        if self.mode == PlayerInfoViewMode.Load:
            deleteButton = ColoredButton(self.info, "fa5s.trash-alt", "red")
            deleteButton.clicked.connect(self.__removePlayer)
            buttonGroup.addWidget(deleteButton)
        # Close button
        if not self.mode == PlayerInfoViewMode.Load:
            closeButton = ColoredButton(self.info, "msc.chrome-close", "red")
            closeButton.clicked.connect(self.close)
            buttonGroup.addWidget(closeButton)
        buttonGroup.addStretch()
        self.info.setCellWidget(3, 0, actions, 1, 2)


    def __createTable(self) -> QTableWidget:
        """Creating table layout

        Returns:
            QTableWidget: Created table widget
        """
        # Setting up a table
        table = ColoredTable(self)
        table.setColumnCount(2)
        for i in range(table.columnCount()):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
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
        self.name = ColoredLabel(self.table, None, "dark-grey")
        self.name.setProperty("class", "xolonium")
        self.table.setCellWidget(0, 1, self.name)
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
        self.names = QTextEdit(self.table)
        self.names.setMaximumHeight(150)
        self.names.setProperty("class", "xolonium")
        self.names.setLineWrapMode(QTextEdit.NoWrap)
        self.names.setReadOnly(True)
        self.table.setCellWidget(6, 1, self.names)
    

    def __createHeatmap(self):
        """Creates a heatmap table
        """
        self.heatmap = ColoredTable(self)
        self.heatmap.setProperty("class", "heatmap")
        # Generating column headers
        columns = []
        for i in range(0, 24, Config.instance()["Settings"]["heatmapHourSpan"]):
            columns.append(str(i) + "-" + str(i + Config.instance()["Settings"]["heatmapHourSpan"]))
        # Setting columns
        self.heatmap.setColumnCount(len(columns))
        self.heatmap.setHorizontalHeaderLabels(columns)
        self.heatmap.horizontalHeader().setMinimumSectionSize(50)
        for i in range(self.heatmap.columnCount()):
            self.heatmap.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Generating rows
        for i in range(7):
            self.heatmap.insertRow(i)
            self.heatmap.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for j in range(self.heatmap.columnCount()):
                self.heatmap.setCellWidget(i, j, ColoredLabel(self.heatmap, None, "heatmap-0"))
        self.heatmap.setVerticalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.heatmap.setMinimumHeight(230)
    

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
                for i in range(self.heatmap.rowCount()):
                    for j in range(self.heatmap.columnCount()):
                        widget = self.heatmap.cellWidget(i, j)
                        widget.setText("")
                        widget.setBackground("heatmap-0")
                # Starting new worker
                self.worker = PlayerInfoWorker(self)
                self.worker.start()
    

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
    

    def updateEditButton(self):
        """Updates visuals of "Refresh" button
        """
        if self.editing:
            self.editButton.setIcon("fa.save")
            self.editButton.setBackground("green")
        else:
            self.editButton.setIcon("fa5s.pencil-alt")
            self.editButton.setBackground("orange")
    

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
            self.status.message("Saving player information")
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
        if self.mode == PlayerInfoViewMode.Add:
            for i in range(3):
                self.info.cellWidget(i, 1).setEnabled(not self.editing)
        else:
            for i in range(1, 3):
                self.info.cellWidget(i, 1).setEnabled(not self.editing)
        self.editing = not self.editing
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
        Config.save("Players")
        self.status.resultMessage("Saved player information", True)
        if self.mode == PlayerInfoViewMode.Edit:
            self.close()
        elif self.mode == PlayerInfoViewMode.Add:
            self.mode = PlayerInfoViewMode.Load
    

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
            if not player == self.player and player["id"] == id:
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
        if key == Qt.Key_Escape:
            self.close()
        # Loading players
        elif (key == Qt.Key_R and QApplication.keyboardModifiers() == Qt.ControlModifier) or key == Qt.Key_F5:
            self.__refresh()