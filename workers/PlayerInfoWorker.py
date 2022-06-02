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
    

    def run(self):
        """Running the Worker task
        """
        # Removing old content from tables
        self.clearInfoTable.emit()
        # Checking if this player is being tracked
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
        self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
        if self.cancel:
            return
        """# Loading player information
        self.message.emit("Loading player information")
        for i in range(self.tab.info.rowCount()):
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
            self.setInfoContent.emit(0, gameDatetime.strftime("%d.%m.%Y %H:%M:%S UTC") + " (" + data["create_dt_fuzzy"] + ")")
            self.setInfoContent.emit(1, "(#" + str(data["server_id"]) + ")")
            self.setInfoContent.emit(2, "(#" + str(data["map_id"]) + ")")
            self.setInfoContent.emit(3, data["game_type_cd"].upper() + " (" + data["game_type_descr"] + ")")
            self.setInfoContent.emit(4, data["duration"] + " (" + str(data["duration_secs"]) + " seconds)")
            # Adding players to table
            self.addPlayers(data)
            self.resultMessage.emit("Successfully loaded game information", True)
            for i in range(self.tab.info.rowCount()):
                self.setInfoRowColor.emit(i, None)
            self.sleep(Config.instance()["Settings"]["groupRequestInterval"])
            if self.cancel:
                return
            # Loading additional information
            self.loadAdditionalInformation(data)
        else:
            self.resultMessage.emit("Unable to load game information", False)
            for i in range(self.tab.info.rowCount()):
                self.setInfoRowColor.emit(i, "dark-red")"""