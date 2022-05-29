from PyQt5 import QtWidgets, QtCore, QtGui
from xml.sax.saxutils import escape
import datetime

from Worker import *
from ColoredWidgets import *
from Functions import *
from Config import *



class PlayerInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _setRowColor = QtCore.pyqtSignal(int, str) # Signal for changing row color
    _setWidgetColor = QtCore.pyqtSignal(int, int, str) # Signal for changing widget color
    _showName = QtCore.pyqtSignal(str) # Showing current player name
    _showSince = QtCore.pyqtSignal(str) # Showing since when this player is playing
    _showActive = QtCore.pyqtSignal(str) # Showing the last time this player joined a game
    _setActiveColor = QtCore.pyqtSignal(str) # Setting a color to "active" label
    _showTime = QtCore.pyqtSignal(str) # Showing total time spent playing
    _showGames = QtCore.pyqtSignal() # Showing number of recently played games
    _updateHeatmapGames = QtCore.pyqtSignal(int, int) # Updating number of games in heatmap
    _updateRefreshButton = QtCore.pyqtSignal() # Signal for updating visuals of a "Refresh" button
    _showRecentGames = QtCore = QtCore.pyqtSignal(list) # Signal for adding new row into table with recent games
    

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
        self._showGames.connect(self.window.showGames)
        self._updateHeatmapGames.connect(self.window.updateHeatmapGames)
        self._updateRefreshButton.connect(self.window.updateRefreshButton)
        self._showRecentGames.connect(self.window.showRecentGames)


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
        for data in self.window.player.loadGameLists():
            if self.cancel:
                break
            if data[1] is None:
                maximum = current = data[0] -1
                self.progress.emit(data[0] -1, maximum)
            else:
                if data[1] is not False:
                    for game in data[1]:
                        self.__processGameTime(game["create_dt"])
                    correct += 1
                    self._showRecentGames.emit(data[1])
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
        self.sleep( Config.instance()["Settings"]["groupRequestInterval"] )
    

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
            self.sleep( Config.instance()["Settings"]["singleRequestInterval"] )
            if self.cancel:
                return
            self.__loadGameData()


    def after(self):
        """This method is called after this worker is finished
        """
        self._updateRefreshButton.emit()