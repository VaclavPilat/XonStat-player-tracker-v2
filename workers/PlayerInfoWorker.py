from PyQt5 import QtCore
import datetime

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *
from workers.TabInfoWorker import *


class PlayerInfoWorker(TabInfoWorker):
    """Worker class is for executing background tasks
    """


    setInfoTextColor = QtCore.pyqtSignal(int, str)


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
        self.setInfoTextColor.connect(self.tab.setInfoTextColor)
    

    def run(self):
        """Running the Worker task
        """
        # Removing old content from tables
        self.clearInfoTable.emit()
        # Checking if this player is being tracked
        self.checkConfigFile()
        # Sleeping
        self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
        if self.cancel:
            return
        # Loading player information
        self.loadPlayerInformation()
        # Sleeping
        self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
        if self.cancel:
            return
        # Loading recent games
        self.loadGames()
    

    def checkConfigFile(self):
        """Checking if this player is already being tracked
        """
        self.message.emit("Checking if player is tracked")
        for i in range(2):
            self.setInfoRowColor.emit(i, "dark-yellow")
        if Config.instance().load("Players"):
            player = checkPlayerExistence(self.tab.id)
            if player is not None:
                self.resultMessage.emit("This player is already being tracked", True)
                self.setInfoContent.emit(0, player["nick"])
                self.setInfoContent.emit(1, player["description"])
            else:
                self.resultMessage.emit("This player is not being tracked yet", True)
            for i in range(2):
                self.setInfoRowColor.emit(i, None)
        else:
            self.resultMessage.emit("Cannot access file with tracked players")
            for i in range(2):
                self.setInfoRowColor.emit(i, "dark-red")
    

    def loadPlayerInformation(self) -> bool:
        """Loading simple player information

        Returns:
            bool: Did it load successfully?
        """
        self.message.emit("Loading player information")
        for i in range(2, 6):
            self.setInfoRowColor.emit(i, "dark-yellow")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/player/" + str(self.tab.id))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            # Showing player information
            self.setInfoContent.emit(2, processNick( data["player"]["nick"] ))
            since = data["player"]["joined_fuzzy"]
            self.setInfoContent.emit(3, since)
            self.setInfoTextColor.emit(3, getAgeColor(since))
            active = data["overall_stats"]["overall"]["last_played_fuzzy"]
            self.setInfoContent.emit(4, active)
            self.setInfoTextColor.emit(4, getActiveColor(active))
            self.setInfoContent.emit(5, str(round(data["overall_stats"]["overall"]["total_playing_time"] / 3600)) + " hours; " + str(data["games_played"]["overall"]["games"]) + " games")
            self.resultMessage.emit("Successfully loaded player information", True)
            for i in range(2, 6):
                self.setInfoRowColor.emit(i, None)
        else:
            self.resultMessage.emit("Unable to load player information", False)
            for i in range(2, 6):
                self.setInfoRowColor.emit(i, "dark-red")
        return bool(response)
    

    def loadGames(self):
        current = 0
        correct = 0
        self.message.emit("Loading recent games")
        # Loading list of games
        url = "https://stats.xonotic.org/games?player_id=" + str(self.tab.id)
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
                        url = "https://stats.xonotic.org/games?player_id=" + str(self.tab.id) + "&start_game_id=" + str(data[-1]["game_id"] -1)
                    else:
                        break
            except BufferError:
                pass
        self.resultProgress.emit("Finished loading recent games", correct, Config.instance()["Settings"]["gameListCount"])
    

    def processGames(self, data: dict):
        """Processes data about a certain game

        Args:
            data (dict): Loaded game information
        """
        for game in data:
            print(game["game_id"])