from PyQt5 import QtCore

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *


class PlayerListWorker(Worker):
    """Worker class is for executing background tasks
    """


    addPlayer = QtCore.pyqtSignal(dict)
    insertPlayer = QtCore.pyqtSignal(dict, int)
    removePlayer = QtCore.pyqtSignal(int)
    setRowColor = QtCore.pyqtSignal(int, str)
    updatePlayer = QtCore.pyqtSignal(int, dict)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.addPlayer.connect(self.tab.addPlayer)
        self.insertPlayer.connect(self.tab.addPlayer)
        self.removePlayer.connect(self.tab.removePlayer)
        self.setRowColor.connect(self.tab.table.setRowColor)
        self.updatePlayer.connect(self.tab.updatePlayer)
    

    def run(self):
        """Running the Worker task
        """
        self.sleep(0.1)
        # Checking config file existence
        if not Config.instance().load("Players"):
            self.resultMessage.emit("Cannot find a config file with players", False)
            return
        # Checking player count
        if len(Config.instance()["Players"]) == 0:
            self.resultMessage.emit("No players were found", True)
            return
        # Loading differences from player lists
        self.message.emit("Loading differences from player lists")
        # Getting list of player ID's
        old = [int(self.tab.table.cellWidget(i, 0).text()) for i in range(self.tab.table.rowCount())]
        new = [Config.instance()["Players"][i]["id"] for i in range(len(Config.instance()["Players"]))]
        add = [item for item in new if item not in old]
        remove = [item for item in old if item not in new]
        # Loading player differences
        self.__loadDifferences(old, new, add, remove)
        # Cancelling
        self.sleep( Config.instance()["Settings"]["groupRequestInterval"] )
        if self.cancel:
            return
        # Loading player information
        self.__loadInformation(new)
    

    def __loadDifferences(self, old: list, new: list, add: list, remove: list):
        """Loading differences between player lists

        Args:
            old (list): Old player index list
            new (list): New player index list
            add (list): Player index list to be added
            remove (list): Player index list to be removed
        """
        i = 0
        # Removing unused rows
        remove.reverse()
        for playerID in remove:
            if self.cancel:
                break
            i += 1
            self.removePlayer.emit(old.index(playerID))
            self.progress.emit(i, len(add) + len(remove))
        # Adding new rows
        for playerID in add:
            if self.cancel:
                break
            i += 1
            self.insertPlayer.emit(Config.instance()["Players"][new.index(playerID)], new.index(playerID))
            self.progress.emit(i, len(add) + len(remove))
        self.resultProgress.emit("Finished loading differences from player lists", i, len(add) + len(remove))
    

    def __loadInformation(self, new: list):
        """Loads information about players from XonStat

        Args:
            new (list): New player index list
        """
        self.message.emit("Loading player information")
        i = 0
        correct = 0
        for index in range(len(new)):
            if self.cancel:
                break
            playerID = new[index]
            self.setRowColor.emit(index, "dark-yellow")
            self.sleep( Config.instance()["Settings"]["singleRequestInterval"] )
            response = None
            try:
                response = createRequest("https://stats.xonotic.org/player/" + str(playerID))
                self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
            except:
                pass
            if response is not None and response:
                correct += 1
                self.updatePlayer.emit(index, response.json())
            else:
                self.setRowColor.emit(index, "dark-red")
            i += 1
            self.progress.emit(i, len(new))
        self.resultProgress.emit("Finished loading player information", correct, len(new))