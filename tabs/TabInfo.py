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
        self.info = ColoredTable(self)
        # Setting table headers settings
        self.info.setColumnCount(2)
        self.info.setShowGrid(False)
        self.info.horizontalHeader().hide()
        for i in range(self.info.columnCount()):
            self.info.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.info.verticalHeader().hide()
        self.info.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        # Setting fixed table height
        self.info.setMaximumHeight(self.info.rowCount() * 30)
        return self.info