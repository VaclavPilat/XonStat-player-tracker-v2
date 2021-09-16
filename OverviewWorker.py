#!/usr/bin/env python3
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from WindowWithStatus import *
import sys, os, json, time

class OverviewWorker(QThread):
    """ Worker thread for Overview window """


    players_filename = "Players.json" # JSON file for storing players
    players = [] # List of players

    signal_add_player = pyqtSignal(dict) # Singnal for adding new player to table


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        self.window = window
        self.signal_add_player.connect(self.window.add_player_to_table)


    def _load_players(self):
        """ Loads players from file """
        self.window.status_change_message("Loading players from file...")
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, self.players_filename) # Absolute path to the file with players
        # Opening file
        if os.path.isfile(absolute_filepath):
            players_file = open(absolute_filepath, "r")
            self.players = json.loads(players_file.read())
            players_file.close()

    
    def _add_players_to_table(self):
        """ Adds rows filled with player data to table """
        if not self.players == []:
            for player in self.players:
                self.signal_add_player.emit(player)
        if len(self.players) > 0:
            self.window.status_result_message("Successfully loaded " + str(len(self.players)) + " players from file.")
        else: 
            self.window.status_result_message("No stored players were found.")


    def run(self):
        # Filling the table with data
        self._load_players()
        self._add_players_to_table()
