#!/usr/bin/env python3
from PyQt5.QtCore import QThread
from WindowWithStatus import *
import sys, os, json, time
from Player import *


class OverviewLoader(QThread):
    """ Overview worker QThread for loading players """

    _players_filename = "Players.json" # JSON file for storing players
    _signal_add_player = pyqtSignal(Player) # Signal for adding new player to table


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Init """
        self._window = window
        self._signal_add_player.connect(self._window.add_player_to_table)
        

    def _load_players(self):
        """ Loads players from file """
        self._window.status_change_message("Loading players from file")
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, self._players_filename) # Absolute path to the file with players
        # Opening file
        if os.path.isfile(absolute_filepath):
            players_file = open(absolute_filepath, "r")
            for player_dict in json.loads(players_file.read()):
                player_instance = Player(player_dict)
                self._window.players.append(player_instance)
            players_file.close()

    
    def _add_players_to_table(self):
        """ Adds rows filled with player data to table """
        if not self._window.players == []:
            for player in self._window.players:
                self._signal_add_player.emit(player)
        if len(self._window.players) > 0:
            self._window.status_result_message("Successfully loaded " + str(len(self._window.players)) + " players from file")
        else: 
            self._window.status_result_message("No stored players were found")


    def run(self):
        """ Loading players and adding then into table """
        self._load_players()
        self._add_players_to_table()




class OverviewUpdater(QThread):
    """ Loading information from player profiles and updating player table """

    _signal_update_player = pyqtSignal(Player) # Singnal for updating player variables
    _signal_change_row_color = pyqtSignal(int, str) # Signal for changing row color
    _signal_set_button_enable = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Init """
        self._window = window
        self._signal_update_player.connect(self._window.update_player_variables)
        self._signal_change_row_color.connect(self._window.change_row_color)
        self._signal_set_button_enable.connect(self._window.set_button_enabled)
    

    def _update_player(self, player: Player) -> bool:
        """ Updating player variables of a single player """
        self._signal_change_row_color.emit(player.row, "dark-yellow")
        time.sleep(0.3)
        player.load_profile()
        player.load_name()
        player.load_active()
        if player.correct:
            self._signal_change_row_color.emit(player.row, None)
        else:
            self._signal_change_row_color.emit(player.row, "dark-red")
        self._signal_update_player.emit(player)
        return player.correct
    
    
    def _update_player_variables(self):
        """ Loading all player profiles and printing out player variables """
        # Disabling buttons
        self._window.refresh_button.setEnabled(False)
        self._window.add_button.setEnabled(False)
        self._signal_set_button_enable.emit(6, False)
        # Updating variables
        time.sleep(1)
        correct = 0
        current = 0
        self._window.status_change_message("Loading information from player profiles")
        self._window.status_update_progress(current, len(self._window.players))
        for player in self._window.players:
            if self._update_player(player):
                correct += 1
            current += 1
            self._window.status_update_progress(current, len(self._window.players))
        self._window.status_result_progress("Finished loading player profiles", correct, len(self._window.players))
        # Enabling buttons
        self._window.refresh_button.setEnabled(True)
        self._window.add_button.setEnabled(True)
        self._signal_set_button_enable.emit(6, True)
        

    def run(self):
        """ Loading players and adding then into table """
        self._update_player_variables()