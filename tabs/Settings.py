from PyQt5 import QtWidgets, QtCore
import qtawesome as qta

from tabs.Tab import *


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
        headers = ["Setting name", "Setting type", "Setting value"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        # Setting column stretching
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.layout.addWidget(self.table)
    

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
                    labelText = parseTextFromHTML(widget.text())
                    if text.lower() in labelText:
                        containsText = True
                        break
            self.table.setRowHidden(row, not containsText)