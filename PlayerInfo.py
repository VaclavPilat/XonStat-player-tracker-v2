from PyQt5.QtWidgets import QVBoxLayout
from Window import *
from Status import *
from ColoredWidgets import *
from Player import *



class PlayerInfo(Window):
    """Class for showing detailed information about players
    """


    def __init__(self, window: Window):
        """Initialising GUI

        Args:
            window (Window): Overview window instance
        """
        super().__init__()
        self.window = window
    

    def setProperties(self):
        """Setting winow properties
        """
        self.setWindowTitle("Player information")
        self.resize(450, 750)
    

    def createLayout(self):
        """Creates widnow layout with widgets
        """
        # Creating the layout itself
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Adding widgets to layout
        # Adding status
        layout.addStretch()
        self.status = Status(self)
        layout.addWidget(self.status)


