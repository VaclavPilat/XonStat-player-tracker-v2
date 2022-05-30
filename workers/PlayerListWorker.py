from PyQt5 import QtWidgets, QtCore, QtGui
import time

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *


class PlayerListWorker(Worker):
    """Worker class is for executing background tasks
    """


    showPlayer = QtCore.pyqtSignal(dict)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.showPlayer.connect(self.tab.showPlayer)
    

    def run(self):
        """Running the Worker task
        """
        # Checking config file existence
        if not Config.instance().load("Players"):
            self.resultMessage.emit("Cannot find a config file with players", False)
            return
        # Checking player count
        if len(Config.instance()["Players"]) == 0:
            self.resultMessage.emit("No players were found", True)
            return
        # Loading players
        self.message.emit("Loading players from file")
        i = 0
        for player in Config.instance()["Players"]:
            if self.cancel:
                break
            i += 1
            self.progress.emit(i, len(Config.instance()["Players"]))
            self.showPlayer.emit(player)
        self.resultProgress.emit("Finished loading players from file", i, len(Config.instance()["Players"]))
        if self.cancel:
            return