from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt



class ColoredWidget():
    """Special methods for styling QWidget objects
    """


    def setBackground(self, value: str = None):
        """Changes this widget's background color

        Args:
            value (str, optional): Background color value, defined in stylesheets. Defaults to None.
        """
        self.setProperty("background", value)
        self.__updateStyle()
        

    def setColor(self, value: str = None):
        """Changes this widget's text color

        Args:
            color (str, optional): Text color value, defined in stylesheets. Defaults to None.
        """
        self.setProperty("color", value)
        self.__updateStyle()
    

    def __updateStyle(self):
        """Forces this widget to update its CSS styles
        """
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()





class ColoredButton(QPushButton, ColoredWidget):
    """Simply stylable button
    """


    def __init__(self, parent: QWidget, text: str = None, background: str = "grey", enabled: bool = True):
        """Initializes a button

        Args:
            parent (QWidget): Parent of this widget
            text (str, optional): Text content of this widget. Defaults to None.
            background (str, optional): Background color value, defined in stylesheets. Defaults to "grey".
            enabled (bool, optional): Is button enabled? Defaults to True.
        """
        super().__init__(text, parent)
        self.setBackground(background)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setEnabled(enabled)





class ColoredLabel(QLabel, ColoredWidget):
    """Simply stylable label
    """


    def __init__(self, parent: QWidget, text: str = None, background: str = None, color: str = None):
        """Initializes a label

        Args:
            parent (QWidget): Parent of this widget
            text (str, optional): Text content of this widget. Defaults to None.
            background (str, optional): Background color value, defined in stylesheets. Defaults to None.
            color (str, optional): Text color value, defined in stylesheets. Defaults to None.
        """
        super().__init__(text, parent)
        self.setBackground(background)
        self.setColor(color)