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
        self.message.emit("Loading players whose name match searched phrase")
        self.showPlayer.emit(137012, "napalm")