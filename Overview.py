#!/usr/bin/env python3
from PyQt5.QtWidgets import * 
from WindowWithStatus import *
from OverviewWorker import *

class Overview(WindowWithStatus):
    """ Class for creating a window that contains a table with currently tracked players """


    def __init__(self):
        super().__init__()
        """ Initialising GUI and a worker thread """
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
        self.player_table.setObjectName("player_table")
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

    
    def add_player_to_table(self, player: Player):
        """ Adds a single row with player data to table """
        row_index = self.player_table.rowCount()
        self.player_table.insertRow(row_index)
        # Adding player ID label
        widget = QLabel(self.player_table)
        widget.setText(str(player["id"]))
        self.player_table.setCellWidget(row_index, 0, widget)
        # Adding player nickname label
        widget = QLabel(self.player_table)
        widget.setText(player["nick"])
        self.player_table.setCellWidget(row_index, 1, widget)
        # Adding player nickname label
        widget = QLabel(self.player_table)
        widget.setText(player["profile"])
        self.player_table.setCellWidget(row_index, 2, widget)
        # Adding button for showing player profile
        widget = QPushButton(self.player_table)
        widget.setText("Show player profile")
        widget.setProperty("class", "profile")
        self.player_table.setCellWidget(row_index, 4, widget)
        # Adding button for showing more info about the player
        widget = QPushButton(self.player_table)
        widget.setText("Show more info")
        widget.setProperty("class", "info")
        self.player_table.setCellWidget(row_index, 5, widget)
        # Adding button for deleting the player
        widget = QPushButton(self.player_table)
        widget.setText("Delete this player")
        widget.setProperty("class", "delete")
        self.player_table.setCellWidget(row_index, 6, widget)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    overview = Overview()
    sys.exit(app.exec_())