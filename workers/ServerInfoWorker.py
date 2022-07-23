from PyQt5 import QtCore
import datetime

from misc.Config import *
from misc.Functions import *
from workers.TabInfoWorker import *


class ServerInfoWorker(TabInfoWorker):
    """Worker class is for executing background tasks
    """


    showPlayer = QtCore.pyqtSignal(int, str, int, str)
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
        self.showPlayer.connect(self.tab.showPlayer)
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
        # Loading players
        self.loadPlayers()
        # Sleeping
        self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
        if self.cancel:
            return
        # Loading recent games
        self.loadGames()
    

    def loadServerInformation(self):
        """Loads information about the server
        """
        self.message.emit("Loading server information")
        for i in range(1, 5):
            self.setInfoRowColor.emit(i, "dark-yellow")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/server/" + str(self.tab.id))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            # Showing player information
            self.setInfoContent.emit(1, data["name"])
            self.setInfoContent.emit(2, data["ip_addr"])
            self.setInfoContent.emit(3, str(data["port"]))
            self.setInfoContent.emit(4, data["create_dt"])
            self.resultMessage.emit("Successfully loaded server information", True)
            for i in range(1, 5):
                self.setInfoRowColor.emit(i, None)
        else:
            self.resultMessage.emit("Unable to load server information", False)
            for i in range(1, 5):
                self.setInfoRowColor.emit(i, "dark-red")
    

    def loadPlayers(self):
        """Loading top scoring players
        """
        self.message.emit("Loading top scoring players")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/server/" + str(self.tab.id) + "/topscorers")
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            # Adding players to table
            for player in data["top_scorers"]:
                if checkPlayerExistence(player["player_id"]):
                    color = "dark-blue"
                else:
                    color = None
                self.showPlayer.emit(player["player_id"], processNick(player["nick"]), player["score"], color)
            self.resultMessage.emit("Successfully loaded top scoring players", True)
        else:
            self.resultMessage.emit("Failed to load top scoring players", False)
    

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