import traceback
from Config import *
from colour import Color



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
        style += '[background="light-' + name + '"],ColoredButton[background="' + name + '"]:hover{background-color:' + colors["light"] + '}'
        style += '[background="dark-' + name + '"],ColoredButton[background="' + name + '"]:disabled{background-color:' + colors["dark"] + '}'
        style += 'ColoredButton[background="' + name + '"]:disabled{border-color:' + colors["normal"] + '}'
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