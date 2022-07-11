from PyQt5 import QtCore
import datetime

from misc.Config import *
from misc.Functions import *
from workers.TabInfoWorker import *


class MapInfoWorker(TabInfoWorker):
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
        # Loading player information
        self.loadServerInformation()
        # Sleeping
        self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
        if self.cancel:
            return
        # Loading recent games
        self.loadGames()
    

    def loadServerInformation(self):
        """Loads information about the server
        """
        self.message.emit("Loading map information")
        for i in range(1, 2):
            self.setInfoRowColor.emit(i, "dark-yellow")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/map/" + str(self.tab.id))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            # Showing player information
            self.setInfoContent.emit(1, data["name"])
            gameDatetime = datetime.datetime.strptime(data["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
            self.setInfoContent.emit(2, gameDatetime.strftime("%d.%m.%Y %H:%M:%S UTC"))
            self.resultMessage.emit("Successfully loaded map information", True)
            for i in range(1, 2):
                self.setInfoRowColor.emit(i, None)
        else:
            self.resultMessage.emit("Unable to load map information", False)
            for i in range(1, 2):
                self.setInfoRowColor.emit(i, "dark-red")
    

    def loadGames(self):
        current = 0
        correct = 0
        self.message.emit("Loading recent games")
        self.setInfoRowColor.emit(6, "dark-yellow")
        # Loading list of games
        url = "https://stats.xonotic.org/games?map_id=" + str(self.tab.id)
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
                        url = "https://stats.xonotic.org/games?map_id=" + str(self.tab.id) + "&start_game_id=" + str(data[-1]["game_id"] -1)
                    else:
                        break
            except:
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