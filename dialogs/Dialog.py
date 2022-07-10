from PyQt5 import QtWidgets


class Dialog(QtWidgets.QDialog):
    """Class for creating a dialog window
    """


    def __init__(self, parent, identifier: int = None):
        """Initializes a dialog window

        Args:
            parent (QMainWindow): Dialog parent
            identifier (int): Player ID. Optional. Defaults to None
        """
        self.id = identifier
        super().__init__(parent)
        self.setFixedSize(500, 250)
        self.createLayout()
        self.exec()
    
    
    def createLayout(self):
        """Creating dialog layout
        """
        pass