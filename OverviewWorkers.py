from PyQt5.QtCore import pyqtSignal
from Window import *
from Worker import *
from Player import *
import sys, os, json, time

PLAYERS_FINENAME = "Players.json" # JSON file for storing players



class OverviewLoader(Worker):
    """Loading players from file and putting them into a table
    """


    signal_add_player = pyqtSignal(Player) # Signal for adding new player to table
    

    def connect_slots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self.signal_add_player.connect(self.window.add_player_to_table)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def load_player(self, player: Player):
        """Loads a single player into list

        Args:
            player (Player): Player instance
        """
        self.window.players.append(player)


    def __load_players(self):
        """Loads players from file
        """
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, PLAYERS_FINENAME) # Absolute path to the file with players
        # Opening file
        try:
            if os.path.isfile(absolute_filepath):
                f = open(absolute_filepath, "r")
                players_loaded = json.loads(f.read())
                for player_dict in players_loaded:
                    if len(player_dict) == 2 and "id" in player_dict and "nick" in player_dict \
                        and type(player_dict["id"]) == int and type(player_dict["nick"]) == str:
                        player = Player(player_dict)
                        self.load_player(player)
                f.close()
        except:
            players_loaded = []
        self.correct = len(self.window.players)
        self.maximum = len(players_loaded)
    

    def add_player(self, player: Player):
        """Adds a single player into table

        Args:
            player (Player): Player instance
        """
        self.signal_add_player.emit(player)

    
    def __add_players(self):
        """Adds rows filled with player data to table
        """
        if not self.window.players == []:
            for player in self.window.players:
                self.add_player(player)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading players from file")


    def run(self):
        """Running the Worker task
        """
        self.__load_players()
        self.__add_players()


    def after(self):
        """This method is called after this worker is finished
        """
        if self.correct > 0:
            self.window.status.result_progress("Finished loading players from file", self.correct, self.maximum)
        else: 
            self.window.status.result_message("No stored players were found")





class OverviewUpdater(Worker):
    """Loading information from player profiles and updating player table
    """


    signal_update_player = pyqtSignal(Player) # Singnal for updating player variables
    signal_change_row_color = pyqtSignal(int, str) # Signal for changing row color
    signal_set_button_enable = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons
    

    def connect_slots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self.signal_update_player.connect(self.window.update_player_variables)
        self.signal_change_row_color.connect(self.window.change_row_color)
        self.signal_set_button_enable.connect(self.window.set_button_enabled)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def update_player(self, player: Player) -> bool:
        """Updating player variables of a single player
        """
        self.signal_change_row_color.emit(self.window.get_row(player), "dark-yellow")
        time.sleep(0.2)
        player.load_profile()
        player.load_name()
        player.load_active()
        if player.error == None:
            self.signal_change_row_color.emit(self.window.get_row(player), None)
        else:
            self.signal_change_row_color.emit(self.window.get_row(player), "dark-red")
        self.signal_update_player.emit(player)
        return player.error == None
    
    
    def __update_players(self):
        """Loading all player profiles and printing out player variables
        """
        # Updating variables
        current = 0
        for player in self.window.players:
            # Checking if cancellation is requested
            if self.cancel:
                self.cancel = False
                break
            # Updating player data
            if self.update_player(player):
                self.correct += 1
            current += 1
            self.window.status.progress(current, self.maximum)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading information from player profiles")
        self.window.status.progress(0, self.maximum)
        # Disabling buttons
        self.window.add_button.setEnabled(False)
        self.signal_set_button_enable.emit(6, False)
        

    def run(self):
        """Running the Worker task
        """
        self.correct = 0
        self.maximum = len(self.window.players)
        if self.maximum > 0:
            self.__update_players()


    def after(self):
        """This method is called after this worker is finished
        """
        self.window.status.result_progress("Finished loading player profiles", self.correct, self.maximum)
        # Enabling buttons
        self.window.refresh_button.setEnabled(True)
        self.window.update_refreshbutton_visuals(False)
        self.window.add_button.setEnabled(True)
        self.signal_set_button_enable.emit(6, True)





