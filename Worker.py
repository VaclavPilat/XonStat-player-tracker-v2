from PyQt5.QtCore import QThread
from Window import *



class Worker(QThread):
    """Worker class is for executing background tasks
    """


    def __init__(self, window: Window):
        """Initialising QThread, connecting slots

        Args:
            window (Window): Window object that this class ws instantiated in
        """
        super().__init__()
        self.window = window
        self.cancel = False
        # Connecting slots and signals
        self.started.connect(self.before)
        self.finished.connect(self.after)
        self.connectSlots()
    

    def before(self):
        """This method is called before this worker is run
        """
        pass


    def after(self):
        """This method is called after this worker is finished
        """
        pass