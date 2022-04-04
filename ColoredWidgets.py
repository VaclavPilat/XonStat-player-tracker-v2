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



class BrowserButton(ColoredButton):
    """Browser button
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for opening links in a web browser

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "msc.browser", "blue")
        self.setToolTip("Open in browser")



class WindowButton(ColoredButton):
    """Window button
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for viewing more information in a new window

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "msc.graph", "yellow")
        self.setToolTip("More information")



class CopyButton(ColoredButton):
    """Copy button
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for copying information into clipboard

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.copy", "grey")
        self.setToolTip("Copy information")



class AddButton(ColoredButton):
    """Button for adding players
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for adding new players into a list with the tracked ones

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.user-plus", "green")
        self.setToolTip("Add player")



class DeleteButton(ColoredButton):
    """Button for deleting players
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for deleting players from list of tracked ones

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa5s.trash-alt", "red")
        self.setToolTip("Delete player")



class EditButton(ColoredButton):
    """Button for editing information
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for editing information about tracked players

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa5s.pencil-alt", "orange")
        self.setToolTip("Edit information")



class SaveButton(ColoredButton):
    """Button for saving information
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for saving edited player information

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.save", "green")
        self.setToolTip("Save information")



class CloseButton(ColoredButton):
    """Button for closing the current window
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for closing the current window

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "msc.chrome-close", "red")
        self.setToolTip("Close window")



class GameButton(ColoredButton):
    """Button for opening a GameInfo window
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for opening a GameInfo window

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.users", "yellow")
        self.setToolTip("Game information")



class LoadButton(ColoredButton):
    """Button for loading content
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for loading new content

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "mdi6.reload", "yellow")
        self.setToolTip("Load information")



class StopButton(ColoredButton):
    """Button for stopping content loading
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for stopping content loading

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "msc.chrome-close", "orange")
        self.setToolTip("Stop loading")