#!/usr/bin/env python3
from WindowWithStatus import *

class AddPlayer(WindowWithStatus):
    """ Class for creating a new "dialog window" for adding new players """

    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Initialising GUI """
        self._window = window
        # GUI
        self.setWindowModality(Qt.ApplicationModal)
        self._set_window_properties()
        self._create_window_layout()
        self.show()
    

    def _set_window_properties(self):
        """ Setting winow properties """
        self.setWindowTitle("XonStat player tracker - Add new player")
        self.resize(400, 150)
        self._center_window()
    

    def closeEvent(self, event):
        """ Event called right before closing """
        self._window.refresh_button.setEnabled(True)
    

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
        window_layout.addWidget(self.add_button)
        # Adding status
        window_layout.addStretch()
        window_layout.addWidget(self._status_create())