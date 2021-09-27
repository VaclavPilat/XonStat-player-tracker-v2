from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QMessageBox
from Window import *
from Status import *
from OverviewWorkers import *
from Player import *
import json

class AddPlayer(Window):
    """ Class for creating a new "dialog window" for adding new players """

    def __init__(self, window: Window):
        super().__init__()
        """ Initialising GUI """
        self._window = window
    

    def set_window_properties(self):
        """ Setting winow properties """
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("XonStat player tracker - Add new player")
        self.setFixedSize(400, 150)
    

    def create_window_layout(self):
        """ Creates widnow layout with widgets """
        # Creating the layout itself
        window_widget = QWidget()
        window_layout = QVBoxLayout()
        window_widget.setLayout(window_layout)
        self.setCentralWidget(window_widget)
        # Adding widgets to layout
        self.id = QLineEdit(self)
        self.id.setPlaceholderText("Player ID")
        window_layout.addWidget(self.id)
        self.nick = QLineEdit(self)
        self.nick.setPlaceholderText("Player nickname")
        window_layout.addWidget(self.nick)
        self.add_button = QPushButton(self)
        self.add_button.setText("Add player")
        self.add_button.setProperty("background", "green")
        self.add_button.clicked.connect(self._try_add)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        window_layout.addWidget(self.add_button)
        # Adding status
        window_layout.addStretch()
        self.status = Status(self)
        window_layout.addWidget(self.status)
    

    def _try_add(self):
        """ Attempt to add a new player """
        if not self.add_button.isEnabled():
            return
        id = self.id.text()
        nick = self.nick.text()
        # Checking input validity
        if id == None or id == "" or nick == None or nick == "":
            self.status.result_message("Both ID and nickname cannot be empty", False)
            return
        if id.isnumeric():
            id = int(id)
        else:
            self.status.result_message("Player ID has to be a number", False)
            return
        # Checking if the ID is already in use
        exists = False
        for player in self._window.players:
            if player["id"] == id:
                exists = True
                break
        if exists:
            self.status.result_message("This ID is already being used", False)
            return
        # Adding the player
        self._add(id, nick)
    

    def _add(self, id: int, nick: str):
        """ Adds new player to table """
        self.add_button.setEnabled(False)
        self.status.message("Adding new player into table")
        player = Player({ "id": id, "nick": nick })
        self._window.adder = OverviewAdder(self._window, player)
        self._window.adder.start()
        self.close()
    

    def closeEvent(self, event):
        """ Event called right before closing """
        self._window.addplayer_window_closed()
    

    def keyPressEvent(self, event):
        """ Reacts to pressing keys """
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self._try_add()
        elif key == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker')
    addplayer = AddPlayer(None)
    sys.exit(app.exec_())