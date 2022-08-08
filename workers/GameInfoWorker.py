from PyQt5 import QtCore
import datetime

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *
from workers.TabInfoWorker import *


class GameInfoWorker(TabInfoWorker):
    """Worker class is for executing background tasks
    """


    showPlayer = QtCore.pyqtSignal(int, str, int, str, str)
    showGroupName = QtCore.pyqtSignal(str)


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
        self.showGroupName.connect(self.tab.showGroupName)
    

    def run(self):
        """Running the Worker task
        """
        # Loading game information
        data = self.loadGameInformation()
        if data is not None:
            # Canceling
            self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
            if self.cancel:
                return
            # Loading additional information
            self.loadAdditionalInformation(data)
    

    def loadGameInformation(self):
        """Loading game information

        Returns:
            dict: Loaded game data
        """
        self.message.emit("Loading game information")
        for i in range(1, self.tab.info.rowCount()):
            self.setInfoRowColor.emit(i, "dark-yellow")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/game/" + str(self.tab.id))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            # Showing game information
            gameDatetime = datetime.datetime.strptime(data["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
            self.setInfoContent.emit(1, gameDatetime.strftime("%d.%m.%Y %H:%M:%S UTC") + " (" + data["create_dt_fuzzy"] + ")")
            self.setInfoContent.emit(2, "(#" + str(data["server_id"]) + ")")
            self.setInfoContent.emit(3, "(#" + str(data["map_id"]) + ")")
            self.setInfoContent.emit(4, data["game_type_cd"].upper() + " (" + data["game_type_descr"] + ")")
            self.setInfoContent.emit(5, data["duration"] + " (" + str(data["duration_secs"]) + " seconds)")
            # Adding players to table
            self.addPlayers(data)
            self.resultMessage.emit("Successfully loaded game information", True)
            for i in range(1, self.tab.info.rowCount()):
                self.setInfoRowColor.emit(i, None)
            return data
        else:
            self.resultMessage.emit("Unable to load game information", False)
            for i in range(1, self.tab.info.rowCount()):
                self.setInfoRowColor.emit(i, "dark-red")
            return None
    

    def addPlayers(self, data: dict):
        """Adds players to table

        Args:
            data (dict): JSON dict
        """
        # Adding players to table
        playerArrays = {
            "player_game_stats": {
                "group": "Players",
                "color": None
            },
            "spectators": {
                "group": "Spectators",
                "color": "grey"
            },
            "forfeits": {
                "group": "Forfeits",
                "color": "grey"
            }
        }
        for array, settings in playerArrays.items():
            if len(data[array]) > 0:
                self.showGroupName.emit(settings["group"].upper())
            for player in data[array]:
                if settings["color"] == None:
                    if "color" in player:
                        if player["color"] == "":
                            color = "blue"
                        else:
                            color = player["color"]
                else:
                    color = settings["color"]
                if "avg_latency" in player:
                    ping = str(player["avg_latency"])
                else:
                    ping = ""
                self.showPlayer.emit(player["player_id"], player["nick"], player["score"], color, ping)


    def loadAdditionalInformation(self, data: dict):
        """Loads additional information for info table

        Args:
            data (dict): Game data
        """
        self.message.emit("Loading additional information")
        successful = 0
        current = 0
        # Loading server name
        self.setInfoRowColor.emit(2, "dark-yellow")
        response = None
        try:
            current += 1
            response = createRequest("https://stats.xonotic.org/server/" + str(data["server_id"]))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        if response:
            successful += 1
            self.addInfoContent.emit(2, response.json()["name"])
            self.setInfoRowColor.emit(2, None)
        else:
            self.setInfoRowColor.emit(1, "dark-red")
        self.progress.emit(current, 2)
        # Loading map name
        self.setInfoRowColor.emit(3, "dark-yellow")
        response = None
        try:
            current += 1
            response = createRequest("https://stats.xonotic.org/map/" + str(data["map_id"]))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        if response:
            successful += 1
            self.addInfoContent.emit(3, response.json()["name"])
            self.setInfoRowColor.emit(3, None)
        else:
            self.setInfoRowColor.emit(2, "dark-red")
        self.progress.emit(current, 2)
        # Showing status
        self.resultProgress.emit("Finished loading additional information", successful, 2)