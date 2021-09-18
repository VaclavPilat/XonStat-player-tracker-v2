#!/usr/bin/env python3
from PyQt5.QtWidgets import * 
from WindowWithStatus import *
from OverviewWorker import *
import webbrowser

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
        self.resize(1300, 800)
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
        self.window_layout.addLayout(self._create_top_widgets())
        self.window_layout.addWidget(self._create_player_table())
        self.window_layout.addWidget(self._status_create())
    

    def _create_top_widgets(self):
        """ Creates a box layout with search bar and a few buttons """
        layout = QHBoxLayout()
        # Creating search bar
        widget = QLineEdit(self)
        widget.setPlaceholderText("Search by player ID, nickname or current player name")
        widget.textChanged.connect(self._search)
        layout.addWidget(widget)
        # Creating button for refreshing table
        widget = QPushButton(self)
        widget.setText("Refresh table")
        widget.setProperty("class", "bg-yellow")
        layout.addWidget(widget)
        # Creating button for adding new player
        widget = QPushButton(self)
        widget.setText("Add new player")
        widget.setProperty("class", "bg-green")
        layout.addWidget(widget)
        #return search
        return layout
    

    def _search(self, text: str):
        """ Hiding and showing rows in the table based on input """
        for row in range(self.player_table.rowCount()):
            contains_text = False
            for column in range(self.player_table.columnCount()):
                widget = self.player_table.cellWidget(row, column)
                if not widget == None and type(widget) == QLabel:
                    if text.lower() in widget.text().lower():
                        contains_text = True
                        break
            self.player_table.setRowHidden(row, not contains_text)


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
        for i in range(1, 3):
            self.player_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        for i in range(3, 7):
            self.player_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        return self.player_table

    
    def add_player_to_table(self, player: Player):
        """ Adds a single row with player data to table """
        # Creating a new row inside the table
        row_index = self.player_table.rowCount()
        player.row = row_index
        self.player_table.insertRow(row_index)
        # Adding player ID label
        widget = QLabel(self.player_table)
        widget.setText(str(player["id"]))
        self.player_table.setCellWidget(row_index, 0, widget)
        # Adding player nickname label
        widget = QLabel(self.player_table)
        widget.setText(player["nick"])
        self.player_table.setCellWidget(row_index, 1, widget)
        # Adding button for showing player profile
        widget = QPushButton(self.player_table)
        widget.setText("Show player profile")
        widget.setProperty("class", "bg-blue")
        widget.clicked.connect(lambda: self._show_profile(player["profile"]))
        self.player_table.setCellWidget(row_index, 4, widget)
        # Adding button for showing more info about the player
        widget = QPushButton(self.player_table)
        widget.setText("Show more info")
        widget.setProperty("class", "bg-yellow")
        self.player_table.setCellWidget(row_index, 5, widget)
        # Adding button for deleting the player
        widget = QPushButton(self.player_table)
        widget.setText("Delete this player")
        widget.setProperty("class", "bg-red")
        self.player_table.setCellWidget(row_index, 6, widget)
    

    def _show_profile(self, url: str):
        """ Opening player profile in a new tab of a browser """
        webbrowser.open(url, new=2)

    
    def update_player_variables(self, player: Player):
        """ Print out player variables into table """
        # Adding label for current player name
        widget = QLabel(self.player_table)
        if player["name"] == None:
            widget.setText("---")
            widget.setAlignment(Qt.AlignCenter)
        else:
            widget.setText(player["name"])
        self.player_table.setCellWidget(player.row, 2, widget)
        # Adding label for the last time this player was active
        widget = QLabel(self.player_table)
        if player["active"] == None:
            widget.setText("---")
            widget.setAlignment(Qt.AlignCenter)
        else:
            widget.setText(player["active"])
            widget.setProperty("class", player.get_active_color())
        self.player_table.setCellWidget(player.row, 3, widget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    overview = Overview()
    sys.exit(app.exec_())