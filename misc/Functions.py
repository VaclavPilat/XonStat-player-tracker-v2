from PyQt5 import QtGui
import re, colorsys
from xml.sax.saxutils import escape

from misc.Config import *
    

def processColor(color: str):
    """Processes color from player nickname and returns it
    Making darker colors less dark (like on XonStat webpage)

    Args:
        color (str): Hexadecimal 3-digit RGB color
    
    Returns:
        [str]: Processed decimal RGB color
    """
    h, l, s = colorsys.rgb_to_hls(int(color[0]*2, 16) / 255, int(color[1]*2, 16) / 255, int(color[2]*2, 16) / 255)
    if l < 0.5:
        l = 0.5
    if l > 1:
        l = 1
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "rgb(" + str(r * 255) + "," + str(g * 255) + "," + str(b * 255) + ")"


def processNick(name: str):
    """Processes nickname from xonotic syntax to HTML

    Args:
        name (str): Raw nickname loaded from XonStat
    """
    name = escape(name)
    for colorCode in re.finditer(r"(\^x*[0-9a-fA-F]{3})", name):
        name = name.replace(colorCode.group(), '<span style="color:' + processColor( colorCode.group()[2:] ) + '">')
    # Replacing special characters
    for character, replacement in Config.instance()["Characters"].items():
        name = name.replace(character, replacement)
    return name


htmlParser = QtGui.QTextDocument() # TextDocument class for parsing text from HTML
def parseTextFromHTML(text: str) -> str:
    """Returns lowercase text without HTML tags

    Args:
        text (str): Text with HTML tags

    Returns:
        str: Lowercase text without HTML tags
    """
    htmlParser.setHtml(text)
    return htmlParser.toPlainText().lower()