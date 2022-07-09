from PyQt5 import QtCore

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *


class SettingsWorker(Worker):
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
        # Showing message
        self.message.emit("Loading settings into table")