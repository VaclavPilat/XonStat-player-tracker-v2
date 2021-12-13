from PyQt5 import QtWidgets, QtCore, QtGui
import os, json

from Functions import *



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
                f = open(filepath, "r", encoding="utf8")
                self[filename.split(".")[0]] = json.loads(f.read())
            # Loading fonts
            folder = os.path.join(os.path.dirname(__file__), "fonts/")
            for filename in os.listdir(folder):
                filepath = folder + filename
                QtGui.QFontDatabase.addApplicationFont(filepath)
            return True
        except:
            return False
    

    def save(filename: str):
        """Saves a selected config file

        Args:
            filename (str): Name of config file
        """
        try:
            filepath = os.path.join(os.path.dirname(__file__), "config/" + filename + ".json")
            f = open(filepath, "w")
            f.write(json.dumps(Config.instance()[filename], sort_keys=False, indent=4))
            f.close()
            return True
        except:
            return False