from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt



class ColoredWidget(QWidget):
    """Special methods for styling QWidget objects
    """
    

    def setProperty(self, prop: str, value: str = None):
        """Overriding setProperty function for updating styles after each change

        Args:
            prop (str): Property name
            value (str, optional): Property value. Defaults to None.
        """
        super().setProperty(prop, value)
        self.__updateStyle()


    def setBackground(self, value: str = None):
        """Changes this widget's background color

        Args:
            value (str, optional): Background color value, defined in stylesheets. Defaults to None.
        """
        self.setProperty("background", value)
        

    def setColor(self, value: str = None):
        """Changes this widget's text color

        Args:
            color (str, optional): Text color value, defined in stylesheets. Defaults to None.
        """
        self.setProperty("color", value)
    

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





class ColoredTable(QTableWidget):
    """Creates a simple table with functions to easily change appearance
    """


    def __init__(self, parent):
        """Initializes a table
        """
        super().__init__(parent)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.horizontalHeader().setMinimumSectionSize(150)

    
    def setRowColor(self, row: int, background: str = None):
        """Changes background color of all labels in a selected row

        Args:
            row (int): Row index
            background (str, optional): Background color value defined in stylesheets. Defaults to None.
        """
        for column in range(self.columnCount()):
            widget = self.cellWidget(row, column)
            if not widget == None:
                if type(widget) == ColoredLabel:
                    widget.setBackground(background)
    

    def setButtonsEnabled(self, column: int, enabled: bool):
        """Sets "enabled" property to a specified value for each button in the column

        Args:
            column (int): Column index
            enabled (bool): Should the buttons be enabled?
        """
        for i in range(self.rowCount()):
            widget = self.cellWidget(i, column)
            if not widget == None and type(widget) == ColoredButton:
                widget.setEnabled(enabled)