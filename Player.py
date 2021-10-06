#!/usr/bin/env python3
import urllib3, webbrowser
from bs4 import BeautifulSoup
from http.client import responses
import time


class Player(dict):
    """Class for interacting with player data
    """


    window = None # PlayerInfo window instance
    profileSource = None # HTML source of the player's profile page
    __profileSoup = None # BeautifulSoup parser for parsing player profile
    gameSources = [] # List containing HTML sources of recently played games


    def __init__(self, data: dict):
        """Initializing a few variables

        Args:
            data (dict): Player data
        """
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
        except Exception as e:
            self.error = "Error: " + type(e).__name__
    

    def loadName(self) -> str:
        """Loads and returns current player name from profile

        Returns:
            str: Current player name
        """
        try:
            if self.error is not None:
                raise Exception
            name = self.__profileSoup.find("h2")
            if not name.find() == None:
                self.name = str(name.find())
            else:
                self.name = name.text.strip()
        except:
            self.name = None
            if self.error is None:
                self.error = "Profile contains wrong info"
        return self.name
    

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
            time = self.__profileSoup.select("div.cell.small-6 p")[1].select("small")[0].text
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
    

    def loadRecentGames(self, pages: int = 5):
        """Loads recently played games

        Args:
            pages (int, optional): Maximum number of pages the cycle will go through. Defaults to 10.
        """
        current = 0
        maximum = 0
        gameListUrl = 'https://stats.xonotic.org/games?player_id=' + str(self["id"])
        try:
            # Getting list of games
            response = self.__poolManager.request("GET", gameListUrl, timeout=urllib3.util.Timeout(2))
            if response.status == 200:
                gameListSource = response.data
                soup = BeautifulSoup(gameListSource, "html.parser")
                gameLinks = soup.select("tr > .text-center > a.button")
                # Looping through game links
                maximum += len(gameLinks)
                for gameLink in gameLinks:
                    try:
                        time.sleep(0.2)
                        current += 1
                        gameUrl = 'https://stats.xonotic.org' + gameLink["href"]
                        yield [current, maximum, gameUrl]
                    except Exception as e:
                        print("Error: " + type(e).__name__)
                        pass
            else:
                self.error = responses[response.status]
        except Exception as e:
            print("Error: " + type(e).__name__)
            pass