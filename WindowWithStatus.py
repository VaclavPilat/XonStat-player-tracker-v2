#!/usr/bin/env python3
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 

class WindowWithStatus(QWidget):
    """ Class for creating a status label and methods for controlling status content """


    def _status_create(self) -> QLabel:
        """ Creates a status label """
        # Creating label
        self.status = QLabel("Ready", self)
        self.status.setAlignment(Qt.AlignCenter)
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


    def _status_change_text (self, text: str):
        """ Changing status label text """
        self.status.setText(text)