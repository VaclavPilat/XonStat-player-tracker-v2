from PyQt5 import QtWidgets

from tabs.Tab import *
from misc.Functions import *


class TabInfo(Tab):
    """Class for showing player information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Player ID
        """
        self.id = identifier
        super().__init__(parent)
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating input field for player ID
        self.identifierInput = QtWidgets.QLineEdit(self)
        if self.id is not None:
            self.identifierInput.setText(str(self.id))
        else:
            self.identifierInput.setFocus()
        self.identifierInput.textChanged.connect(self.startLoading)
        self.layout.addWidget(self.identifierInput)
        # Creating scroll area
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget(self.scrollArea)
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(self.scrollWidget)
        self.layout.addWidget(self.scrollArea)
    

    def startLoading(self) -> bool:
        """Starting page (re)loading
        """
        # Setting ID
        if self.identifierInput.text() is None or self.identifierInput.text() == "":
            self.id = None
        else:
            self.id = getNumberFromString(self.identifierInput.text())
            if self.id is None:
                self.status.resultMessage("Entered ID is not a number", False)
        # Looking for possible tab duplicates
        for i in range(self.parent.tabWidget.count()):
            if self != self.parent.tabWidget.widget(i) and isinstance(self.parent.tabWidget.widget(i), type(self)):
                if self.id == self.parent.tabWidget.widget(i).id:
                    self.parent.tabWidget.setCurrentIndex(i)
                    self.parent.removeTab(self.parent.tabWidget.indexOf(self))
                    return False
        if self.id == None:
            return False
        return True


    def clearOldInformation(self):
        """Removes old information to make space for new ones
        """
        self.clearInfoTable()
    

    def localKeyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Setting focus to ID input field
            if key == QtCore.Qt.Key_F:
                self.identifierInput.setFocus()
                self.identifierInput.selectAll()
    

    def createInfoTable(self, headings: list) -> ColoredTable:
        """Creates an info table

        Args:
            headings (list): List of headers

        Returns:
            ColoredTable: Created info table
        """
        self.info = ColoredFixedTable(self, False)
        # Setting table headers settings
        self.info.setColumnCount(2)
        self.info.setShowGrid(False)
        for i in range(self.info.columnCount()):
            self.info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.info.verticalHeader().hide()
        # Adding rows
        for heading in headings:
            row = self.info.rowCount()
            self.info.insertRow(row)
            self.info.setCellWidget(row, 0, ColoredLabel(self, heading + ":"))
            self.info.cellWidget(row, 0).setAlignment(QtCore.Qt.AlignRight)
            # Adding content widgets
            widget = ColoredWidget()
            layout = QtWidgets.QHBoxLayout()
            widget.setLayout(layout)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            label = ColoredLabel(self, None, "transparent")
            layout.addWidget(label)
            self.info.setCellWidget(row, 1, widget)
        return self.info
    

    def setInfoContent(self, row: int, text: str):
        """Sets content of a label in info table

        Args:
            row (int): Row index
            text (str): New label content
        """
        self.info.cellWidget(row, 1).layout().itemAt(0).widget().setText(text)
    

    def addInfoContent(self, row: int, text: str):
        """Adds text to a content of a label in info table

        Args:
            row (int): Row index
            text (str): Additional label content
        """
        widget = self.info.cellWidget(row, 1).layout().itemAt(0).widget()
        widget.setText(widget.text() + " " + text)
    

    def clearInfoTable(self):
        """Removes text from content labels in info table
        """
        for i in range(self.info.rowCount()):
            self.setInfoContent(i, "")