#!/usr/bin/env python3
from PyQt5.QtCore import QThread
from WindowWithStatus import *
import sys, os, json, time
from Player import *

class OverviewWorker(QThread):
    """ Worker thread for Overview window """


    players_filename = "Players.json" # JSON file for storing players
    players = [] # List of players

    signal_add_player = pyqtSignal(Player) # Singnal for adding new player to table
    signal_update_player = pyqtSignal(Player) # Singnal for updating player variables


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        self.window = window
        self.signal_add_player.connect(self.window.add_player_to_table)
        self.signal_update_player.connect(self.window.update_player_variables)
        

    def load_players(self):
        """ Loads players from file """
        self.window.status_change_message("Loading players from file")
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, self.players_filename) # Absolute path to the file with players
        # Opening file
        if os.path.isfile(absolute_filepath):
            players_file = open(absolute_filepath, "r")
            for player_dict in json.loads(players_file.read()):
                player_instance = Player(player_dict)
                self.players.append(player_instance)
            players_file.close()

    
    def add_players_to_table(self):
        """ Adds rows filled with player data to table """
        if not self.players == []:
            for player in self.players:
                self.signal_add_player.emit(player)
        if len(self.players) > 0:
            self.window.status_result_message("Successfully loaded " + str(len(self.players)) + " players from file")
        else: 
            self.window.status_result_message("No stored players were found")
    

    def update_player_variables(self):
        """ Loading all player profiles and printing out player variables """
        self.window.refresh_button.setEnabled(False)
        self.window.add_button.setEnabled(False)
        time.sleep(1)
        correct = 0
        current = 0
        self.window.status_change_message("Loading information from player profiles")
        self.window.status_update_progress(current, len(self.players))
        for player in self.players:
            time.sleep(0.3)
            player.load_profile()
            player.load_name()
            player.load_active()
            if player.correct:
                correct += 1
            current += 1
            self.signal_update_player.emit(player)
            self.window.status_update_progress(current, len(self.players))
        self.window.status_result_progress("Finished loading player profiles", correct, len(self.players))
        self.window.refresh_button.setEnabled(True)
        self.window.add_button.setEnabled(True)


    def run(self):
        # Filling the table with data
        self.load_players()
        self.add_players_to_table()
        self.update_player_variables()