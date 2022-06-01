from tabs.TabInfo import *


class PlayerInfo(TabInfo):
    """Class for showing player information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Player ID
        """
        super().__init__(parent, identifier)
        self.name = "Player Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter player ID")
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if super().startLoading():
            self.status.message("Loading player information")