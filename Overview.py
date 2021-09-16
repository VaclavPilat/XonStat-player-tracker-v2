#!/usr/bin/env python3
import sys, os, json
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from WindowWithStatus import *

class Oveview(WindowWithStatus):
    """ Class for creating a window that contains a table with currently tracked players """


    players_filename = "Players.json" # JSON file for storing players
    players = [] # List of players


    def __init__(self):
        super().__init__()
        self._set_window_properties()
        self._create_window_layout()
        self.show()
    

    def _set_window_properties(self):
        """ Setting winow properties """
        # Setting window title and size
        self.setWindowTitle("XonStat player tracker - Overview")
        self.resize(1200, 800)
        # Moving window to the center of the screen
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())
    

    def _create_window_layout(self):
        """ Creates widnow layout with widgets """
        # Creating the layout itself
        self.window_layout = QVBoxLayout()
        self.setLayout(self.window_layout)
        # Adding widgets to layout
        self.window_layout.addWidget(self._create_player_table())
        self.window_layout.addWidget(self._status_create())


    def _load_players(self):
        """ Loads players from file """
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, self.players_filename) # Absolute path to the file with players
        # Opening file
        if os.path.isfile(absolute_filepath):
            players_file = open(absolute_filepath, "r")
            self.players = json.loads(players_file.read())
            players_file.close()
        else:
            pass

    
    def _add_players_to_table(self):
        """ Adds rows filled with player data to table """
        if not self.players == []:
            self.player_table.setRowCount( len(self.players) )
            i = 0
            for player in self.players:
                self.player_table.setItem(i, 0, QTableWidgetItem(str(player["id"])))
                self.player_table.setItem(i, 1, QTableWidgetItem(player["nick"]))
                i += 1


    def _create_player_table(self) -> QTableWidget:
        """ Creating table of players """
        self.player_table = QTableWidget()
        # Setting columns
        table_headers = ["ID", "Player nickname", "Current player name", "Last played", 
                        "Player profile", "More information", "Delete player"]
        self.player_table.setColumnCount( len(table_headers) )
        self.player_table.setHorizontalHeaderLabels(table_headers)
        # Filling the table with data
        self._load_players()
        self._add_players_to_table()
        # Enabling horizontal stretching
        self.player_table.horizontalHeader().setStretchLastSection(True)
        self.player_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return self.player_table
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    overview = Oveview()
    sys.exit(app.exec_())