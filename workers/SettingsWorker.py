from email import message
from PyQt5 import QtCore

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *


class SettingsWorker(Worker):
    """Worker class is for executing background tasks
    """


    addSetting = QtCore.pyqtSignal(str, float)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.addSetting.connect(self.tab.addSetting)
    

    def run(self):
        """Running the Worker task
        """
        # Showing message
        self.message.emit("Loading settings into table")
        success = Config.instance().load("Settings")
        # Loading settings
        self.addSetting.emit("exampleSetting", 215.14)
        # Showing result message
        if success:
            message = "Finished loading settings into table"
        else:
            message = "An error occured when loading settings into table"
        self.resultMessage.emit(message, success)