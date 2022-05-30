from PyQt5 import QtWidgets, QtCore, QtGui
import traceback
from colour import Color

from misc.Config import *
from widgets.ColoredWidgets import *



def printException():
    """Prints caught exception traceback
    """
    print("\n--------------- CAUGHT EXCEPTION ---------------\n" 
        + traceback.format_exc() + "------------------------------------------------\n")


def getColorStyles():
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
    return style


def executeCallbackOnButtons(name: str, callback):
    """Executes callback on all buttons with a selected object name

    Args:
        name (str): Button object name
        callback (function): Callback function on button
    """
    for window in QtWidgets.QApplication.topLevelWidgets():
        for button in window.findChildren(QtWidgets.QStackedWidget, name):
            callback(button)


def setButtonsEnabled(name: str, enabled: bool):
    """Sets "enabled" property of all buttons that match the selected object name

    Args:
        name (str): Button object name
        enabled (bool): "Enabled" property value
    """
    executeCallbackOnButtons(name, lambda button: button.setEnabled(enabled))