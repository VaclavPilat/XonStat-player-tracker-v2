from Worker import *
from ColoredWidgets import *
from bs4 import BeautifulSoup
import time



class PlayerInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _setRowColor = pyqtSignal(int, str) # Signal for changing row color
    _showName = pyqtSignal(str) # Showing current player name
    _showSince = pyqtSignal(str) # Showing since when this player is playing
    _showActive = pyqtSignal(str) # Showing the last time this player joined a game
    _setActiveColor = pyqtSignal(str) # Setting a color to "active" label
    _showTime = pyqtSignal(str) # Showing total time spent playing
    _showUsedNames = pyqtSignal(str) # Showing recently used names
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._setRowColor.connect(self.window.table.setRowColor)
        self._showName.connect(self.window.name.setText)
        self._showSince.connect(self.window.since.setText)
        self._showActive.connect(self.window.active.setText)
        self._setActiveColor.connect(self.window.active.setColor)
        self._showTime.connect(self.window.time.setText)
        self._showUsedNames.connect(self.window.showUsedNames)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading information from player profile")
    

    def __fillLabels(self):
        """Yields loaded simple player values

        Yields:
            Iterator[list]: 0 => table row index, 1 => lambda of an emitted signal
        """
        yield [0, lambda: self._showName.emit(self.window.player.loadName())]
        yield [1, lambda: self._showSince.emit(self.window.player.loadSince())]
        yield [2, lambda: self._showActive.emit(self.window.player.loadActive())]
        yield [3, lambda: self._showTime.emit(self.window.player.loadTime())]
    

    def __loadSimpleValues(self):
        """Loads simple values
        """
        for i in range(4):
            self._setRowColor.emit(i, "dark-yellow")
        self.window.player.loadProfile()
        # Filling in simple player variables
        for label in self.__fillLabels():
            label[1]()
            # Setting active color
            if label[0] == 2:
                self._setActiveColor.emit(self.window.player.getActiveColor())
            if self.window.player.error:
                self._setRowColor.emit(label[0], "dark-red")
            else:
                self._setRowColor.emit(label[0], None)
    

    def __processGameData(self, data: BeautifulSoup):
        """Processes game data retrieved from game pages

        Args:
            data (BeautifulSoup): Beutiful soup object for game page
        """
        try:
            element = data.find("a", href="/player/" + str(self.window.player["id"]))
            self._showUsedNames.emit(self.window.player.loadName(element))
        except:
            pass
    

    def __loadRecentGames(self):
        """Loads recent games and extracts information from them
        """
        for i in range(4, 7):
            self._setRowColor.emit(i, "dark-yellow")
        self.window.status.message("Loading recent games")
        correct = 0
        maximum = 0
        for gameValues in self.window.player.loadRecentGames():
            maximum = gameValues[1]
            correct += 1
            self.__processGameData(gameValues[2])
            if gameValues[0] == maximum:
                self.window.status.resultProgress("Finished loading games", correct, maximum)
            else:
                self.window.status.progress(gameValues[0], gameValues[1])
        

    def run(self):
        """Running the Worker task
        """
        self.__loadSimpleValues()
        # Changing status
        if self.window.player.error is not None:
            self.window.status.resultMessage("An error occured: " + self.window.player.error, False)
        else:
            self.window.status.resultMessage("Successfully loaded player profile")
            time.sleep(1)
            self.__loadRecentGames()