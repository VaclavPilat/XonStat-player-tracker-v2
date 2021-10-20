from Window import *
from Worker import *
from Player import *
import sys, os, json, time
from Functions import *
from Settings import *



class OverviewLoader(Worker):
    """Loading players from file and putting them into a table
    """


    _showPlayer = pyqtSignal(Player) # Signal for adding new player to table
    _setButtonsEnabled = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons
    _updateRefreshButton = pyqtSignal() # Signal for updating visuals of a "Refresh" button
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._showPlayer.connect(self.window.showPlayer)
        self._setButtonsEnabled.connect(self.window.table.setButtonsEnabled)
        self._updateRefreshButton.connect(self.window.updateRefreshButton)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def loadPlayer(self, player: Player):
        """Loads a single player into list

        Args:
            player (Player): Player instance
        """
        self.window.players.append(player)


    def __loadPlayers(self):
        """Loads players from file
        """
        # Getting abolute path to file
        absolutePath = os.path.join(os.path.dirname(__file__), "Players.json") # Absolute path to the file with players
        # Opening file
        try:
            if os.path.isfile(absolutePath):
                f = open(absolutePath, "r")
                loadedPlayers = json.loads(f.read())
                for loadedPlayer in loadedPlayers:
                    if len(loadedPlayer) == 2 and "id" in loadedPlayer and "nick" in loadedPlayer \
                        and type(loadedPlayer["id"]) == int and type(loadedPlayer["nick"]) == str:
                        player = Player(loadedPlayer)
                        self.loadPlayer(player)
                f.close()
        except:
            loadedPlayers = []
        self.correct = len(self.window.players)
        self.maximum = len(loadedPlayers)
    

    def showPlayer(self, player: Player):
        """Adds a single player into table

        Args:
            player (Player): Player instance
        """
        self._showPlayer.emit(player)

    
    def __showPlayers(self):
        """Adds rows filled with player data to table
        """
        if not self.window.players == []:
            for player in self.window.players:
                self.showPlayer(player)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading players from file")


    def run(self):
        """Running the Worker task
        """
        self.__loadPlayers()
        self.__showPlayers()


    def after(self):
        """This method is called after this worker is finished
        """
        self.window.refreshButton.setEnabled(True)
        self._updateRefreshButton.emit()
        self.window.addButton.setEnabled(True)
        self._setButtonsEnabled.emit(6, True)
        if self.correct > 0:
            self.window.status.resultProgress("Finished loading players from file", self.correct, self.maximum)
        else: 
            self.window.status.resultMessage("No stored players were found")





class OverviewUpdater(Worker):
    """Loading information from player profiles and updating player table
    """


    _updatePlayer = pyqtSignal(Player) # Singnal for updating player variables
    _setRowColor = pyqtSignal(int, str) # Signal for changing row color
    _setButtonsEnabled = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons
    _updateRefreshButton = pyqtSignal() # Signal for updating visuals of a "Refresh" button
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._updatePlayer.connect(self.window.updatePlayer)
        self._setRowColor.connect(self.window.table.setRowColor)
        self._setButtonsEnabled.connect(self.window.table.setButtonsEnabled)
        self._updateRefreshButton.connect(self.window.updateRefreshButton)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
        self.maximum = 0
    

    def updatePlayer(self, player: Player) -> bool:
        """Updating player variables of a single player
        """
        self._setRowColor.emit(self.window.getRow(player), "dark-yellow")
        # Sleep before loading
        time.sleep(Settings.instance()["singleRequestInterval"])
        # Loading information
        player.loadProfile()
        player.loadName()
        player.loadActive()
        if player.error == None:
            self._setRowColor.emit(self.window.getRow(player), None)
        else:
            self._setRowColor.emit(self.window.getRow(player), "dark-red")
        self._updatePlayer.emit(player)
        return player.error == None
    
    
    def __updatePlayers(self):
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
            if self.updatePlayer(player):
                self.correct += 1
            current += 1
            self.window.status.progress(current, self.maximum)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading information from player profiles")
        self.window.status.progress(0, self.maximum)
        # Disabling buttons
        self.window.addButton.setEnabled(False)
        self._setButtonsEnabled.emit(6, False)
        

    def run(self):
        """Running the Worker task
        """
        self._updateRefreshButton.emit()
        self.correct = 0
        self.maximum = len(self.window.players)
        if self.maximum > 0:
            self.__updatePlayers()


    def after(self):
        """This method is called after this worker is finished
        """
        self.window.status.resultProgress("Finished loading player profiles", self.correct, self.maximum)
        # Enabling buttons
        self.window.refreshButton.setEnabled(True)
        self._updateRefreshButton.emit()
        self.window.addButton.setEnabled(True)
        self._setButtonsEnabled.emit(6, True)





