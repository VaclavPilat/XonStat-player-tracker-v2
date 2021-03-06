from PyQt5 import QtCore
import re

from workers.Worker import *
from misc.Config import *
from tabs.Tab import *
from misc.Functions import *


class SettingsWorker(Worker):
    """Worker class is for executing background tasks
    """


    addSettingInt = QtCore.pyqtSignal(str, int)
    addSettingFloat = QtCore.pyqtSignal(str, float)
    addSettingBool = QtCore.pyqtSignal(str, bool)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.addSettingInt.connect(self.tab.addSetting)
        self.addSettingFloat.connect(self.tab.addSetting)
        self.addSettingBool.connect(self.tab.addSetting)
    

    def processSettingName(self, name: str):
        """Processes setting name into a more readable variant

        Args:
            name (str): Setting name in CamelCase

        Returns:
            str: New, more readable, name
        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name)
        return " ".join([m.group(0) for m in matches]).lower().capitalize()
    

    def run(self):
        """Running the Worker task
        """
        # Showing message
        self.message.emit("Loading settings into table")
        success = Config.instance().load("Settings")
        # Loading settings
        for name, value in Config.instance()["Settings"].items():
            name = self.processSettingName(name)
            if type(value) == int:
                self.addSettingInt.emit(name, value)
            elif type(value) == float:
                self.addSettingFloat.emit(name, value)
            elif type(value) == bool:
                self.addSettingBool.emit(name, value)
        # Showing result message
        if success:
            message = "Finished loading settings into table"
        else:
            message = "An error occured when loading settings into table"
        self.resultMessage.emit(message, success)