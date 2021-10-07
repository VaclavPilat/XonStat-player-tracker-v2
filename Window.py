from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon
from ColoredWidgets import *
import os, qdarkstyle



class Window(QMainWindow):
    """Class for creating a status label and methods for controlling status content
    """


    def __init__(self):
        """Initializes window, adds stylesheet, sets properties using methods implemented by derived classes.
        """
        self.__closing = False
        self.worker = None
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.__addStylesheet()
        self.__addIcon()
        self.setProperties()
        self.createLayout()
        self.show()
        self.__centerWindow()
        self.destroyed.connect(lambda: print(str(type(self)) + " window destroyed"))
    

    def __addStylesheet(self):
        """Adding CSS styling (my own + the one from "qdarkstyle" module)
        """
        # Adding CSS stylesheet from QDarkStyle
        stylesheet = qdarkstyle.load_stylesheet()
        # Adding my own stylesheet
        with open(os.path.join(os.path.dirname(__file__), "Style.css"), "r") as myCSSFile:
            myCSS = myCSSFile.read()
            if myCSS is not None and myCSS != "":
                stylesheet += myCSS
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
    

    def setWindowTitle(self, title: str = ""):
        """Sets window title

        Args:
            title (str, optional): Window title. Defaults to "".
        """
        super().setWindowTitle(str(QApplication.instance().applicationName()) + " - " + title)


    def closeEvent(self, event):
        """Stopping background tasks before closing this window to avoid crashes

        Args:
            event: Closing event
        """
        if self.worker.isRunning() and not self.__closing:
            self.__closing = True
            event.ignore()
            self.status.lock()
            self.worker.cancel = True
            self.setEnabled(False)
            self.worker.finished.connect(self.close)