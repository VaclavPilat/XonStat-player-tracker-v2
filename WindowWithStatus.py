#!/usr/bin/env python3
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 

class WindowWithStatus(QWidget):
    """ Class for creating a status label and methods for controlling status content """
    

    _status_message = ""


    def _status_create(self) -> QLabel:
        """ Creates a status label """
        # Creating label
        self.status = QLabel(self)
        self.status.setAlignment(Qt.AlignCenter)
        self._status_change_text("Ready")
        self.status.setProperty("class", "ready")
        # Adding CSS
        self.status.setStyleSheet("""
            QLabel {
                padding: 5px;
                font-weight: bold;
            }
            .ready   { background-color: #bbbbbb }
            .working { background-color: #e9ea83 }
            .success { background-color: #a1ea83 }
            .error   { background-color: #ea9883 }
        """)
        return self.status


    def _status_change_color (self, color: str):
        """ Changing status background color by changing its class property """
        self.status.setProperty("class", color)
        # Forcing appearance update
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.status.update()


    def _status_change_text (self, text: str):
        """ Changing status label text """
        self.status.setText(text)
    

    def status_change_message (self, message: str):
        """ Changing status message """
        self._status_message = message
        self._status_change_text(message)
        self._status_change_color("working")
    

    def status_update_progress (self, current: int, max: int, change_color: bool = False):
        """ Printing out progress with the current status message """
        self._status_change_text(self._status_message + " (" + str(current) + " out of " + str(max) + ")")
        if change_color:
            self._status_change_color("working")
    

    def status_result_message (self, message: str, current: int, max: int):
        """ Printing result message and progress """
        self._status_change_text(message)
        self._status_update_progress(current, max)
        if current == max:
            self._status_change_color("correct")
        else:
            self._status_change_color("error")
    

    def status_result_message (self, message: str, correct: bool = True):
        """ Printing result message and progress """
        self._status_change_text(message)
        if correct:
            self._status_change_color("success")
        else:
            self._status_change_color("error")