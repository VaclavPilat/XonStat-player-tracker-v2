#!/usr/bin/env python3
import urllib3, webbrowser
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
        self.profile = "https://stats.xonotic.org/player/" + str(data["id"])
    

    def show_profile(self):
        """ Opening player profile in a new tab of a browser """
        webbrowser.open(self.profile, new=2)

    
    def load_profile(self, info: bool = False):
        """ Loading player profile """
        try:
            response = self._http.request("GET", self.profile, timeout=urllib3.util.Timeout(3))
            if response.status == 200:
                self._profile_html = response.data
                self._soup = BeautifulSoup(self._profile_html, "html.parser")
                if "Player Information" in str(self._profile_html):
                    self.error = None
                else:
                    self.error = "Profile error"
            else:
                self.error = "Stats error"
        except:
            self.error = "Network error"
    

    def load_name(self) -> str:
        """ Loads and returns current player name from profile """
        if self.error == None:
            name = self._soup.find("h2")
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
    

    def load_active(self) -> str:
        """ Loads the last time this player played a game """
        if self.error == None:
            elements = self._soup.find_all("span", attrs={"class": "abstime"})
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
    

    def  get_active_color(self) -> str:
        """ Gets text color for "active" label based on its content """
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