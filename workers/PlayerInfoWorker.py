from PyQt5 import QtCore
import datetime, math

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *
from workers.TabInfoWorker import *


class PlayerInfoWorker(TabInfoWorker):
    """Worker class is for executing background tasks
    """


    setInfoTextColor = QtCore.pyqtSignal(int, str)
    showRecentGame = QtCore.pyqtSignal(dict)
    updateHeatmap = QtCore.pyqtSignal(int, int)
    showGameStats = QtCore.pyqtSignal(list, dict)


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
        self.showRecentGame.connect(self.tab.showRecentGame)
        self.updateHeatmap.connect(self.tab.updateHeatmap)
        self.showGameStats.connect(self.tab.showGameStats)
    

    def run(self):
        """Running the Worker task
        """
        self.thisWeek = 0
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
        for i in range(1, 2):
            self.setInfoRowColor.emit(i, "dark-yellow")
        if not Config.instance().load("Players"):
            # Creating new file for players
            Config.instance()["Players"] = []
            Config.instance().save("Players")
            # Checking if it was created
            if not Config.instance().load("Players"):
                self.resultMessage.emit("Cannot access file with tracked players", False)
                for i in range(1, 3):
                    self.setInfoRowColor.emit(i, "dark-red")
            else:
                self.resultMessage.emit("Created a new config file for players", True)
        if Config.instance().load("Players"):
            player = checkPlayerExistence(self.tab.id)
            if player is not None:
                self.resultMessage.emit("This player is already being tracked", True)
                self.setInfoContent.emit(1, player["nick"])
                self.setInfoContent.emit(2, player["description"])
            else:
                self.resultMessage.emit("This player is not being tracked yet", True)
            for i in range(1, 2):
                self.setInfoRowColor.emit(i, None)
    

    def loadPlayerInformation(self) -> bool:
        """Loading simple player information

        Returns:
            bool: Did it load successfully?
        """
        self.message.emit("Loading player information")
        for i in range(3, 7):
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
            self.setInfoContent.emit(3, processNick( data["player"]["nick"] ))
            since = data["player"]["joined_fuzzy"]
            self.setInfoContent.emit(4, since)
            self.setInfoTextColor.emit(4, getAgeColor(since))
            active = data["overall_stats"]["overall"]["last_played_fuzzy"]
            self.setInfoContent.emit(5, active)
            self.setInfoTextColor.emit(5, getActiveColor(active))
            self.setInfoContent.emit(6, str(round(data["overall_stats"]["overall"]["total_playing_time"] / 3600)) + " hours; " + str(data["games_played"]["overall"]["games"]) + " games")
            self.resultMessage.emit("Successfully loaded player information", True)
            for i in range(3, 7):
                self.setInfoRowColor.emit(i, None)
            # Processing game stats information
            dataList = sorted(data["games_played"].values(), key=lambda x: x["games"], reverse=True)
            self.showGameStats.emit(dataList, data["overall_stats"])
        else:
            self.resultMessage.emit("Unable to load player information", False)
            for i in range(3, 7):
                self.setInfoRowColor.emit(i, "dark-red")
        return bool(response)
    

    def loadGames(self):
        current = 0
        correct = 0
        self.message.emit("Loading recent games")
        self.setInfoContent.emit(7, "0")
        self.setInfoRowColor.emit(7, "dark-yellow")
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
            except:
                pass
        # Showing results
        if current == correct:
            self.setInfoRowColor.emit(7, None)
        else:
            self.setInfoRowColor.emit(7, "dark-red")
        self.resultProgress.emit("Finished loading recent games", correct, Config.instance()["Settings"]["gameListCount"])
    

    def processGames(self, data: dict):
        """Processes data about a certain game

        Args:
            data (dict): Loaded game information
        """
        for game in data:
            # Checking if this game happened within the last 7 days
            gameDatetime = datetime.datetime.strptime(game["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
            gameTime = gameDatetime.timestamp()
            currentTime = int(time.time())
            week = 60 * 60 * 24 * 7
            if (currentTime - gameTime) <= week:
                # Getting information from datetime
                row = gameDatetime.date().weekday()
                column = gameDatetime.hour // Config.instance()["Settings"]["heatmapHourSpan"]
                # Updating heatmap
                self.updateHeatmap.emit(row, column)
                # Updating info label
                self.thisWeek += 1
                if self.thisWeek == Config.instance()["Settings"]["gameListCount"] * 20:
                    self.setInfoContent.emit(7, ">" + str(self.thisWeek) + " (>" + str(math.floor(self.thisWeek / 7)) + " games per day)")
                else:
                    self.setInfoContent.emit(7, str(self.thisWeek) + " (~" + str(math.floor(self.thisWeek / 7)) + " games per day)")
            # Showing game in a gameList table
            self.showRecentGame.emit(game)