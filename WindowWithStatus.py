#!/usr/bin/env python3
from PyQt5.QtCore import (
    Qt, pyqtSignal
)
from PyQt5.QtGui import (
    QIcon, QCursor
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QTableWidget, QHeaderView, QMainWindow
)
import os, qdarkstyle, math


class WindowWithStatus(QMainWindow):
    """ Class for creating a status label and methods for controlling status content """

    def __init__(self):
        super().__init__()
        self._add_window_icon()
        self._add_stylesheet()
    

    def _center_window(self):
        """ Moving window to the center of the screen """
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())

    
    def force_style_update(self, widget: QWidget):
        """ Forcing a widget to update its styles """
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()


    def _add_window_icon(self):
        """ Add icon to this window """
        self.setWindowIcon(QIcon( os.path.join(os.path.dirname(__file__), "Icon.png") ))
    

    def _add_stylesheet(self):
        """ Adding CSS styling """
        # Adding CSS stylesheet from QDarkStyle
        stylesheet = qdarkstyle.load_stylesheet()
        # Adding my own stylesheet
        with open(os.path.join(os.path.dirname(__file__), "Style.css"), "r") as css_file:
            css_content = css_file.read()
            if not css_content == None and not css_content == "":
                stylesheet += css_content
        # Applying stylesheet
        self.setStyleSheet(stylesheet)


    def _status_create(self) -> QLabel:
        """ Creates a status label """
        # Creating label
        self.status = QLabel(self)
        self.status.setAlignment(Qt.AlignCenter)
        self._status_change_text("Ready")
        self.status.setProperty("background", "grey")
        self.status.setObjectName("status")
        return self.status


    def _status_change_color (self, color: str):
        """ Changing status background color by changing its class property """
        self.status.setProperty("background", color)
        self.force_style_update(self.status)


    def _status_change_text (self, text: str):
        """ Changing status label text """
        self.status.setText(text)
    

    def status_change_message (self, message: str):
        """ Changing status message """
        message += " ..."
        self._status_message = message
        self._status_change_text(message)
        self._status_change_color("yellow")
    

    def status_update_progress (self, current: int, max: int, result: bool = False):
        """ Printing out progress with the current status message """
        output = self._status_message + " "
        if current > 0:
            output += str(math.ceil(current / max * 100))
        else:
            output += "0"
        output += "% "
        if result:
            output += "correct"
        else:
            output += "done"
        output += " (" + str(current) + " out of " + str(max) + ")"
        self._status_change_text(output)
    

    def status_result_progress (self, message: str, correct: int, max: int):
        """ Printing result message and progress """
        self.status_change_message(message)
        self.status_update_progress(correct, max, True)
        if correct == max:
            self._status_change_color("green")
        elif correct > 0:
            self._status_change_color("orange")
        else:
            self._status_change_color("red")
    

    def status_result_message (self, message: str, correct: bool = True):
        """ Printing result message and progress """
        self.status_change_message(message)
        if correct:
            self._status_change_color("green")
        else:
            self._status_change_color("red")