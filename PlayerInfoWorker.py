from Worker import *
from ColoredWidgets import *
import time, datetime
from Functions import *
from Config import *



class PlayerInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _setRowColor = pyqtSignal(int, str) # Signal for changing row color
    _setWidgetColor = pyqtSignal(int, int, str) # Signal for changing widget color
    _showName = pyqtSignal(str) # Showing current player name
    _showSince = pyqtSignal(str) # Showing since when this player is playing
    _showActive = pyqtSignal(str) # Showing the last time this player joined a game
    _setActiveColor = pyqtSignal(str) # Setting a color to "active" label
    _showTime = pyqtSignal(str) # Showing total time spent playing
    _showUsedNames = pyqtSignal(str) # Showing recently used names
    _showGames = pyqtSignal() # Showing number of recently played games
    _updateHeatmapGames = pyqtSignal(int, int) # Updating number of games in heatmap
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._setRowColor.connect(self.window.table.setRowColor)
        self._setWidgetColor.connect(self.window.heatmap.setWidgetColor)
        self._showName.connect(self.window.name.setText)
        self._showSince.connect(self.window.since.setText)
        self._showActive.connect(self.window.active.setText)
        self._setActiveColor.connect(self.window.active.setColor)
        self._showTime.connect(self.window.time.setText)
        self._showUsedNames.connect(self.window.showUsedNames)
        self._showGames.connect(self.window.showGames)
        self._updateHeatmapGames.connect(self.window.updateHeatmapGames)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.message.emit("Loading information from player profile")
    

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
    
    """
    def __processGameData(self, data: BeautifulSoup):
        ""Processes game data retrieved from game pages

        Args:
            data (BeautifulSoup): Beutiful soup object for game page
        ""
        # Getting used player name
        try:
            element = data.find("a", href="/player/" + str(self.window.player["id"]))
            self._showUsedNames.emit(self.window.player.loadName())
        except:
            printException()
        # Checking if this game happened within the last 7 days
        try:
            currentTime = int(time.time())
            element = data.select("span.abstime")[0]
            gameTime = int(element["data-epoch"])
            week = 60 * 60 * 24 * 7
            if (currentTime - gameTime) <= week:
                self._showGames.emit()
                # Getting information from datetime
                gameDatetime = datetime.datetime.utcfromtimestamp(gameTime)
                row = gameDatetime.date().weekday()
                column = gameDatetime.hour // Config.i()["heatmapHourSpan"]
                # Updating heatmap
                currentColor = self.window.heatmap.cellWidget(row, column).property("background")
                if currentColor is not None:
                    currentColorIndex = int(currentColor.split('-')[1])
                    if int(currentColor.split('-')[1]) > 1:
                        self._setWidgetColor.emit(row, column, "active-" + str(currentColorIndex -1))
                else:
                    self._setWidgetColor.emit(row, column, "active-7")
                self._updateHeatmapGames.emit(row, column)
        except:
            printException()
    """

    def __loadRecentGames(self):
        """Loads recent games and extracts information from them
        """
        self.message.emit("Loading list of recent games")
        for i in range(4, self.window.table.rowCount()):
            self._setRowColor.emit(i, "dark-yellow")
        # Loading recent games
        correct = 0
        maximum = 0
        for gameValues in self.window.player.loadRecentGames():
            maximum = gameValues[1]
            correct += 1
            self.__processGameData(gameValues[2])
            if not gameValues[1] == 0 and gameValues[0] == gameValues[1]:
                self.resultProgress.emit("Loading recent games", correct, maximum)
            else:
                self.message.emit("Loading recent games")
                self.progress.emit(gameValues[0], gameValues[1])
        # Printing out message
        if maximum > 0:
            self.resultProgress.emit("Finished loading games", correct, maximum)
        else:
            self.resultMessage.emit("No games were found", self.window.player.time == "0 hours")
        if correct > 0 or (maximum == 0 and self.window.player.time == "0 hours"):
            for i in range(4, self.window.table.rowCount()):
                self._setRowColor.emit(i, None)
        else:
            for i in range(4, self.window.table.rowCount()):
                self._setRowColor.emit(i, "dark-red")
        

    def run(self):
        """Running the Worker task
        """
        # Loading values
        self.__loadSimpleValues()
        if self.cancel:
            return
        # Changing status
        if self.window.player.error is not None:
            self.resultMessage.emit("An error occured: " + self.window.player.error, False)
        else:
            self.resultMessage.emit("Successfully loaded player profile", True)
            time.sleep( Config.instance()["Settings"]["singleRequestInterval"] )
            if self.cancel:
                return
            self.__loadRecentGames()