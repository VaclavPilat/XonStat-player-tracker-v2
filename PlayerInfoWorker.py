from Worker import *
from ColoredWidgets import *
import time, datetime
from Functions import *
from Config import *
from xml.sax.saxutils import escape



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
    _updateRefreshButton = pyqtSignal() # Signal for updating visuals of a "Refresh" button
    

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
        self._updateRefreshButton.connect(self.window.updateRefreshButton)


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
        for i in range(0, 4):
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
    
    
    def __processGameTime(self, gametime: str):
        """Updates heatmap and number of recent games based on game datetime

        Args:
            gametime (str): Game UTC datetime
        """
        try:
            # Checking if this game happened within the last 7 days
            gameDatetime = datetime.datetime.strptime(gametime, "%Y-%m-%dT%H:%M:%SZ")
            gameTime = gameDatetime.timestamp()
            currentTime = int(time.time())
            week = 60 * 60 * 24 * 7
            if (currentTime - gameTime) <= week:
                self._showGames.emit()
                # Getting information from datetime
                row = gameDatetime.date().weekday()
                column = gameDatetime.hour // Config.instance()["Settings"]["heatmapHourSpan"]
                # Updating heatmap
                currentColor = self.window.heatmap.cellWidget(row, column).property("background")
                self._updateHeatmapGames.emit(row, column)
        except:
            printException()
    
    
    def __findPlayerName(self, data: dict):
        """Processes game data retrieved from game pages

        Args:
            data (dict): Json object with game data
        """
        try:
            # Getting used player name
            if data is not None:
                for player in data["player_game_stats"]:
                    if player["player_id"] == self.window.player["id"]:
                        self._showUsedNames.emit(escape(player["nick"]))
                        break
        except:
            printException()


    def __loadGameData(self):
        """Loads recent games and extracts information from them
        """
        # Updating visuals
        self.message.emit("Loading lists of recent games")
        for i in range(4, 6):
            self._setRowColor.emit(i, "dark-yellow")
        # Loading recent games
        correct = 0
        maximum = Config.instance()["Settings"]["gameListCount"]
        self.progress.emit(0, maximum)
        games = []
        for data in self.window.player.loadGameLists():
            if self.cancel:
                return
            if data[1] is None:
                maximum = current = data[0] -1
                self.progress.emit(data[0] -1, maximum)
            else:
                if data[1] is not False:
                    for game in data[1]:
                        self.__processGameTime(game["create_dt"])
                    games += data[1]
                    correct += 1
                self.progress.emit(data[0], maximum)
        # Updating visuals
        if correct > 0 and maximum > 0:
            for i in range(4, 6):
                self._setRowColor.emit(i, None)
        else:
            for i in range(4, self.window.table.rowCount()):
                self._setRowColor.emit(i, "dark-red")
        self.resultProgress.emit("Finished loading gamelists", correct, maximum)
        # Canceling
        time.sleep( Config.instance()["Settings"]["groupRequestInterval"] )
        if self.cancel:
            return
        # Loading game data
        if len(games) > 0:
            current = 0
            correct = 0
            self.message.emit("Loading game data")
            self.progress.emit(current, len(games))
            self._setRowColor.emit(6, "dark-yellow")
            current = 0
            correct = 0
            for gameData in self.window.player.loadGameData(games):
                current += 1
                if gameData is not None:
                    correct += 1
                self.__findPlayerName(gameData)
                self.progress.emit(current, len(games))
            self.resultProgress.emit("Loaded game data", correct, len(games))
            if correct > 0:
                self._setRowColor.emit(6, None)
            else:
                self._setRowColor.emit(6, "dark-red")
    

    def before(self):
        """This method is called before this worker is run
        """
        self._updateRefreshButton.emit()
        

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
            self.__loadGameData()


    def after(self):
        """This method is called after this worker is finished
        """
        self._updateRefreshButton.emit()