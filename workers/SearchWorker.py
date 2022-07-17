from PyQt5 import QtCore
import datetime

from workers.Worker import *
from misc.Functions import *


class SearchWorker(Worker):
    """Worker class is for executing background tasks
    """


    showPlayer = QtCore.pyqtSignal(int, str)


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
    

    def run(self):
        """Running the Worker task
        """
        # Showing message
        self.message.emit("Loading players whose name match searched phrase")
        # Getting search phrase
        phrase = self.tab.searchBar.text()
        # Loading list of players
        try:
            response = createRequest("https://stats.xonotic.org/players?nick=" + phrase)
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Checking response
        if response is not None and response:
            data = response.json()
            for player in data["players"]:
                self.showPlayer.emit(player["player_id"], processNick(player["nick"]))
            self.resultMessage.emit("Successfully loaded list of players", True)
        else:
            self.resultMessage.emit("Failed to load list of players", False)