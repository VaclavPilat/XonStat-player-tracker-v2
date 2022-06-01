from tabs.TabInfo import *


class GameInfo(TabInfo):
    """Class for showing game information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Game ID
        """
        super().__init__(parent, identifier)
        self.name = "Game Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter game ID")
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if super().startLoading():
            self.status.message("Loading game information")