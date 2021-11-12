from Functions import *
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
        # Getting abolute path to config folder
        folder = os.path.join(os.path.dirname(__file__), "config/")
        # Loading json from files into self
        try:
            for filename in os.listdir(folder):
                filepath = folder + filename
                f = open(filepath, "r")
                self[filename.split(".")[0]] = json.loads(f.read())
        except:
            printException()