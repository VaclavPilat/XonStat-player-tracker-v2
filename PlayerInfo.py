from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTextEdit
from PyQt5.QtGui import QPixmap
from Window import *
from Status import *
from ColoredWidgets import *
from Player import *
from PlayerInfoWorker import *
from Config import *
import os



class PlayerInfo(Window):
    """Class for showing detailed information about players
    """


    def __init__(self, player: Player):
        """Initialising GUI

        Args:
            player (Player): Player instance
        """
        self.__usedNames = {}
        self.__gamesPlayed = 0
        self.player = player
        super().__init__()
        self.worker = PlayerInfoWorker(self)
        self.worker.start()
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowTitle("Player information")
        self.resize(550, 700)
    

    def createLayout(self):
        """Creates widnow layout with widgets
        """
        # Creating the layout itself
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Add player table
        layout.addWidget(self.__createTable())
        # Adding top widgets
        self.__addSimpleInfo()
        # Hiding top widgets
        """
        for i in range(0, 2):
            self.table.setRowHidden(i, True) 
        """
        # Adding the rest of widgets
        self.__addWidgetsToTable()
        # Adding status
        self.status = Status(self)
        layout.addWidget(self.status)
    

    def __addSimpleInfo(self):
        """Creates labels for displaying simple information
        """
        for i in range(3):
            self.table.insertRow(i)
        headers = ["Player ID", "Player nickname", "Player description"]
        i = 0
        for header in headers:
            self.table.setCellWidget(i, 0, ColoredLabel(self.table, header))
            i += 1
        self.id = ColoredLabel(self, str(self.player["id"]))
        self.table.setCellWidget(0, 1, self.id)
        self.nick = ColoredLabel(self, self.player["nick"])
        self.table.setCellWidget(1, 1, self.nick)
        self.description = ColoredLabel(self, self.player["description"])
        self.table.setCellWidget(2, 1, self.description)


    def __createTable(self) -> QTableWidget:
        """Creating table layout

        Returns:
            QTableWidget: Created table widget
        """
        # Setting up a table
        self.table = ColoredTable(self)
        self.table.setColumnCount(2)
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setHorizontalHeaderLabels( ["#" + str(self.player["id"]), self.player["nick"]] )
        self.table.verticalHeader().hide()
        return self.table
    

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
        self.table.setCellWidget(3, 1, self.name)
        self.since = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(4, 1, self.since)
        self.active = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(5, 1, self.active)
        self.time = ColoredLabel(self.table, None, "dark-grey")
        self.table.setCellWidget(6, 1, self.time)
        self.games = ColoredLabel(self.table, None, "dark-grey")
        self.games.setText("0")
        self.table.setCellWidget(7, 1, self.games)
        # Adding heatmap table
        self.table.insertRow(8)
        self.__createHeatmap()
        self.table.setCellWidget(8, 0, self.heatmap, 1, 2)
        # Recently used names
        self.table.insertRow(9)
        self.table.setCellWidget(9, 0, ColoredLabel(self.table, "Recently used names", "dark-grey"))
        self.names = QTextEdit(self.table)
        self.names.setMaximumHeight(150)
        self.names.setProperty("class", "xolonium")
        self.names.setLineWrapMode(QTextEdit.NoWrap)
        self.names.setReadOnly(True)
        self.table.setCellWidget(9, 1, self.names)
    

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