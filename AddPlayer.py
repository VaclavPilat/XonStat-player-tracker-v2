#!/usr/bin/env python3
from WindowWithStatus import *
from Player import *
import json

class AddPlayer(WindowWithStatus):
    """ Class for creating a new "dialog window" for adding new players """

    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Initialising GUI """
        self._window = window
        # GUI
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._set_window_properties()
        self._create_window_layout()
        self.show()
    

    def _set_window_properties(self):
        """ Setting winow properties """
        self.setWindowTitle("XonStat player tracker - Add new player")
        self.setFixedSize(400, 150)
        self._center_window()
    

    def _create_window_layout(self):
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
        window_layout.addWidget(self._status_create())
    

    def _try_add(self):
        """ Attempt to add a new player """
        if not self.add_button.isEnabled():
            return
        id = self.id.text()
        nick = self.nick.text()
        # Checking input validity
        if id == None or id == "" or nick == None or nick == "":
            self.status_result_message("Both ID and nickname cannot be empty", False)
            return
        if id.isnumeric():
            id = int(id)
        else:
            self.status_result_message("Player ID has to be a number", False)
            return
        # Checking if the ID is already in use
        exists = False
        for player in self._window.players:
            if player["id"] == id:
                exists = True
                break
        if exists:
            self.status_result_message("This ID is already being used", False)
            return
        # Adding the player
        self._add(id, nick)
    

    def _add(self, id: int, nick: str):
        """ Adds new player to table """
        self.add_button.setEnabled(False)
        self.status_change_message("Adding new player into table")
        player = Player({ "id": id, "nick": nick })
        print(json.dumps(player, sort_keys=False, indent=4))
    

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