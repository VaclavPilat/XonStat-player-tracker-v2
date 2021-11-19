import urllib3, webbrowser, json, time, re, colorsys
from xml.sax.saxutils import escape
from http.client import responses
from Functions import *
from Config import *



class Player(dict):
    """Class for interacting with player data
    """


    def __init__(self, data: dict):
        """Initializing a few variables

        Args:
            data (dict): Player data
        """
        self.window = None # PlayerInfo window instance
        self.profileInfo = None # HTML source of the player's profile page
        self.gameSources = [] # List containing HTML sources of recently played games
        super().__init__()
        self.update(data)
        self.profile = "https://stats.xonotic.org/player/" + str(data["id"])
        self.http = urllib3.PoolManager() # Pool manager for sending request with urllib3
        self.headers = {'Accept': 'application/json'}
        self.timeout = urllib3.util.Timeout(2)


    def showProfile(self):
        """Opening player profile in a new tab of a browser
        """
        webbrowser.open(self.profile, new=2)

    
    def loadProfile(self):
        """Loading player profile
        """
        try:
            response = self.http.request('GET', self.profile, headers=self.headers, timeout=self.timeout)
            if response.status == 200:
                self.profileInfo = json.loads(response.data.decode('utf-8'))
                self.error = None
            else:
                self.error = responses[response.status]
        except urllib3.exceptions.HTTPError:
            self.error = "Cannot connect to XonStat"
        except Exception as e:
            self.error = type(e).__name__
            printException()
    

    def __processColor(self, color: str):
        """Processes color from player nickname and returns it
        Making darker colors less dark (like on XonStat webpage)

        Args:
            hex (str): Hexadecimal 3-digit RGB color
        
        Returns:
            [str]: Processed decimal RGB color
        """
        h, l, s = colorsys.rgb_to_hls(int(color[0]*2, 16) / 255, int(color[1]*2, 16) / 255, int(color[2]*2, 16) / 255)
        if l < 0.5:
            l = 0.5
        if l > 1:
            l = 1
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return "rgb(" + str(r * 255) + "," + str(g * 255) + "," + str(b * 255) + ")"
    

    def __processName(self, name: str):
        """Processes nickname from xonotic syntax to HTML

        Args:
            name (str): Raw nickname loaded from XonStat
        """
        name = escape(name)
        for colorCode in re.finditer(r"(\^x*[0-9a-fA-F]{3})", name):
            name = name.replace(colorCode.group(), '<span style="color:' + self.__processColor( colorCode.group()[2:] ) + '">')
        # Replacing special characters
        for character, replacement in Config.instance()["Characters"].items():
            name = name.replace(character, replacement)
        return name
    

    def loadName(self) -> str:
        """Loads and returns current player name from profile

        Returns:
            str: Current player name
        """
        try:
            if self.error is not None:
                raise Exception
            self.name = self.__processName( self.profileInfo["player"]["nick"] )
        except Exception as e:
            self.name = None
            if self.error is None:
                self.error = "Cannot load name"
        return self.name
    

    def loadSince(self) -> str:
        """Loads the first time this player played a game

        Returns:
            str: The first time this player joined a game
        """
        try:
            if self.error is not None:
                raise Exception
            self.since = self.profileInfo["player"]["joined_fuzzy"]
        except Exception as e:
            self.since = None
            if self.error is None:
                self.error = "Cannot load since"
        return self.since
    

    def loadActive(self) -> str:
        """Loads the last time this player played a game

        Returns:
            str: The last time this player joined a game
        """
        try:
            if self.error is not None:
                raise Exception
            self.active = self.profileInfo["overall_stats"]["overall"]["last_played_fuzzy"]
        except Exception as e:
            self.active = None
            if self.error is None:
                self.error = "Cannot load active"
        return self.active
    

    def  getActiveColor(self) -> str:
        """Gets text color for "active" label based on its content

        Returns:
            str: Text color value, defined in stylesheets
        """
        if self.active is None:
            return None
        else:
            # Extracting number from string
            number = 0
            for substring in self.active.split():
                if substring.isdigit():
                    number = int(substring)
            # Comparing string
            if "year" in self.active or "month" in self.active:
                color = "active-7"
            else:
                if "day" in self.active:
                    if number > 7:
                        color = "active-6"
                    elif number > 1:
                        color = "active-5"
                    else:
                        color = "active-4"
                else:
                    if "hour" in self.active:
                        if number >= 20:
                            color = "active-4"
                        elif number >=2:
                            color = "active-3"
                        else:
                            color = "active-2"
                    else:
                        color = "active-1"
            return color
    

    def loadTime(self) -> str:
        """Loads total time this player spent playing

        Returns:
            str: Total time this player spent playing
        """
        try:
            if self.error is not None:
                raise Exception
            self.time = str(round(self.profileInfo["overall_stats"]["overall"]["total_playing_time"] / 3600)) + " hours"
        except Exception as e:
            self.time = None
            if self.error is None:
                self.error = "Cannot load time time spent"
        return self.time
    

    def loadRecentGames(self):
        """Loads recently played games
        """
        current = 0
        maximum = 0
        # Loading list of games
        gameListUrl = "https://stats.xonotic.org/games?player_id=" + str(self["id"])
        try:
            for i in range( Config.instance()["Settings"]["gameListCount"] ):
                # Canceling
                if self.window.worker.cancel:
                    raise StopIteration
                # Getting list of games
                gameListResponse = self.http.request('GET', gameListUrl, headers=self.headers, timeout=self.timeout)
                if gameListResponse.status == 200:
                    gameList = json.loads(gameListResponse.data.decode('utf-8'))
                    if gameList is not None:
                        maximum += len(gameList)
                    else:
                        raise StopIteration
                    for link in gameList:
                        # Canceling
                        if self.window.worker.cancel:
                            raise StopIteration
                        try:
                            time.sleep( Config.instance()["Settings"]["singleRequestInterval"] )
                            current += 1
                            try:
                                gameResponse = self.http.request("GET", "https://stats.xonotic.org/game/" + str(link["game_id"]), headers=self.headers, timeout=self.timeout)
                                if gameResponse.status == 200:
                                    gameObject = json.loads(gameResponse.data.decode('utf-8'))
                                    yield [current, maximum, gameObject]
                            except:
                                printException()
                        except:
                            printException()
                    # Getting new URL
                    if gameList is not None and len(gameList) > 0:
                        gameListUrl = "https://stats.xonotic.org/games?player_id=" + str(self["id"]) + "&start_game_id=" + str(gameList[-1]["game_id"] -1)
                    else:
                        raise StopIteration
                else:
                    self.error = responses[gameListResponse.status]
                if not i == Config.instance()["Settings"]["gameListCount"] -1:
                    time.sleep( Config.instance()["Settings"]["groupRequestInterval"] )
        except StopIteration:
            pass
        except:
            printException()