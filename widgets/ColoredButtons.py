from widgets.ColoredWidgets import *


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
        self.setToolTip("Refresh page")



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



class TabButton(ColoredButton):
    """Button for adding new tab
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for adding new tab

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "ei.plus", "green")
        self.setToolTip("Add new tab")



class AcceptButton(ColoredButton):
    """Button for accepting a dialog
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for accepting a dialog window

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.check", "green")
        self.setToolTip("Accept")



class RejectButton(ColoredButton):
    """Button for rejecting a dialog
    """


    def __init__(self, parent: QtWidgets.QWidget):
        """Creates a new button for rejecting a dialog window

        Args:
            parent (QtWidgets.QWidget): Parent element
        """
        ColoredButton.__init__(self, parent, "fa.times", "red")
        self.setToolTip("Reject")