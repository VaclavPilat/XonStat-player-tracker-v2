from PyQt5 import QtWidgets, QtCore, QtGui
import time

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *


class PlayerListWorker(Worker):
    """Worker class is for executing background tasks
    """


    addPlayer = QtCore.pyqtSignal(dict)
    insertPlayer = QtCore.pyqtSignal(dict, int)
    removePlayer = QtCore.pyqtSignal(int)


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
        # First loading
        if self.tab.table.rowCount() == 0:
            self.message.emit("Loading players from file")
            # Loading players
            i = 0
            for player in Config.instance()["Players"]:
                if self.cancel:
                    break
                i += 1
                self.progress.emit(i, len(Config.instance()["Players"]))
                self.addPlayer.emit(player)
            self.resultProgress.emit("Finished loading players from file", i, len(Config.instance()["Players"]))
        else:
            self.message.emit("Loading differences from player lists")
            # Getting list of player ID's
            old = [int(self.tab.table.cellWidget(i, 0).text()) for i in range(self.tab.table.rowCount())]
            new = [Config.instance()["Players"][i]["id"] for i in range(len(Config.instance()["Players"]))]
            add = [item for item in new if item not in old]
            remove = [item for item in old if item not in new]
            i = 0
            # Removing unused rows
            remove.reverse()
            for id in remove:
                if self.cancel:
                    break
                i += 1
                self.removePlayer.emit(old.index(id))
                self.progress.emit(i, len(add) + len(remove))
            # Adding new rows
            for id in add:
                if self.cancel:
                    break
                i += 1
                self.insertPlayer.emit(Config.instance()["Players"][new.index(id)], new.index(id))
                self.progress.emit(i, len(add) + len(remove))
            self.resultProgress.emit("Finished loading differences from player lists", i, len(add) + len(remove))
        # Cancelling
        if self.cancel:
            return