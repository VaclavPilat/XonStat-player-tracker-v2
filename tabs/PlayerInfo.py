from tabs.TabInfo import *
from widgets.ColoredButtons import *
from workers.PlayerInfoWorker import *


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
        # Creating an info table
        self.layout.addWidget(self.createInfoTable(["Player nickname", "Player description", "Current player name", "Playing since", "Last active", "Total time spent playing", "Games played this week"]))
        # Adding server info buttons
    

    def startLoading(self):
        """Starting page (re)loading
        """
        if self.worker is None:
            self.worker = GameInfoWorker(self)
        if super().startLoading():
            self.info.setEnabled(True)
            if (self.worker.isFinished() or not self.worker.isRunning()):
                self.worker.start()
        else:
            self.info.setEnabled(False)
    

    def setInfoTextColor(self, row: int, color: str):
        """Setting text color of a content label in an info table

        Args:
            row (int): Row index
            color (str): Color class
        """
        self.info.cellWidget(row, 1).layout().itemAt(0).widget().setColor(color)