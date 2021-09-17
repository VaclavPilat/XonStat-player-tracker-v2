import urllib3

class Player(dict):
    """ Class for interacting with player data """

    def __init__(self, data: dict):
        super().__init__()
        """ Initializing a few variables """
        self.update(data)
        self["profile"] = "https://stats.xonotic.org/player/" + str(data["id"])

    
    def load_profile(self):
        """ Loading player profile """
        if not self._pool_manager == None:
            self._pool_manager = urllib3.PoolManager()
        response = _pool_manager.request("GET", self["profile"])
        self.profile_html = response.data