from PyQt5 import QtWidgets, QtCore
import math
import qtawesome as qta

from windows.Window import *
from widgets.ColoredWidgets import *



class Status(ColoredWidget):
    """Stylable status label
    """


    def __init__(self, parent: Window):
        """Creates a status label

        Args:
            parent (Window): Parent of this widget
        """
        self.parent = parent
        super().__init__()
        self.__locked = False # Boolean for locking changes
        # Creating layout
        self.setObjectName("status")
        self.setBackground("grey")
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # Creating label for displaying an icon
        self.icon = ColoredLabel(self)
        self.icon.setObjectName("status-icon")
        self.icon.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.icon)
        # Creating inner status label
        self.inner = ColoredLabel(self, "Ready")
        self.inner.setObjectName("status-inner")
        self.inner.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.inner)
        # Creating label for ratelimit
        self.rate = ColoredLabel(self)
        self.rate.setObjectName("status-rate")
        self.rate.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.rate)
        self.setMaximumHeight(30)
    

    def setIcon(self, icon: str):
        """Set status and tab icon

        Args:
            icon (str): QTAwesome icon name
        """
        self.icon.setIcon(icon)
        self.parent.parent.tabWidget.setTabIcon( self.parent.parent.tabWidget.indexOf(self.parent), qta.icon(icon, color="#FFFFFF") )
    

    def showRate(self, remaining: str, limit: str):
        """Shows x-ratelimit header

        Args:
            remaining (str): Remaining number of requests
            limit (str): Request limit
        """
        for i in range(self.parent.parent.tabWidget.count()):
            self.parent.parent.tabWidget.widget(i).status.rate.setText(remaining + " / " + limit)
    

    def message(self, message: str, changeIcon: bool = True):
        """Changing status message and setting background color to yellow. Used for starting a new task

        Args:
            message (str): Text that will be displayed in the status.
            color (str): New background color status
            changeIcon (bool): Automatically update icon? Defaults to True.
        """
        if not self.__locked:
            message += " ..."
            self.__message = message
            self.inner.setText(message)
            self.setBackground("yellow")
            if changeIcon:
                self.setIcon("mdi6.dots-horizontal-circle-outline")
    

    def progress(self, current: int, maximum: int, finished: bool = False, changeIcon: bool = True):
        """Changing status progress. Used for displaying how much work is done in a task.

        Args:
            current (int): Current amount of parts completed in this task
            maximum (int): Maximum amount of parts that can be completed in this task
            finished (bool, optional): Is the task finished? Defaults to False.
            changeIcon (bool): Automatically update icon? Defaults to True.
        """
        if not self.__locked:
            if not self.property("background") == "yellow":
                self.setBackground("yellow")
            output = self.__message + " "
            # Displaying percentage
            if current > 0:
                division = current / maximum
                output += str(math.ceil(division * 100))
                number = max(1, math.floor(division * 8))
                if changeIcon:
                    self.setIcon("mdi6.circle-slice-" + str(number))
            elif maximum == 0:
                output += "100"
                if changeIcon:
                    self.setIcon("mdi6.circle-slice-8")
            else:
                output += "0"
                if changeIcon:
                    self.setIcon("mdi6.circle-outline")
            output += "% "
            # Varying status message based on if the task is finished
            if finished:
                output += "correct"
            else:
                output += "done"
            # Displaying amount of parts finished
            output += " (" + str(current) + " out of " + str(maximum) + ")"
            self.inner.setText(output)
    

    def resultMessage(self, message: str, correct: bool = True):
        """Changing status message and changing status color based on the if the task is completed successfully.

        Args:
            message (str): Text that will be displayed on the status
            correct (bool, optional): Is the task completed successfully? Defaults to True.
        """
        if not self.__locked:
            self.inner.setText(message + " ...")
            # Changing the background color based on if the task is completed successfully
            if correct:
                self.setBackground("green")
                self.setIcon("mdi6.check-circle-outline")
            else:
                self.setBackground("red")
                self.setIcon("mdi6.alert-circle-outline")
    

    def resultProgress(self, message: str, correct: int, max: int):
        """Changing status message and background color based on the amount of successfully completed parts

        Args:
            message (str): Text that will be displayed on the status
            correct (int): Amount of successfully completed parts of this task
            max (int): Maximum amount of parts that can be completed
        """
        if not self.__locked:
            self.__message = message + " ..."
            self.progress(correct, max, True)
            # Changing the background color based on if the task is completed successfully
            if correct == max:
                self.setBackground("green")
            elif correct > 0:
                self.setBackground("orange")
            else:
                self.setBackground("red")
    

    def lock(self):
        """Locking status from further changes
        """
        if not self.__locked:
            self.message("Waiting for background task to finish")
            self.setBackground("blue")
            self.__locked = True