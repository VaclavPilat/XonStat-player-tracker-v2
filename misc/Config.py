from PyQt5 import QtGui
import os, json


class Config(dict):
    """Singleton for loading settings
    """


    __instance = None # Singeton instance


    def instance():
        """Returns instance of this singleton

        Returns:
            Config: Config object instance
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
            folder = os.path.join(os.path.dirname(__file__), "../config/")
            for string in os.listdir(folder):
                filename = string.split(".")[0]
                Config.instance().load(filename)
            # Loading fonts
            folder = os.path.join(os.path.dirname(__file__), "../fonts/")
            for filename in os.listdir(folder):
                filepath = folder + filename
                QtGui.QFontDatabase.addApplicationFont(filepath)
            return True
        except:
            return False
    

    def load(self, filename: str):
        """Loads a selected config file

        Args:
            filename (str): Name of a config file
        """
        try:
            filepath = os.path.join(os.path.dirname(__file__), "../config/" + filename + ".json")
            f = open(filepath, "r", encoding="utf8")
            Config.instance()[filename] = json.loads(f.read())
            f.close()
            return True
        except:
            return False
    

    def save(self, filename: str):
        """Saves a selected config file

        Args:
            filename (str): Name of config file
        """
        try:
            filepath = os.path.join(os.path.dirname(__file__), "../config/" + filename + ".json")
            f = open(filepath, "w")
            f.write(json.dumps(Config.instance()[filename], sort_keys=False, indent=4))
            f.close()
            return True
        except:
            return False