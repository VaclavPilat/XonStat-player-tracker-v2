from PyQt5 import QtCore

from tabs.Tab import *
from workers.Worker import *


class TabInfoWorker(Worker):
    """Worker class is for executing background tasks
    """


    clearTable = QtCore.pyqtSignal()
    setInfoContent = QtCore.pyqtSignal(int, str)
    addInfoContent = QtCore.pyqtSignal(int, str)
    clearInfoTable = QtCore.pyqtSignal()
    setInfoRowColor = QtCore.pyqtSignal(int, str)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.clearTable.connect(lambda: self.tab.players.setRowCount(0))
        self.setInfoContent.connect(self.tab.setInfoContent)
        self.addInfoContent.connect(self.tab.addInfoContent)
        self.clearInfoTable.connect(self.tab.clearInfoTable)
        self.setInfoRowColor.connect(self.tab.info.setRowColor)