#!/usr/bin/env python3
from PyQt5.QtCore import QThread
from WindowWithStatus import *
import sys, os, json, time
from Player import *


PLAYERS_FINENAME = "Players.json" # JSON file for storing players



class OverviewLoader(QThread):
    """ Overview worker QThread for loading players """

    _signal_add_player = pyqtSignal(Player) # Signal for adding new player to table


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Init """
        self._window = window
        self._signal_add_player.connect(self._window.add_player_to_table)
        

    def _load_players(self) -> int:
        """ Loads players from file """
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, PLAYERS_FINENAME) # Absolute path to the file with players
        # Opening file
        try:
            if os.path.isfile(absolute_filepath):
                players_file = open(absolute_filepath, "r")
                players_loaded = json.loads(players_file.read())
                for player_dict in players_loaded:
                    if len(player_dict) == 2 and "id" in player_dict and "nick" in player_dict \
                        and type(player_dict["id"]) == int and type(player_dict["nick"]) == str:
                        player_instance = Player(player_dict)
                        self._window.players.append(player_instance)
                players_file.close()
        except:
            players_loaded = []
        return len(players_loaded)

    
    def _add_players_to_table(self):
        """ Adds rows filled with player data to table """
        if not self._window.players == []:
            for player in self._window.players:
                self._signal_add_player.emit(player)


    def run(self):
        """ Loading players and adding then into table """
        self._window.status_change_message("Loading players from file")
        max = self._load_players()
        self._add_players_to_table()
        if len(self._window.players) > 0:
            self._window.status_result_progress("Finished loading players from file", len(self._window.players), max)
        else: 
            self._window.status_result_message("No stored players were found")
        time.sleep(2)




class OverviewUpdater(QThread):
    """ Loading information from player profiles and updating player table """

    _signal_update_player = pyqtSignal(Player) # Singnal for updating player variables
    _signal_change_row_color = pyqtSignal(int, str) # Signal for changing row color
    _signal_set_button_enable = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons


    def __init__(self, window: WindowWithStatus):
        super().__init__()
        """ Init """
        self.cancel = False
        self._window = window
        self._signal_update_player.connect(self._window.update_player_variables)
        self._signal_change_row_color.connect(self._window.change_row_color)
        self._signal_set_button_enable.connect(self._window.set_button_enabled)
    

    def _update_player(self, player: Player) -> bool:
        """ Updating player variables of a single player """
        self._signal_change_row_color.emit(player.row, "dark-yellow")
        time.sleep(0.2)
        player.load_profile()
        player.load_name()
        player.load_active()
        if player.error == None:
            self._signal_change_row_color.emit(player.row, None)
        else:
            self._signal_change_row_color.emit(player.row, "dark-red")
        self._signal_update_player.emit(player)
        return player.error == None
    
    
    def _update_player_variables(self):
        """ Loading all player profiles and printing out player variables """
        # Disabling buttons
        #self._window.refresh_button.setEnabled(False)
        self._window.add_button.setEnabled(False)
        self._signal_set_button_enable.emit(6, False)
        # Updating variables
        correct = 0
        current = 0
        self._window.status_change_message("Loading information from player profiles")
        self._window.status_update_progress(current, len(self._window.players))
        for player in self._window.players:
            # Checking if cancellation is requested
            if self.cancel:
                break
            # Updating player data
            if self._update_player(player):
                correct += 1
            current += 1
            self._window.status_update_progress(current, len(self._window.players))
        self._window.status_result_progress("Finished loading player profiles", correct, len(self._window.players))
        # Enabling buttons
        self._window.refresh_button.setEnabled(True)
        self._window.update_refreshbutton_visuals(False)
        self._window.add_button.setEnabled(True)
        self._signal_set_button_enable.emit(6, True)
        

    def run(self):
        """ Loading players and adding then into table """
        if len(self._window.players) > 0:
            self._update_player_variables()
        self.cancel = False
        #print(json.dumps(self._window.players, sort_keys=False, indent=4))