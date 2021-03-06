from PyQt5 import QtCore

from tabs.Tab import *
from workers.Worker import *


class TabInfoWorker(Worker):
    """Worker class is for executing background tasks
    """


    setInfoContent = QtCore.pyqtSignal(int, str)
    addInfoContent = QtCore.pyqtSignal(int, str)
    setInfoRowColor = QtCore.pyqtSignal(int, str)
    setInputEnabled = QtCore.pyqtSignal(bool)


    def __init__(self, tab: Tab):
        """Initialising QtCore.QThread, connecting slots

        Args:
            tab (Tab): Tab object that this class was instantiated in
        """
        super().__init__(tab)
    

    def connectSlots(self):
        """Connecting signals to slots. This method is called in init.
        """
        self.setInfoContent.connect(self.tab.setInfoContent)
        self.addInfoContent.connect(self.tab.addInfoContent)
        self.setInfoRowColor.connect(self.tab.info.setRowColor)
        self.setInputEnabled.connect(self.tab.identifierInput.setEnabled)
    

    def before(self):
        """This method is called before this worker is run
        """
        super().before()
        self.setInputEnabled.emit(False)
        if self.tab.id is not None:
            self.setInfoContent.emit(0, str(self.tab.id))


    def after(self):
        """This method is called after this worker is finished
        """
        super().after()
        self.setInputEnabled.emit(True)