from PyQt5 import QtCore
import datetime

from misc.Config import *
from misc.Functions import *
from workers.TabInfoWorker import *


class ServerInfoWorker(TabInfoWorker):
    """Worker class is for executing background tasks
    """


    showRecentGame = QtCore.pyqtSignal(dict)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        super().connectSlots()
        self.showRecentGame.connect(self.tab.showRecentGame)
    

    def run(self):
        """Running the Worker task
        """
        # Loading recent games
        self.loadGames()
    

    def loadGames(self):
        current = 0
        correct = 0
        self.message.emit("Loading recent games")
        self.setInfoRowColor.emit(6, "dark-yellow")
        # Loading list of games
        url = "https://stats.xonotic.org/games?server_id=" + str(self.tab.id)
        for i in range( Config.instance()["Settings"]["gameListCount"] ):
            # Sleeping
            time.sleep( Config.instance()["Settings"]["singleRequestInterval"] )
            # Canceling
            if self.cancel:
                break
            # Getting list of games
            current += 1
            self.progress.emit(current, Config.instance()["Settings"]["gameListCount"])
            try:
                response = createRequest(url)
                self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
                if response:
                    correct += 1
                    data = response.json()
                    if data is not None and len(data) > 0:
                        self.processGames(data)
                        # Getting new URL
                        url = "https://stats.xonotic.org/games?server_id=" + str(self.tab.id) + "&start_game_id=" + str(data[-1]["game_id"] -1)
                    else:
                        break
            except BufferError:
                pass
        # Showing results
        if current == correct:
            self.setInfoRowColor.emit(6, None)
        else:
            self.setInfoRowColor.emit(6, "dark-red")
        self.resultProgress.emit("Finished loading recent games", correct, Config.instance()["Settings"]["gameListCount"])
    

    def processGames(self, data: dict):
        """Processes data about a certain game

        Args:
            data (dict): Loaded game information
        """
        for game in data:
            # Showing game in a gameList table
            self.showRecentGame.emit(game)