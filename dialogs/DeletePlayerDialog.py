from PyQt5 import QtWidgets

from dialogs.Dialog import *


class DeletePlayerDialog(Dialog):
    """Class for creating a dialog window for delting players
    """


    def __init__(self, parent, identifier: int = None):
        """Initializes a dialog window

        Args:
            parent (QMainWindow): Dialog parent
            identifier (int): Player ID. Optional. Defaults to None
        """
        super().__init__(parent, identifier)
    
    
    def createLayout(self):
        """Creating dialog layout
        """
        self.setWindowTitle("Delete player #" + str(self.id) + " ?")