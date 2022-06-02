from PyQt5 import QtCore
import datetime

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *


class GameInfoWorker(Worker):
    """Worker class is for executing background tasks
    """


    clearTable = QtCore.pyqtSignal()
    showPlayer = QtCore.pyqtSignal(int, str, int, str)
    showGroupName = QtCore.pyqtSignal(str)
    setRowColor = QtCore.pyqtSignal(int, str)
    setInfoContent = QtCore.pyqtSignal(int, str)
    addInfoContent = QtCore.pyqtSignal(int, str)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.clearTable.connect(lambda: self.tab.players.setRowCount(0))
        self.showPlayer.connect(self.tab.showPlayer)
        self.showGroupName.connect(self.tab.showGroupName)
        self.setRowColor.connect(self.tab.info.setRowColor)
        self.setInfoContent.connect(self.tab.setInfoContent)
        self.addInfoContent.connect(self.tab.addInfoContent)
    

    def run(self):
        """Running the Worker task
        """
        # Clearing player table
        for i in range(self.tab.info.rowCount()):
            self.setInfoContent.emit(i, "")
        self.clearTable.emit()
        # Loading game information
        self.message.emit("Loading game information")
        for i in range(self.tab.info.rowCount()):
            self.setRowColor.emit(i, "dark-yellow")
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/game/" + str(self.tab.id))
        except:
            pass
        # Checking response
        if response is not None and response:
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
            data = response.json()
            # Showing game information
            gameDatetime = datetime.datetime.strptime(data["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
            self.setInfoContent.emit(0, gameDatetime.strftime("%d.%m.%Y %H:%M:%S UTC") + " (" + data["create_dt_fuzzy"] + ")")
            self.setInfoContent.emit(1, "(#" + str(data["server_id"]) + ")")
            self.setInfoContent.emit(2, "(#" + str(data["map_id"]) + ")")
            self.setInfoContent.emit(3, data["game_type_cd"].upper() + " (" + data["game_type_descr"] + ")")
            self.setInfoContent.emit(4, data["duration"] + " (" + str(data["duration_secs"]) + " seconds)")
            # Adding players to table
            self.addPlayers(data)
            self.resultMessage.emit("Successfully loaded game information", True)
            for i in range(self.tab.info.rowCount()):
                self.setRowColor.emit(i, None)
            self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
            if self.cancel:
                return
            # Loading additional information
            self.loadAdditionalInformation(data)
        else:
            self.resultMessage.emit("Unable to load game information", False)
            for i in range(self.tab.info.rowCount()):
                self.setRowColor.emit(i, "dark-red")
    

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
                self.showPlayer.emit(player["player_id"], player["nick"], player["score"], color)


    def loadAdditionalInformation(self, data: dict):
        """Loads additional information for info table

        Args:
            data (dict): Game data
        """
        self.message.emit("Loading additional information")
        successful = 0
        current = 0
        # Loading server name
        self.setRowColor.emit(1, "dark-yellow")
        response = None
        try:
            current += 1
            response = createRequest("https://stats.xonotic.org/server/" + str(data["server_id"]))
        except:
            pass
        if response:
            successful += 1
            self.addInfoContent.emit(1, response.json()["name"])
            self.setRowColor.emit(1, None)
        else:
            self.setRowColor.emit(1, "dark-red")
        self.progress.emit(current, 2)
        # Loading map name
        self.setRowColor.emit(2, "dark-yellow")
        response = None
        try:
            current += 1
            response = createRequest("https://stats.xonotic.org/map/" + str(data["map_id"]))
        except:
            pass
        if response:
            successful += 1
            self.addInfoContent.emit(2, response.json()["name"])
            self.setRowColor.emit(2, None)
        else:
            self.setRowColor.emit(2, "dark-red")
        self.progress.emit(current, 2)
        # Showing status
        self.resultProgress.emit("Finished loading additional information", successful, 2)