from PyQt5 import QtWidgets, QtCore

from Worker import *



class GameInfoWorker(Worker):
    """Loading detailed information about a player
    """


    _showPlayer = QtCore.pyqtSignal(int, str, str, int) # Signal for adding new player into table
    

    def connectSlots(self):
        """Connecting signals to slots (called from Worker class)
        """
        self._showPlayer.connect(self.window.showPlayer)


    def __init__(self, window: Window):
        """Initialising Worker thread
        """
        super().__init__(window)
    

    def before(self):
        """This method is called before this worker is run
        """
        self.message.emit("Loading game information")
        

    def run(self):
        """Running the Worker task
        """
        pass


    def after(self):
        """This method is called after this worker is finished
        """
        pass