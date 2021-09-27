from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon
from ColoredWidgets import *
import os, qdarkstyle



class Window(QMainWindow):
    """Class for creating a status label and methods for controlling status content
    """


    def __init__(self):
        """Initializes window, adds stylesheet, sets properties using methods implemented by derived classes.
        """
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.__addStylesheet()
        self.__addIcon()
        self.setProperties()
        self.createLayout()
        self.show()
        self.__centerWindow()
    

    def __addStylesheet(self):
        """Adding CSS styling (my own + the one from "qdarkstyle" module)
        """
        # Adding CSS stylesheet from QDarkStyle
        stylesheet = qdarkstyle.load_stylesheet()
        # Adding my own stylesheet
        with open(os.path.join(os.path.dirname(__file__), "Style.css"), "r") as css_file:
            css_content = css_file.read()
            if not css_content == None and not css_content == "":
                stylesheet += css_content
        # Applying stylesheet
        self.setStyleSheet(stylesheet)
    

    def __addIcon(self):
        """Adds an icon to this window
        """
        self.setWindowIcon(QIcon( os.path.join(os.path.dirname(__file__), "Icon.png") )) # Adding icon
    

    def __centerWindow(self):
        """Moving window to the center of the screen
        """
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())