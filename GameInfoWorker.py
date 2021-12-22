from PyQt5 import QtWidgets, QtCore
from http.client import responses

from Worker import *
from Requests import *



class GameInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _showPlayer = QtCore.pyqtSignal(int, str, str, int, str) # Signal for adding new player into table
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._showPlayer.connect(self.window.showPlayer)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
        

    def run(self):
        """Running the Worker task
        """
        # Checking ID validity
        try:
            gameID = int(self.window.gameID.text())
            if gameID <= 0:
                raise ValueError
        except:
            self.resultMessage.emit("Invalid game ID", False)
            return
        # Making a request
        try:
            self.message.emit("Loading data of game #" + str(gameID))
            response = Requests.instance().request('https://stats.xonotic.org/game/' + str(gameID))
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                self.__processData(data)
                self.resultMessage.emit("Successfully loaded game data", True)
            else:
                self.resultMessage.emit("An error occured: " + responses[response.status], False)
                return
            self.showRate.emit( response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"] )
        except urllib3.exceptions.HTTPError:
            self.resultMessage.emit("An error occured: " + "Cannot connect to XonStat", False)
        except Exception as e:
            self.resultMessage.emit("An error occured: " + type(e).__name__, False)
            printException()
    

    def __processData(self, data: dict):
        """Processing game data and adding players into table

        Args:
            data (dict): Dictinary with data from JSON
        """
        self.message.emit("Processing game data")
        playerArrays = {
            "player_game_stats": None, 
            "forfeits": "grey", 
            "spectators": "grey"
        }
        for array, colorPreset in playerArrays.items():
            for player in data[array]:
                if colorPreset == None:
                    if "color" in player:
                        color = player["color"]
                else:
                    color = colorPreset
                self._showPlayer.emit(player["player_id"], player["nick"], "", player["score"], color)


    def after(self):
        """This method is called after this worker is finished
        """
        pass