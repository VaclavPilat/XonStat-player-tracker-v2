from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTextEdit
from PyQt5.QtGui import QPixmap
from Window import *
from Status import *
from ColoredWidgets import *
from Player import *
from PlayerInfoWorker import *
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
        self.resize(500, 700)
    

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
        layout.addWidget(self.__createTable())
        # Adding status
        self.status = Status(self)
        layout.addWidget(self.status)


    def __createTable(self) -> QTableWidget:
        """Creating table layout

        Returns:
            QTableWidget: Created table widget
        """
        # Setting up a table
        self.table = ColoredTable(self)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        # Adding headers to table
        self.__addWidgetsToTable()
        return self.table
    

    def __addWidgetsToTable(self):
        """Adding widgets to QTableView widget
        """
        headers = ["Current player name", "Playing since", "Last active", "Total time spent", "Games played this week", 
            "Recently used names", "Activity heatmap"]
        for header in headers:
            rowIndex = self.table.rowCount()
            self.table.insertRow(rowIndex)
            self.table.setCellWidget(rowIndex, 0, ColoredLabel(self.table, header, "dark-grey"))
        # Adding widgets to table
        self.name = ColoredLabel(self.table, None, "dark-grey")
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
        self.names = QTextEdit(self.table)
        self.names.setLineWrapMode(QTextEdit.NoWrap)
        self.names.setReadOnly(True)
        self.table.setCellWidget(5, 1, self.names)
        self.heatmap = ColoredLabel(self.table, None, "dark-grey")
        self.heatmap.setFixedSize(300, 200)
        self.table.setCellWidget(6, 1, self.heatmap)
    

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
    

    def showHeatmap(self, pixmap: QPixmap):
        """Shows heatmap image

        Args:
            pixmap (QPixmap): Pixmap of heatmap image
        """
        self.heatmap.setPixmap(pixmap)