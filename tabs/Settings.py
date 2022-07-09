from PyQt5 import QtWidgets, QtCore

from tabs.Tab import *
from workers.SettingsWorker import *


class Settings(Tab):
    """Class for a settings tab
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "Settings"
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating search bar
        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by setting name")
        self.searchBar.textChanged.connect(self.__search)
        self.layout.addWidget(self.searchBar)
        # Creating table for tracked players
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["Name", "Type", "Value"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().hide()
        # Setting column stretching
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.layout.addWidget(self.table)

    
    def addSetting(self, name: str, value):
        """Create a single row with setting

        Args:
            name (str): Setting name
            value (mixed): Setting value
        """
        row = self.table.rowCount()
        # Creating a new row inside the table
        self.table.insertRow(row)
        # Adding widgets
        self.table.setCellWidget(row, 0, ColoredLabel(self.table, name))
        self.table.setCellWidget(row, 1, ColoredLabel(self.table, type(value).__name__))
        self.table.setCellWidget(row, 2, ColoredLabel(self.table, str(value)))


    def clearOldInformation(self):
        """Removes old information to make space for new ones
        """
        self.table.setRowCount(0)
    

    def __search(self, text: str):
        """Hiding and showing rows in the table based on input

        Args:
            text (str): Serched text
        """
        for row in range(self.table.rowCount()):
            containsText = False
            for column in range(0, self.table.columnCount()):
                widget = self.table.cellWidget(row, column)
                if not widget == None and type(widget) == ColoredLabel:
                    # Checking if this label contins HTML
                    labelText = parseTextFromHTML(widget.text())
                    if text.lower() in labelText:
                        containsText = True
                        break
            self.table.setRowHidden(row, not containsText)
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = SettingsWorker(self)
        if self.worker.isFinished() or not self.worker.isRunning():
            self.worker.start()
    

    def localKeyPressEvent(self, event):
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