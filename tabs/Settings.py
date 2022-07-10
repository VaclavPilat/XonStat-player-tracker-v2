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
        self.searchBar.setPlaceholderText("Search by setting name, type or value")
        self.searchBar.textChanged.connect(self.__search)
        self.layout.addWidget(self.searchBar)
        # Creating table for tracked players
        self.table = ColoredTable(self)
        # Setting columns
        headers = ["Name", "Type", "Value"]
        self.table.setColumnCount( len(headers) )
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
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
        self.table.setCellWidget(row, 2, QtWidgets.QLineEdit(str(value), self.table))
        self.table.cellWidget(row, 2).textChanged.connect(self.showWaitingMessage)
        self.table.cellWidget(row, 2).editingFinished.connect(self.saveSettings)
    

    def showWaitingMessage(self):
        """Showing a message that the app is waiting for th user to make changes
        """
        self.status.message("Waiting for editing to finish (press Enter to save)")


    def saveSettings(self):
        """Attempts to save settings
        """
        newSettings = Config.instance()["Settings"].copy()
        row = 0
        try:
            for row in range(self.table.rowCount()):
                settingName = list(newSettings.keys())[row]
                settingType = type(newSettings[settingName])
                settingValue = self.table.cellWidget(row, 2).text()
                if settingType == int:
                    newSettings[settingName] = int(settingValue)
                elif settingType == float:
                    newSettings[settingName] = float(settingValue)
                elif settingType == bool:
                    if settingValue.lower() == "true":
                        newSettings[settingName] = True
                    elif settingValue.lower() == "false":
                        newSettings[settingName] = False
                    else:
                        raise
                self.table.setRowColor(row)
        except:
            self.table.setRowColor(row, "dark-red")
            self.status.resultMessage("Invalid value(s) prevents from saving", False)
        else:
            self.status.message("Saving settings")
            Config.instance()["Settings"] = newSettings
            if Config.instance().save("Settings"):
                self.status.resultMessage("Settings saved successfully", True)
            else:
                self.status.resultMessage("An error occured when saving settings", False)


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