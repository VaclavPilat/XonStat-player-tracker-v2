from Functions import *
import os, json



class Settings(dict):
    """Singleton for loading settings
    """


    __instance = None # Singeton instance


    def instance():
        """Returns instance of this singleton

        Returns:
            Settings: Settings object instance
        """
        if Settings.__instance is None:
            Settings.__instance = Settings()
            Settings.__instance.__load()
        return Settings.__instance


    def __load(self):
        """Loading settings from json
        """
        # Getting abolute path to file
        absolutePath = os.path.join(os.path.dirname(__file__), "Settings.json") # Absolute path to the file with players
        # Opening file
        try:
            if os.path.isfile(absolutePath):
                f = open(absolutePath, "r")
                self.update(json.loads(f.read()))
        except:
            printException()