class OverviewAdder(OverviewLoader, OverviewUpdater):
    """Loading information about a single player and updating player table during runtime
    """


    _showPlayer = pyqtSignal(Player) # Signal for adding new player to table
    _updatePlayer = pyqtSignal(Player) # Singnal for updating player variables
    _setRowColor = pyqtSignal(int, str) # Signal for changing row color
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._showPlayer.connect(self.window.showPlayer)
        self._updatePlayer.connect(self.window.updatePlayer)
        self._setRowColor.connect(self.window.table.setRowColor)
    

    def __init__(self, window: Window, player: Player):
        """Initialising Worker thread
        """
        OverviewLoader.__init__(self, window)
        OverviewUpdater.__init__(self, window)
        self.player = player
    

    def savePlayers(self):
        """Attempts to save current list of players into file
        """
        # Getting abolute path to file
        absolutePath = os.path.join(os.path.dirname(__file__), "Players.json") # Absolute path to the file with players
        # Saving file
        try:
            f = open(absolutePath, "w")
            f.write(json.dumps(self.window.players, sort_keys=False, indent=4))
            f.close()
        except:
            printException()
    

    def before(self):
        """This method is called before this worker is run
        """
        # Disabling buttons
        self.window.refreshButton.setEnabled(False)
        self.window.addButton.setEnabled(False)
        self.window.status.message("Loading information about new player \"" + self.player["nick"] + "\" (ID#" + str(self.player["id"]) + ")")
        
    
    def run(self):
        """Running the Worker task
        """
        self.loadPlayer(self.player)
        self.showPlayer(self.player)
        self.correct = self.updatePlayer(self.player)
        self.savePlayers()


    def after(self):
        """This method is called after this worker is finished
        """
        if self.correct:
            self.window.status.resultMessage("Successfully loaded new player \"" + self.player["nick"] + "\" (ID#" + str(self.player["id"]) + ")")
        else:
            self.window.status.resultMessage("An error occured while loading player \"" + self.player["nick"] + "\" (ID#" + str(self.player["id"]) + ")", False)
        # Enabling buttons
        self.window.refreshButton.setEnabled(True)
        self.window.addButton.setEnabled(True)





class OverviewRemover(OverviewAdder):
    """Removes a player from table and from files
    """


    _hidePlayer = pyqtSignal(Player) # Signal for removing a player from table
    _setButtonsEnabled = pyqtSignal(int, bool) # Signal for changing "enabled" property of buttons
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._hidePlayer.connect(self.window.hidePlayer)
        self._setButtonsEnabled.connect(self.window.table.setButtonsEnabled)
    

    def __init__(self, window: Window, player: Player):
        """Initialising Worker thread
        """
        super().__init__(window, player)
    

    def __removePlayer(self):
        """Removes a selected player from list
        """
        index = self.window.players.index(self.player)
        self.window.players.pop(index)
    

    def before(self):
        """This method is called before this worker is run
        """
        # Disabling buttons
        self.window.refreshButton.setEnabled(False)
        self.window.addButton.setEnabled(False)
        self._setButtonsEnabled.emit(6, False)
        self.window.status.message("Removing player \"" + self.player["nick"] + "\" (ID#" + str(self.player["id"]) + ")")
        
    
    def run(self):
        """Running the Worker task
        """
        # Deleting player
        self._hidePlayer.emit(self.player)
        self.__removePlayer()
        self.savePlayers()


    def after(self):
        """This method is called after this worker is finished
        """
        # Enabling buttons
        self.window.refreshButton.setEnabled(True)
        self.window.addButton.setEnabled(True)
        self._setButtonsEnabled.emit(6, True)
        self.window.status.resultMessage("Successfully removed player \"" + self.player["nick"] + "\" (ID#" + str(self.player["id"]) + ")")