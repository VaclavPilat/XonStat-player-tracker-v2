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
        # Loading player information
        self.message.emit("Loading player information")