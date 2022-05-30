from PyQt5 import QtWidgets, QtCore, QtGui
import time

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *


class PlayerListWorker(Worker):
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
        pass
    

    def run(self):
        """Running the Worker task
        """
        if not Config.instance().load("Players"):
            self.resultMessage.emit("Cannot find a config file with players", False)
            return
        if len(Config.instance()["Players"]) == 0:
            self.resultMessage.emit("No players were found", True)
            return
        self.message.emit("Loading players from file")
        self.sleep(10)