from PyQt5 import QtCore
import requests

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *


class GameInfoWorker(Worker):
    """Worker class is for executing background tasks
    """


    clearTable = QtCore.pyqtSignal()
    showPlayer = QtCore.pyqtSignal(int, str, int, str)
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
        self.clearTable.connect(lambda: self.tab.players.setRowCount(0))
        self.showPlayer.connect(self.tab.showPlayer)
        self.showGroupName.connect(self.tab.showGroupName)
    

    def run(self):
        """Running the Worker task
        """
        # Clearing player table
        self.clearTable.emit()
        # Loading game information
        self.message.emit("Loading player information")
        try:
            response = requests.get(
                "https://stats.xonotic.org/game/" + str(self.tab.id),
                headers={'Accept': 'application/json'},
                timeout=2
            )
        except:
            self.resultMessage.emit("Unable to reach XonStat API", False)
            return
        # Checking response
        if response is not None and response:
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
            # Adding players to table
            data = response.json()
            self.addPlayers(data)
            self.resultMessage.emit("Successfully loaded game information", True)
        else:
            self.resultMessage.emit("Unable to load game information", False)
    

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
