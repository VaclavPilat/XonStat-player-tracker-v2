from PyQt5 import QtWidgets, QtCore, QtGui
import time

from tabs.Tab import *


class Worker(QtCore.QThread):
    """Worker class is for executing background tasks
    """


    message = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int, int)
    resultMessage = QtCore.pyqtSignal(str, bool)
    resultProgress = QtCore.pyqtSignal(str, int, int)
    showRate = QtCore.pyqtSignal(str, str)
    updateRefreshButtons = QtCore.pyqtSignal()


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__()
        self.tab = tab
        self.cancel = False
        # Connecting slots and signals
        self.started.connect(self.before)
        self.finished.connect(self.after)
        self.message.connect(self.tab.status.message)
        self.progress.connect(self.tab.status.progress)
        self.resultMessage.connect(self.tab.status.resultMessage)
        self.resultProgress.connect(self.tab.status.resultProgress)
        self.showRate.connect(self.tab.status.showRate)
        self.updateRefreshButtons.connect(self.tab.parent.updateRefreshButtons)
        self.connectSlots()
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        pass
    

    def before(self):
        """This method is called before this worker is run
        """
        self.updateRefreshButtons.emit()


    def after(self):
        """This method is called after this worker is finished
        """
        self.updateRefreshButtons.emit()
    

    def sleep(self, amount: float):
        """Sleep for a specified amount of time while checking if canceling is requested
        """
        division = 10
        for i in range(division):
            time.sleep(amount / division)
            if self.cancel:
                return