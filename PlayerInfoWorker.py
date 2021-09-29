from Worker import *
from ColoredWidgets import *



class PlayerInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _showName = pyqtSignal(str) # Showing current player name
    _showSince = pyqtSignal(str) # Showing since when this player is playing
    _showActive = pyqtSignal(str) # Showing the last time this player joined a game
    _setActiveColor = pyqtSignal(str) # Setting a color to "active" label
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._showName.connect(self.window.name.setText)
        self._showSince.connect(self.window.since.setText)
        self._showActive.connect(self.window.active.setText)
        self._setActiveColor.connect(self.window.active.setColor)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.window.status.message("Loading information from player profile")
        

    def run(self):
        """Running the Worker task
        """
        self.window.player.loadProfile()
        # Filling in player info
        self.window.table.setRowColor(0, "dark-yellow")
        self._showName.emit(self.window.player.loadName())
        if self.window.player.error:
            self.window.table.setRowColor(0, "dark-red")
        else:
            self.window.table.setRowColor(0, None)
        
        self.window.table.setRowColor(1, "dark-yellow")
        self._showSince.emit(self.window.player.loadSince())
        if self.window.player.error:
            self.window.table.setRowColor(1, "dark-red")
        else:
            self.window.table.setRowColor(1, None)

        self.window.table.setRowColor(2, "dark-yellow")
        self._showActive.emit(self.window.player.loadActive())
        self._setActiveColor.emit(self.window.player.getActiveColor())
        if self.window.player.error:
            self.window.table.setRowColor(2, "dark-red")
        else:
            self.window.table.setRowColor(2, None)

        # Changing status
        if self.window.player.error is not None:
            self.window.status.resultMessage("An error occured: " + self.window.player.error, False)
        else:
            self.window.status.resultMessage("Successfully loaded player profile")


    def after(self):
        """This method is called after this worker is finished
        """
        pass