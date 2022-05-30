from PyQt5 import QtWidgets, QtCore
from http.client import responses
import re, datetime

from Worker import *
from Requests import *



class GameInfoWorker(Worker):
    """Loading detailed information about a player
    """

    _setInfoTableEnabled = QtCore.pyqtSignal(bool) # Setting enabled property for info table
    _setTableEnabled = QtCore.pyqtSignal(bool) # Setting enabled property for player table
    _showPlayer = QtCore.pyqtSignal(int, str, int, str) # Signal for adding new player into table
    _showGroupName = QtCore.pyqtSignal(str) # Shows name of a player group
    _showServerName = QtCore.pyqtSignal(str) # Showing game server
    _showMapName = QtCore.pyqtSignal(str) # Showing game map
    _showGameMode = QtCore.pyqtSignal(str) # Showing game mode
    _showGameTime = QtCore.pyqtSignal(str) # Showing game time
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._setInfoTableEnabled.connect(self.window.infoTable.setEnabled)
        self._setTableEnabled.connect(self.window.table.setEnabled)
        self._showPlayer.connect(self.window.showPlayer)
        self._showGroupName.connect(self.window.showGroupName)
        self._showServerName.connect(self.window.serverName.setText)
        self._showMapName.connect(self.window.mapName.setText)
        self._showGameMode.connect(self.window.gameMode.setText)
        self._showGameTime.connect(self.window.gameTime.setText)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def before(self):
        """This method is called before this worker is run
        """
        self._setInfoTableEnabled.emit(True)
        self._setTableEnabled.emit(True)
        self._showServerName.emit(None)
        self._showMapName.emit(None)
        self._showGameMode.emit(None)
        self._showGameTime.emit(None)
        

    def run(self):
        """Running the Worker task
        """
        # Checking ID validity
        try:
            gameID = int(re.findall('\d+|$', self.window.gameID.text())[0])
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
                self._setInfoTableEnabled.emit(True)
                self._setTableEnabled.emit(True)
                data = json.loads(response.data.decode('utf-8'))
                serverID, mapID = self.__processData(data)
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
        else:
            # Making additional request
            try:
                # Server name
                response = Requests.instance().request('https://stats.xonotic.org/server/' + serverID)
                if response.status == 200:
                    self._showServerName.emit( json.loads(response.data.decode('utf-8'))["name"] + " (#" + serverID + ")" )
                else:
                    self.resultMessage.emit("An error occured: " + responses[response.status], False)
                    return
                # Map name
                response = Requests.instance().request('https://stats.xonotic.org/map/' + mapID)
                if response.status == 200:
                    self._showMapName.emit( json.loads(response.data.decode('utf-8'))["name"] + " (#" + mapID + ")" )
                else:
                    self.resultMessage.emit("An error occured: " + responses[response.status], False)
                    return
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
                self._showGroupName.emit(settings["group"].upper())
            for player in data[array]:
                if settings["color"] == None:
                    if "color" in player:
                        if player["color"] == "":
                            color = "blue"
                        else:
                            color = player["color"]
                else:
                    color = settings["color"]
                self._showPlayer.emit(player["player_id"], player["nick"], player["score"], color)
        # Showing game info
        self._showServerName.emit( "Server #" + str(data["server_id"]) )
        self._showMapName.emit( "Map #" + str(data["map_id"]) )
        self._showGameMode.emit( data["game_type_descr"]  + " (" + data["game_type_cd"].upper() + ")" )
        gameDatetime = datetime.datetime.strptime(data["create_dt"], "%Y-%m-%dT%H:%M:%SZ")
        self._showGameTime.emit( gameDatetime.strftime("%d.%m.%Y %H:%M:%S UTC") )
        return str(data["server_id"]), str(data["map_id"])