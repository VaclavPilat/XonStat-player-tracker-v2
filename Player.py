import urllib3, webbrowser
from bs4 import BeautifulSoup
from http.client import responses
import time
from Functions import *
from Settings import *


class Player(dict):
    """Class for interacting with player data
    """


    def __init__(self, data: dict):
        """Initializing a few variables

        Args:
            data (dict): Player data
        """
        self.window = None # PlayerInfo window instance
        self.profileSource = None # HTML source of the player's profile page
        self.__profileSoup = None # BeautifulSoup parser for parsing player profile
        self.gameSources = [] # List containing HTML sources of recently played games
        super().__init__()
        self.update(data)
        self.profile = "https://stats.xonotic.org/player/" + str(data["id"])
        self.__poolManager = urllib3.PoolManager() # Pool manager for sending request with urllib3
    

    def showProfile(self):
        """Opening player profile in a new tab of a browser
        """
        webbrowser.open(self.profile, new=2)

    
    def loadProfile(self):
        """Loading player profile
        """
        try:
            response = self.__poolManager.request("GET", self.profile, timeout=urllib3.util.Timeout(2))
            if response.status == 200:
                self.profileSource = response.data
                self.__profileSoup = BeautifulSoup(self.profileSource, "html.parser")
                if "Player Information" in str(self.profileSource):
                    self.error = None
                else:
                    self.error = "Profile might not exist"
            else:
                self.error = responses[response.status]
        except urllib3.exceptions.HTTPError:
            self.error = "Cannot connect to stats"
        except:
            self.error = "Error: " + type(e).__name__
    

    def loadName(self, element = None) -> str:
        """Loads and returns current player name from profile

        Returns:
            str: Current player name
        """
        saveName = False
        try:
            if element is None:
                if self.error is not None:
                    raise Exception
                element = self.__profileSoup.find("h2")
                saveName = True
            if not element.find() == None:
                name = str(element.find())
            else:
                name = element.text.strip()
        except:
            name = None
            if self.error is None:
                self.error = "Profile contains wrong info"
        # Saving and returning name
        if saveName:
            self.name = name
        return name
    

    def loadSince(self) -> str:
        """Loads the first time this player played a game

        Returns:
            str: The first time this player joined a game
        """
        try:
            if self.error is not None:
                raise Exception
            self.since = self.__profileSoup.select("span.abstime")[0].text
        except:
            self.since = None
            if self.error is None:
                self.error = "Profile contains wrong info"
        return self.since
    

    def loadActive(self) -> str:
        """Loads the last time this player played a game

        Returns:
            str: The last time this player joined a game
        """
        try:
            if self.error is not None:
                raise Exception
            self.active = self.__profileSoup.select("span.abstime")[1].text
        except:
            self.active = None
            if self.error is None:
                self.error = "Profile contains wrong info"
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
            time = self.__profileSoup.select("div.cell.small-6 p")[0].select("small")[1].text
            hours = 0
            timeList = time.split(" ")
            for i in range(0, (len(timeList) // 2) * 2, 2):
                if "day" in timeList[i + 1]:
                    hours += int(timeList[i]) * 24
                elif "hour" in timeList[i + 1]:
                    hours += int(timeList[i])
            self.time = str(hours) + " hours"
        except:
            self.time = None
            if self.error is None:
                self.error = "Profile contains wrong info"
        return self.time
    

    def loadRecentGames(self):
        """Loads recently played games
        """
        current = 0
        maximum = 0
        gameListUrl = 'https://stats.xonotic.org/games?player_id=' + str(self["id"])
        # Getting list of games
        try:
            for i in range(Settings.instance()["gameListCount"]):
                # Canceling
                if self.window.worker.cancel:
                    raise StopIteration
                # Getting list of games
                gameListResponse = self.__poolManager.request("GET", gameListUrl, timeout=urllib3.util.Timeout(2))
                if gameListResponse.status == 200:
                    gameListSoup = BeautifulSoup(gameListResponse.data, "html.parser")
                    gameListLinks = gameListSoup.select("tr > .text-center > a.button")
                    # Looping through game links
                    maximum += len(gameListLinks)
                    for gameLink in gameListLinks:
                        if self.window.worker.cancel:
                            raise StopIteration
                        try:
                            time.sleep(Settings.instance()["singleRequestInterval"])
                            current += 1
                            gameUrl = 'https://stats.xonotic.org' + gameLink["href"]
                            try:
                                gameResponse = self.__poolManager.request("GET", gameUrl, timeout=urllib3.util.Timeout(2))
                                if gameResponse.status == 200:
                                    gameSoup = BeautifulSoup(gameResponse.data, "html.parser")
                                    yield [current, maximum, gameSoup]
                            except:
                                printException()
                        except:
                            printException()
                else:
                    self.error = responses[gameListResponse.status]
                # Getting new URL
                nextPageElements = gameListSoup.select('a[name="Next Page"]')
                if len(nextPageElements) >= 0:
                    gameListUrl = 'https://stats.xonotic.org' + nextPageElements[0]["href"]
                else:
                    raise StopIteration
                if not i == Settings.instance()["gameListCount"] -1:
                    time.sleep(Settings.instance()["groupRequestInterval"])
        except StopIteration:
            pass
        except:
            printException()