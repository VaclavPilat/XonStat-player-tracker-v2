from PyQt5.QtCore import QThread, pyqtSignal
from Window import *



class Worker(QThread):
    """Worker class is for executing background tasks
    """


    message = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    resultMessage = pyqtSignal(str, bool)
    resultProgress = pyqtSignal(str, int, int)


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
        self.message.connect(self.window.status.message)
        self.progress.connect(self.window.status.progress)
        self.resultMessage.connect(self.window.status.resultMessage)
        self.resultProgress.connect(self.window.status.resultProgress)
        self.connectSlots()
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        pass
    

    def before(self):
        """This method is called before this worker is run
        """
        pass


    def after(self):
        """This method is called after this worker is finished
        """
        pass