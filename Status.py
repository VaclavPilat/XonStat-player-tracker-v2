from Window import *
from ColoredWidgets import *
import math
from PyQt5.QtWidgets import QApplication, QHBoxLayout



class Status(ColoredWidget):
    """Stylable status label
    """


    def __init__(self, parent: Window):
        """Creates a status label

        Args:
            parent (Window): Parent of this widget
        """
        super().__init__()
        self.__locked = False # Boolean for locking changes
        # Creating layout
        self.setObjectName("status")
        self.setBackground("grey")
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # Creating label for displaying an icon
        self.icon = ColoredLabel(self)
        self.icon.setObjectName("status-icon")
        self.icon.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.icon)
        # Creating inner status label
        self.inner = ColoredLabel(self, "Ready")
        self.inner.setObjectName("status-inner")
        self.inner.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.inner)
        # Creating label for ratelimit
        self.rate = ColoredLabel(self)
        self.rate.setObjectName("status-rate")
        self.rate.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.rate)
    

    def showRate(self, remaining: str, limit: str):
        """Shows x-ratelimit header

        Args:
            remaining (str): Remaining number of requests
            limit (str): Request limit
        """
        for widget in QApplication.topLevelWidgets():
            if issubclass(type(widget), Window) and widget.status:
                widget.status.rate.setText(remaining + " / " + limit)
    

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
                self.icon.setIcon("mdi6.dots-horizontal-circle-outline")
    

    def progress(self, current: int, maximum: int, finished: bool = False, changeIcon: bool = True):
        """Changing status progress. Used for displaying how much work is done in a task.

        Args:
            current (int): Current amount of parts completed in this task
            maximum (int): Maximum amount of parts that can be completed in this task
            finished (bool, optional): Is the task finished? Defaults to False.
            changeIcon (bool): Automatically update icon? Defaults to True.
        """
        if not self.__locked:
            output = self.__message + " "
            # Displaying percentage
            if current > 0:
                division = current / maximum
                output += str(math.ceil(division * 100))
                number = max(1, math.floor(division * 8))
                if changeIcon:
                    self.icon.setIcon("mdi6.circle-slice-" + str(number))
            else:
                output += "0"
                if changeIcon:
                    self.icon.setIcon("mdi6.circle-outline")
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
            self.message(message, False)
            # Changing the background color based on if the task is completed successfully
            if correct:
                self.setBackground("green")
                self.icon.setIcon("mdi6.check-circle-outline")
            else:
                self.setBackground("red")
                self.icon.setIcon("mdi6.alert-circle-outline")
    

    def resultProgress(self, message: str, correct: int, max: int):
        """Changing status message and background color based on the amount of successfully completed parts

        Args:
            message (str): Text that will be displayed on the status
            correct (int): Amount of successfully completed parts of this task
            max (int): Maximum amount of parts that can be completed
        """
        if not self.__locked:
            self.message(message, False)
            self.progress(correct, max, True, False)
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