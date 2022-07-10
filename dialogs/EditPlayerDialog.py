from PyQt5 import QtWidgets

from dialogs.Dialog import *


class EditPlayerDialog(Dialog):
    """Class for creating a dialog window for editing player information
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
        self.setWindowTitle("Edit player information")