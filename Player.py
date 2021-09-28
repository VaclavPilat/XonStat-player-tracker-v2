#!/usr/bin/env python3
import urllib3, webbrowser
from bs4 import BeautifulSoup


class Player(dict):
    """Class for interacting with player data
    """


    window = None # PlayerInfo window instance
    __poolManager = urllib3.PoolManager() # Pool manager for sending request with urllib3
    __profileSource = None # HTML source of the player's profile page
    __soup = None # BeautifulSoup parser


    def __init__(self, data: dict):
        """Initializing a few variables

        Args:
            data (dict): Player data
        """
        super().__init__()
        self.update(data)
        self.profile = "https://stats.xonotic.org/player/" + str(data["id"])
    

    def showProfile(self):
        """Opening player profile in a new tab of a browser
        """
        webbrowser.open(self.profile, new=2)

    
    def loadProfile(self):
        """Loading player profile
        """
        try:
            response = self.__poolManager.request("GET", self.profile, timeout=urllib3.util.Timeout(3))
            if response.status == 200:
                self.__profileSource = response.data
                self.__soup = BeautifulSoup(self.__profileSource, "html.parser")
                if "Player Information" in str(self.__profileSource):
                    self.error = None
                else:
                    self.error = "Profile error"
            else:
                self.error = "Stats error"
        except:
            self.error = "Network error"
    

    def loadName(self) -> str:
        """Loads and returns current player name from profile

        Returns:
            str: Current player name
        """
        if self.error == None:
            name = self.__soup.find("h2")
            if not name == None:
                if not name.find() == None:
                    self.name = str(name.find())
                else:
                    self.name = name.text.strip()
            else:
                self.error = "Profile error"
        else:
            self.name = None
        return self.name
    

    def loadActive(self) -> str:
        """Loads the last time this player played a game

        Returns:
            str: The last time this player joined a game
        """
        if self.error == None:
            elements = self.__soup.find_all("span", attrs={"class": "abstime"})
            if not elements == None:
                if len(elements) >= 2:
                    self.active = elements[1].text
                else: 
                    self.active = None
            else:
                self.error = "Profile error"
        else:
            self.active = None
        return self.active
    

    def  getActiveColor(self) -> str:
        """Gets text color for "active" label based on its content

        Returns:
            str: Text color value, definec in stylesheets
        """
        if self.active == None:
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