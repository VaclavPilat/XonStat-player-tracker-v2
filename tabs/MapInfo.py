from tabs.TabInfo import *


class MapInfo(TabInfo):
    """Class for showing map information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Map ID
        """
        super().__init__(parent, identifier)
        self.name = "Map Info"
    

    def createLayout(self):
        """Creating tab layout
        """
        super().createLayout()
        self.identifierInput.setPlaceholderText("Enter map ID")
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if super().startLoading():
            self.status.message("Loading map information")