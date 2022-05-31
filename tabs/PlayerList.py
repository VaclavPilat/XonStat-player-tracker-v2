from PyQt5 import QtWidgets, QtGui

from tabs.Tab import *
from widgets.ColoredWidgets import *
from widgets.ColoredButtons import *
from workers.PlayerListWorker import *
from misc.Functions import *


class PlayerList(Tab):
    """Class for a showing list of currently tracked players
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Player List"
        # TextDocument class for parsing text from HTML
        self.__doc = QtGui.QTextDocument()
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by player ID, nickname, description or current player name")
        self.searchBar.textChanged.connect(self.__search)
        self.layout.addWidget(self.searchBar)
        # Creating table for tracked players
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
        self.layout.addWidget(self.table)

    
    def addPlayer(self, player: dict, row: int = -1):
        """Adds a single row with player data to table

        Args:
            player (dics): Player info
        """
        if row < 0:
            row = self.table.rowCount()
        # Creating a new row inside the table
        self.table.insertRow(row)
        # Adding labels
        for i in range(5):
            self.table.setCellWidget(row, i, ColoredLabel(self.table, "", "dark-grey"))
        # Adding label text
        self.table.cellWidget(row, 0).setText(str(player["id"]))
        self.table.cellWidget(row, 1).setText(player["nick"])
        self.table.cellWidget(row, 2).setText(player["description"])
        # Adding buttons
        actions = ColoredWidget()
        actions.setBackground("dark-grey")
        buttonGroup = QtWidgets.QHBoxLayout()
        actions.setLayout(buttonGroup)
        buttonGroup.setContentsMargins(0, 0, 0, 0)
        buttonGroup.setSpacing(0)
        buttonGroup.addStretch()
        # Profile button
        profileButton = BrowserButton(self.table)
        buttonGroup.addWidget(profileButton)
        # PlayerInfo button
        infoButton = WindowButton(self.table)
        buttonGroup.addWidget(infoButton)
        # Stacked widget with edit and save button
        editButton = EditButton(self.table)
        buttonGroup.addWidget(editButton)
        # Delete button
        deleteButton = DeleteButton(self.table)
        buttonGroup.addWidget(deleteButton)
        buttonGroup.addStretch()
        self.table.setCellWidget(row, 5, actions)


    def removePlayer(self, row: int):
        """Removes a row by index

        Args:
            row (int): Row index
        """
        self.table.removeRow(row)

    
    def updatePlayer(self, row: int, data: dict):
        """Fills in loaded player data

        Args:
            row (int): Row index
            data (dict): Player data in JSON
        """
        # Showing nick
        nick = processNick( data["player"]["nick"] )
        self.table.cellWidget(row, 3).setText(nick)
        # Showing the last time the player was active
        active = data["overall_stats"]["overall"]["last_played_fuzzy"]
        self.table.cellWidget(row, 4).setText(active)
        self.table.cellWidget(row, 4).setColor(getActiveColor(active))
        # Setting row color
        nick = parseTextFromHTML(nick)
        name = parseTextFromHTML( self.table.cellWidget(row, 1).text() )
        description = parseTextFromHTML( self.table.cellWidget(row, 2).text() )
        if nick in name or name in nick or nick in description or (description in nick and len(description) > 0):
            self.table.setRowColor(row, "dark-blue")
        else:
            self.table.setRowColor(row, None)
    

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
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None or (self.worker.isFinished() and not self.worker.isRunning()):
            self.worker = PlayerListWorker(self)
            self.worker.start()
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Setting focus to search bar
            if key == QtCore.Qt.Key_F:
                self.searchBar.setFocus()
                self.searchBar.selectAll()