from PyQt5 import QtWidgets, QtCore, QtGui
import time

from Window import *



class Worker(QtCore.QThread):
    """Worker class is for executing background tasks
    """


    message = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int, int)
    resultMessage = QtCore.pyqtSignal(str, bool)
    resultProgress = QtCore.pyqtSignal(str, int, int)
    showRate = QtCore.pyqtSignal(str, str)


    def __init__(self, window: Window):
        """Initialising QtCore.QThread, connecting slots

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
        self.showRate.connect(self.window.status.showRate)
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
    

    def sleep(self, amount: float):
        """Sleep for a specified amount of time while checking if canceling is requested
        """
        division = 10
        for i in range(division):
            time.sleep(amount / division)
            if self.cancel:
                return