class OverviewAdder(OverviewLoader, OverviewUpdater):
    """Loading information about a single player and updating player table during runtime
    """


    signal_add_player = pyqtSignal(Player) # Signal for adding new player to table
    signal_update_player = pyqtSignal(Player) # Singnal for updating player variables
    signal_change_row_color = pyqtSignal(int, str) # Signal for changing row color
    

    def connect_slots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self.signal_add_player.connect(self.window.add_player_to_table)
        self.signal_update_player.connect(self.window.update_player_variables)
        self.signal_change_row_color.connect(self.window.change_row_color)
    

    def __init__(self, window: Window, player: Player):
        """Initialising Worker thread
        """
        OverviewLoader.__init__(self, window)
        OverviewUpdater.__init__(self, window)
        self.player = player
    

    def save_players(self):
        """Attempts to save current list of players into file
        """
        # Getting abolute path to file
        current_directory = os.path.dirname(__file__) # The directory where this script is located
        absolute_filepath = os.path.join(current_directory, PLAYERS_FINENAME) # Absolute path to the file with players
        # Saving file
        try:
            f = open(absolute_filepath, "w")
            f.write(json.dumps(self.window.players, sort_keys=False, indent=4))
            f.close()
        except:
            pass
    

    def before(self):
        """This method is called before this worker is run
        """
        # Disabling buttons
        self.window.refresh_button.setEnabled(False)
        self.window.add_button.setEnabled(False)
        self.window.status.message("Loading information about new player \"" + self.player["nick"] + "\" (ID = " + str(self.player["id"]) + ")")
        
    
    def run(self):
        """Running the Worker task
        """
        self.load_player(self.player)
        self.add_player(self.player)
        self.correct = self.update_player(self.player)
        self.save_players()


    def after(self):
        """This method is called after this worker is finished
        """
        if self.correct:
            self.window.status.result_message("Successfully loaded new player \"" + self.player["nick"] + "\" (ID = " + str(self.player["id"]) + ")")
        else:
            self.window.status.result_message("An error occured while loading player \"" + self.player["nick"] + "\" (ID = " + str(self.player["id"]) + ")", False)
        # Enabling buttons
        self.window.refresh_button.setEnabled(True)
        self.window.add_button.setEnabled(True)





class OverviewRemover(OverviewAdder):
    """Removes a player from table and from files
    """


    signal_remove_player = pyqtSignal(Player) # Signal for removing a player from table
    signal_set_button_enable = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons
    

    def connect_slots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self.signal_remove_player.connect(self.window.remove_player_from_table)
        self.signal_set_button_enable.connect(self.window.set_button_enabled)
    

    def __init__(self, window: Window, player: Player):
        """Initialising Worker thread
        """
        super().__init__(window, player)
    

    def __remove_player(self):
        """Removes a selected player from list
        """
        index = self.window.players.index(self.player)
        self.window.players.pop(index)
    

    def before(self):
        """This method is called before this worker is run
        """
        # Disabling buttons
        self.window.refresh_button.setEnabled(False)
        self.window.add_button.setEnabled(False)
        self.signal_set_button_enable.emit(6, False)
        self.window.status.message("Removing player \"" + self.player["nick"] + "\" (ID " + str(self.player["id"]) + ")")
        
    
    def run(self):
        """Running the Worker task
        """
        # Deleting player
        self.signal_remove_player.emit(self.player)
        self.__remove_player()
        self.save_players()


    def after(self):
        """This method is called after this worker is finished
        """
        # Enabling buttons
        self.window.refresh_button.setEnabled(True)
        self.window.add_button.setEnabled(True)
        self.signal_set_button_enable.emit(6, True)
        self.window.status.result_message("Successfully removed player \"" + self.player["nick"] + "\" (ID " + str(self.player["id"]) + ")")