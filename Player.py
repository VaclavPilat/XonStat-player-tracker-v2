import urllib3
from bs4 import BeautifulSoup

class Player(dict):
    """ Class for interacting with player data """


    _http = urllib3.PoolManager() # Pool manager for sending request with urllib3
    _profile_html = None # HTML source of the player's profile page
    _soup = None # BeautifulSoup parser


    def __init__(self, data: dict):
        super().__init__()
        """ Initializing a few variables """
        self.update(data)
        self["profile"] = "https://stats.xonotic.org/player/" + str(data["id"])

    
    def load_profile(self, info: bool = False):
        """ Loading player profile """
        response = self._http.request("GET", self["profile"])
        if response.status == 200:
            self.correct = True
            self._profile_html = response.data
            self._soup = BeautifulSoup(self._profile_html, "html.parser")
        else:
            self.correct = False
    
    def load_name(self) -> str:
        """ Loads and returns current player name from profile """
        if self.correct:
            name = self._soup.find("h2")
            if not name.find() == None:
                self["name"] = str(name.find())
            else:
                self["name"] = name.text.strip()
        else:
            self["name"] =  "---"
        return self["name"]