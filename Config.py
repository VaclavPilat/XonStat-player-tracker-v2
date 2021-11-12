from Functions import *
from PyQt5 import QtGui
import os, json



class Config(dict):
    """Singleton for loading settings
    """


    __instance = None # Singeton instance


    def instance():
        """Returns instance of this singleton

        Returns:
            Settings: Settings object instance
        """
        if Config.__instance is None:
            Config.__instance = Config()
            Config.__instance.__load()
        return Config.__instance


    def __load(self):
        """Loading all config files
        """
        try:
            # Loading json from config files into self
            folder = os.path.join(os.path.dirname(__file__), "config/")
            for filename in os.listdir(folder):
                filepath = folder + filename
                f = open(filepath, "r")
                self[filename.split(".")[0]] = json.loads(f.read())
            # Loading fonts
            folder = os.path.join(os.path.dirname(__file__), "fonts/")
            for filename in os.listdir(folder):
                filepath = folder + filename
                QtGui.QFontDatabase.addApplicationFont(filepath)
        except:
            printException()