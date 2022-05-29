from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta



class ColoredWidget(QtWidgets.QWidget):
    """Special methods for styling QWidget objects
    """


    def __init__(self):
        """Init for ColoredWiget class
        """
        QtWidgets.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
    

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



class ColoredButton(QtWidgets.QPushButton, ColoredWidget):
    """Simply stylable button
    """


    def __init__(self, parent: QtWidgets.QWidget, content = None, background: str = "grey", enabled: bool = True):
        """Initializes a colored button

        Args:
            parent (QtWidgets.QWidget): Parent widget
            content (str, optional): Icon name or button text content. Defaults to None.
            background (str, optional): Background color defined in generated stylesheets. Defaults to "grey".
            enabled (bool, optional): Should the button be enabled?. Defaults to True.
        """
        if content is None:
            content = ""
        if "." in content:
            QtWidgets.QPushButton.__init__(self, None, parent)
            self.setIcon(content)
        else:
            QtWidgets.QPushButton.__init__(self, content, parent)
        self.setBackground(background)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setEnabled(enabled)


    def setIcon(self, icon: str):
        """Sets button icon

        Args:
            icon (str): QTAwesome icon name
        """
        super().setIcon(qta.icon(icon, color="#DDD"))



class ColoredLabel(QtWidgets.QLabel, ColoredWidget):
    """Simply stylable label
    """


    def __init__(self, parent: QtWidgets.QWidget, text: str = None, background: str = None, color: str = None):
        """Initializes a label

        Args:
            parent (QtWidgets.QWidget): Parent of this widget
            text (str, optional): Text content of this widget. Defaults to None.
            background (str, optional): Background color value, defined in stylesheets. Defaults to None.
            color (str, optional): Text color value, defined in stylesheets. Defaults to None.
        """
        QtWidgets.QLabel.__init__(self, text, parent)
        self.setBackground(background)
        self.setColor(color)
    

    def setIcon(self, icon: str):
        """Sets label icon

        Args:
            icon (str): QTAwesome icon name
        """
        self.setPixmap(qta.icon(icon, color="#DDD").pixmap(QtCore.QSize(20, 20)))



class ColoredTable(QtWidgets.QTableWidget, ColoredWidget):
    """Creates a simple table with functions to easily change appearance
    """


    def __init__(self, parent):
        """Initializes a table
        """
        QtWidgets.QTableWidget.__init__(self, parent)
        self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.horizontalHeader().setMinimumSectionSize(140)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    
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
            if type(widget) is ColoredWidget or ColoredWidget in type(widget).__bases__:
                widget.setBackground(background)
    

    def setCellWidget(self, row: int, column: int, widget: QtWidgets.QWidget, rowSpan: int = None, columnSpan: int = None):
        """Overriding setCellWidget method for setting widget position and span at the same time

        Args:
            row (int): Row index
            column (int): Column index
            widget (QtWidgets.QWidget): Widget
            rowSpan (int, optional): Row span. Defaults to None.
            columnSpan (int, optional): Column span. Defaults to None.
        """
        super().setCellWidget(row, column, widget)
        # Sets widget span if arguments are not empty
        if rowSpan is not None and columnSpan is not None:
            super().setSpan(row, column, rowSpan, columnSpan)



class ColoredTextarea(QtWidgets.QTextEdit, ColoredWidget):
    """Creates a simple text edit with easily modifiable appearance
    """


    def __init__(self, parent):
        """Initializes a text edit widgets
        """
        QtWidgets.QTextEdit.__init__(self, parent)



class ColoredToolButton(QtWidgets.QToolButton, ColoredWidget):
    """Creates a class for a colored ToolButton
    """


    def __init__(self, parent, color: str = None):
        """Initializes a text edit widgets
        """
        QtWidgets.QToolButton.__init__(self, parent)
        self.setIconSize(QtCore.QSize(50, 50))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setBackground(color)