#!/usr/bin/env python3
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from WindowWithStatus import *
from OverviewWorker import *

class Overview(WindowWithStatus):
    """ Class for creating a window that contains a table with currently tracked players """


    def __init__(self):
        super().__init__()
        self._set_window_properties()
        self._create_window_layout()
        self.show()
        # Starting a worker thread
        self.worker = OverviewWorker(self)
        self.worker.start()
    

    def _set_window_properties(self):
        """ Setting winow properties """
        # Setting window title and size
        self.setWindowTitle("XonStat player tracker - Overview")
        self.resize(1200, 800)
        # Moving window to the center of the screen
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())
    

    def _create_window_layout(self):
        """ Creates widnow layout with widgets """
        # Creating the layout itself
        self.window_layout = QVBoxLayout()
        self.setLayout(self.window_layout)
        # Adding widgets to layout
        self.window_layout.addWidget(self._create_player_table())
        self.window_layout.addWidget(self._status_create())


    def _create_player_table(self) -> QTableWidget:
        """ Creating table of players """
        self.player_table = QTableWidget()
        self.player_table.setEditTriggers( QTableWidget.NoEditTriggers )
        # Setting columns
        table_headers = ["ID", "Player nickname", "Current player name", "Last played", 
                        "Player profile", "More information", "Delete player"]
        self.player_table.setColumnCount( len(table_headers) )
        self.player_table.setHorizontalHeaderLabels(table_headers)
        # Setting column stretching
        self.player_table.horizontalHeader().setMinimumSectionSize(150)
        self.player_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.player_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.player_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.player_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.player_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.player_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.player_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        return self.player_table

    
    def add_player_to_table(self, player: dict):
        """ Adds a single row with player data to table """
        row_index = self.player_table.rowCount()
        self.player_table.insertRow(row_index)
        self.player_table.setItem(row_index, 0, QTableWidgetItem(str(player["id"])))
        self.player_table.setItem(row_index, 1, QTableWidgetItem(player["nick"]))
        # Adding button for showing player profile
        button = QPushButton(self.player_table)
        button.setText("Show player profile")
        self.player_table.setCellWidget(row_index, 4, button)
        # Adding button for showing more info about the player
        button = QPushButton(self.player_table)
        button.setText("Show more info")
        self.player_table.setCellWidget(row_index, 5, button)
        # Adding button for deleting the player
        button = QPushButton(self.player_table)
        button.setText("Delete this player")
        self.player_table.setCellWidget(row_index, 6, button)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    overview = Overview()
    sys.exit(app.exec_())