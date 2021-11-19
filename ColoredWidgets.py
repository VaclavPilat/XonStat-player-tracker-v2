from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTableWidget
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt
import qtawesome as qta



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
        self.setAttribute(Qt.WA_StyledBackground, True)
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


    def __init__(self, parent: QWidget, content = None, background: str = "grey", enabled: bool = True):
        """Initializes a button

        Args:
            parent (QWidget): Parent of this widget
            text (str, optional): Text content of this widget. Defaults to None.
            background (str, optional): Background color value, defined in stylesheets. Defaults to "grey".
            icon (QIcon, optimal): Optional button icon
            enabled (bool, optional): Is button enabled? Defaults to True.
        """
        if content is None:
            content = ""
        if "." in content:
            super().__init__(None, parent)
            self.setIcon(content)
        else:
            super().__init__(content, parent)
        self.setBackground(background)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setEnabled(enabled)

    def setIcon(self, icon: str):
        """Sets button icon

        Args:
            icon (str): Icon name
        """
        super().setIcon(qta.icon(icon, color="#DDD"))





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
        self.horizontalHeader().setMinimumSectionSize(140)

    
    def setRowColor(self, row: int, background: str = None):
        """Changes background color of all labels in a selected row

        Args:
            row (int): Row index
            background (str, optional): Background color value defined in stylesheets. Defaults to None.
        """
        for column in range(self.columnCount()):
            self.setWidgetColor(row, column, background)
    

    def setWidgetColor(self, row: int, column: int, background: str = None):
        """Changes background color of a selected ColoredLabel in a table

        Args:
            row (int): Row index
            column (int): Column index
            background (str, optional): Background color value defined in stylesheets. Defaults to None.
        """
        widget = self.cellWidget(row, column)
        if not widget == None:
            if type(widget) is ColoredLabel or type(widget) is ColoredWidget:
                widget.setBackground(background)
    

    def setButtonsEnabled(self, name: str, enabled: bool):
        """Sets "enabled" property to all buttons with specified object name

        Args:
            name (str): Object name
            enabled (bool): Should the buttons be enabled?
        """
        for button in self.findChildren(ColoredButton, name):
            button.setEnabled(enabled)
    

    def setCellWidget(self, row: int, column: int, widget: QWidget, rowSpan: int = None, columnSpan: int = None):
        """Overriding setCellWidget method for setting widget position and span at the same time

        Args:
            row (int): Row index
            column (int): Column index
            widget (QWidget): Widget
            rowSpan (int, optional): Row span. Defaults to None.
            columnSpan (int, optional): Column span. Defaults to None.
        """
        super().setCellWidget(row, column, widget)
        # Sets widget span if arguments are not empty
        if rowSpan is not None and columnSpan is not None:
            super().setSpan(row, column, rowSpan, columnSpan)