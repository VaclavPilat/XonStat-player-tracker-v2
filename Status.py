from Window import *
from ColoredWidgets import *
import math



class Status(ColoredLabel):
    """Stylable status label
    """


    def __init__(self, parent: Window):
        """Creates a status label

        Args:
            parent (Window): Parent of this widget
        """
        self.__locked = False # Boolean for locking changes
        super().__init__(parent, "Ready", "grey")
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("status")
    

    def message(self, message: str, color: str = "yellow"):
        """Changing status message and setting background color to yellow. Used for starting a new task

        Args:
            message (str): Text that will be displayed in the status.
            color (str): New background color status
        """
        if not self.__locked:
            message += " ..."
            self.__message = message
            self.setText(message)
            self.setBackground(color)
    

    def progress(self, current: int, max: int, finished: bool = False):
        """Changing status progress. Used for displaying how much work is done in a task.

        Args:
            current (int): Current amount of parts completed in this task
            max (int): Maximum amount of parts that can be completed in this task
            finished (bool, optional): Is the task finished? Defaults to False.
        """
        if not self.__locked:
            output = self.__message + " "
            # Displaying percentage
            if current > 0:
                output += str(math.ceil(current / max * 100))
            else:
                output += "0"
            output += "% "
            # Varying status message based on if the task is finished
            if finished:
                output += "correct"
            else:
                output += "done"
            # Displaying amount of parts finished
            output += " (" + str(current) + " out of " + str(max) + ")"
            self.setText(output)
    

    def resultMessage(self, message: str, correct: bool = True):
        """Changing status message and changing status color based on the if the task is completed successfully.

        Args:
            message (str): Text that will be displayed on the status
            correct (bool, optional): Is the task completed successfully? Defaults to True.
        """
        if not self.__locked:
            self.message(message)
            # Changing the background color based on if the task is completed successfully
            if correct:
                self.setBackground("green")
            else:
                self.setBackground("red")
    

    def resultProgress(self, message: str, correct: int, max: int):
        """Changing status message and background color based on the amount of successfully completed parts

        Args:
            message (str): Text that will be displayed on the status
            correct (int): Amount of successfully completed parts of this task
            max (int): Maximum amount of parts that can be completed
        """
        if not self.__locked:
            self.message(message)
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
            self.message("Waiting for background task to finish", "blue")
            self.__locked = True