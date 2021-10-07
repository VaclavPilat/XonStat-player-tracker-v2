from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QMessageBox
from Window import *
from Status import *
from OverviewWorkers import *
from ColoredWidgets import *
from Player import *



class AddPlayer(Window):
    """Class for creating a new "dialog window" for adding new players 
    """


    def __init__(self, window: Window):
        """Initialising GUI

        Args:
            window (Window): Overview window instance
        """
        super().__init__()
        self.window = window
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Add new player")
        self.setFixedSize(400, 150)
    

    def createLayout(self):
        """Creates widnow layout with widgets
        """
        # Creating the layout itself
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding widgets to layout
        self.id = QLineEdit(self)
        self.id.setPlaceholderText("Player ID")
        layout.addWidget(self.id)
        self.nick = QLineEdit(self)
        self.nick.setPlaceholderText("Player nickname")
        layout.addWidget(self.nick)
        self.addButton = ColoredButton(self, "Add player", "green")
        self.addButton.clicked.connect(self.__tryAddPlayer)
        layout.addWidget(self.addButton)
        # Adding status
        layout.addStretch()
        self.status = Status(self)
        layout.addWidget(self.status)
    

    def __tryAddPlayer(self):
        """Attempts to add a new player
        """
        if not self.addButton.isEnabled():
            return
        id = self.id.text()
        nick = self.nick.text()
        # Checking input validity
        if id == None or id == "" or nick == None or nick == "":
            self.status.resultMessage("Both ID and nickname cannot be empty", False)
            return
        if id.isnumeric():
            id = int(id)
        else:
            self.status.resultMessage("Player ID has to be a number", False)
            return
        # Checking if the ID is already in use
        exists = False
        for player in self.window.players:
            if player["id"] == id:
                exists = True
                break
        if exists:
            self.status.resultMessage("This ID is already being used", False)
            return
        # Adding the player
        self.__addPlayer(id, nick)
    

    def __addPlayer(self, id: int, nick: str):
        """Adds new player to table

        Args:
            id (int): Player ID
            nick (str): Player nickname
        """
        self.addButton.setEnabled(False)
        self.status.message("Adding new player into table")
        player = Player({ "id": id, "nick": nick })
        self.worker = OverviewAdder(self.window, player)
        self.worker.start()
        self.close()
    

    def closeEvent(self, event):
        """Event called right before closing

        Args:
            event: Event
        """
        super().closeEvent(event)
        self.window.addButton.setEnabled(True)
        self.window.refreshButton.setEnabled(True)
    

    def keyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.__tryAddPlayer()
        elif key == Qt.Key_Escape:
            self.close()