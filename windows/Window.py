from PyQt5 import QtWidgets, QtCore, QtGui
import os, qdarkstyle
from colour import Color

from widgets.ColoredWidgets import *
from misc.Config import *


class Window(QtWidgets.QMainWindow):
    """Class for creating a status label and methods for controlling status content
    """


    def __init__(self):
        """Initializes window, adds stylesheet, sets properties using methods implemented by derived classes.
        """
        self.closing = False
        self.worker = None
        self.status = None
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.__addStylesheet()
        self.__addIcon()
        self.setProperties()
        self.createLayout()
        self.show()
        self.__centerWindow()


    def getColorStyles(self):
        """Generates stylesheet for each color in Colors.json file

        Returns:
            str: Generated stylesheet
        """
        style = ""
        # Generating button and label background and border colors
        for name, colors in Config.instance()["Colors"]["presets"].items():
            style += '[background="' + name + '"]{background-color:' + colors["normal"] + ';border-color:' + colors["light"] + '}'
            style += '[background="light-' + name + '"],ColoredButton[background="' + name + '"]:hover,ColoredToolButton[background="' + name + '"]:hover{background-color:' + colors["light"] + '}'
            style += '[background="dark-' + name + '"],ColoredButton[background="' + name + '"]:disabled,ColoredToolButton[background="' + name + '"]:disabled{background-color:' + colors["dark"] + '}'
            style += 'ColoredButton[background="' + name + '"]:disabled,ColoredToolButton[background="' + name + '"]:disabled{border-color:' + colors["normal"] + '}'
        if "grey" in Config.instance()["Colors"]["presets"]:
            style += 'QTabBar::tab:!selected{background-color:' + Config.instance()["Colors"]["presets"]["grey"]["normal"] + '}'
        if "blue" in Config.instance()["Colors"]["presets"]:
            style += 'QTabBar::tab:top:selected{background-color:' + Config.instance()["Colors"]["presets"]["blue"]["light"] + '}'
            style += 'QLineEdit:!disabled{background-color:' + Config.instance()["Colors"]["presets"]["blue"]["dark"] + ';border-color:' + Config.instance()["Colors"]["presets"]["blue"]["normal"] + '}'
            style += 'QLineEdit:!disabled:focus{background-color:' + Config.instance()["Colors"]["presets"]["blue"]["normal"] + ';border-color:' + Config.instance()["Colors"]["presets"]["blue"]["light"] + '}'
        if "yellow" in Config.instance()["Colors"]["presets"]:
            style += 'QTabBar QToolButton:disabled,QTabBar QToolButton:disabled:hover{background-color:' + Config.instance()["Colors"]["presets"]["yellow"]["dark"] + ';border:1px solid ' + Config.instance()["Colors"]["presets"]["yellow"]["normal"] + '}'
            style += 'QTabBar QToolButton{background-color:' + Config.instance()["Colors"]["presets"]["yellow"]["normal"] + ';border:1px solid ' + Config.instance()["Colors"]["presets"]["yellow"]["light"] + '}'
            style += 'QTabBar QToolButton:hover{background-color:' + Config.instance()["Colors"]["presets"]["yellow"]["light"] + '}'
        # Generating colors for heatmap
        minimum = Color( Config.instance()["Colors"]["heatmap"]["min"] )
        maximum = Color( Config.instance()["Colors"]["heatmap"]["max"] )
        count = Config.instance()["Colors"]["heatmap"]["count"]
        i = 0
        for color in list(minimum.range_to(maximum, count + 1)):
            style += '[background="heatmap-' + str(i) + '"]{background-color:' + str(color) + '}'
            i += 1
        # Generating colors for activity labels
        i = 1
        for color in Config.instance()["Colors"]["activity"]:
            style += '[color="active-' + str(i) + '"]{color:' + str(color) + '}'
            i += 1
        # Generating colors for age labels
        i = 1
        for color in Config.instance()["Colors"]["age"]:
            style += '[color="age-' + str(i) + '"]{color:' + str(color) + '}'
            i += 1
        return style
    

    def __addStylesheet(self):
        """Adding CSS styling (my own + the one from "qdarkstyle" module)
        """
        # Adding CSS stylesheet from QDarkStyle
        stylesheet = qdarkstyle.load_stylesheet()
        # Adding my own stylesheet
        folder = os.path.join(os.path.dirname(__file__), "../css/")
        for filename in os.listdir(folder):
            filepath = folder + filename
            f = open(filepath, "r", encoding="utf8")
            stylesheet += f.read()
        # Adding generated color styles
        stylesheet += self.getColorStyles()
        # Applying stylesheet
        self.setStyleSheet(stylesheet)
    

    def __addIcon(self):
        """Adds an icon to this window
        """
        self.setWindowIcon(QtGui.QIcon( os.path.join(os.path.dirname(__file__), "Icon.png") )) # Adding icon
    

    def __centerWindow(self):
        """Moving window to the center of the screen
        """
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())
    

    def setWindowTitle(self, title: str = ""):
        """Sets window title

        Args:
            title (str, optional): Window title. Defaults to "".
        """
        if title != "":
            super().setWindowTitle(str(QtWidgets.QApplication.instance().applicationName()) + " - " + title)
        else:
            super().setWindowTitle(str(QtWidgets.QApplication.instance().applicationName()))


    def closeEvent(self, event, isChildWindow = True):
        """Stopping background tasks before closing this window to avoid crashes

        Args:
            event: Closing event
            isChildWindow (bool): Has this window a parent window?
        """
        if self.worker is not None:
            if self.worker.isRunning() and not self.closing:
                self.closing = True
                event.ignore()
                self.status.lock()
                self.worker.cancel = True
                self.setEnabled(False)
                if isChildWindow:
                    self.worker.finished.connect(self.close)