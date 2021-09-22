#!/usr/bin/env python3
from WindowWithStatus import *
from OverviewWorker import *
from AddPlayer import *


class Overview(WindowWithStatus):
    """ Class for creating a window that contains a table with currently tracked players """

    players = [] # List of players


    def __init__(self):
        super().__init__()
        """ Initialising GUI and a worker thread """
        self._set_window_properties()
        self._create_window_layout()
        self.show()
        # Worker threads
        self._loader = OverviewLoader(self)
        self._updater = OverviewUpdater(self)
        self._loader.start()
        self._loader.finished.connect(self._update_player_data)
        self.update_refreshbutton_visuals(False)
    

    def _set_window_properties(self):
        """ Setting winow properties """
        # Setting window title and size
        self.setWindowTitle("XonStat player tracker - Overview")
        self.resize(1300, 800)
        self._center_window()
    

    def _create_window_layout(self):
        """ Creates widnow layout with widgets """
        # Creating the layout itself
        window_widget = QWidget()
        window_layout = QVBoxLayout()
        window_widget.setLayout(window_layout)
        self.setCentralWidget(window_widget)
        # Adding widgets to layout
        window_layout.addLayout(self._create_top_widgets())
        window_layout.addWidget(self._create_player_table())
        window_layout.addWidget(self._status_create())
    

    def _create_top_widgets(self):
        """ Creates a box layout with search bar and a few buttons """
        layout = QHBoxLayout()
        # Creating search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search by player ID, nickname or current player name")
        self.search_bar.textChanged.connect(self._search)
        layout.addWidget(self.search_bar)
        # Creating button for refreshing table
        self.refresh_button = QPushButton(self)
        self.refresh_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_button.clicked.connect(self._update_player_data)
        self.refresh_button.setEnabled(False)
        layout.addWidget(self.refresh_button)
        # Creating button for adding new player
        self.add_button = QPushButton(self)
        self.add_button.setText("Add new player")
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.clicked.connect(self._open_addplayer_window)
        self.add_button.setProperty("background", "green")
        self.add_button.setEnabled(False)
        layout.addWidget(self.add_button)
        #return search
        return layout
    

    def _update_player_data(self):
        """ Attempts to update player variables """
        self.refresh_button.setEnabled(True)
        if self._updater.isRunning():
            self._updater.cancel = True
            self.refresh_button.setEnabled(False)
        else:
            self._updater.start()
        self.update_refreshbutton_visuals(self._updater.isRunning())
    

    def update_refreshbutton_visuals(self, running: bool):
        """ Updates visuals of "Refresh" button """
        if running:
            self.refresh_button.setText("Stop updating table")
            self.refresh_button.setProperty("background", "orange")
        else:
            self.refresh_button.setText("Refresh table")
            self.refresh_button.setProperty("background", "yellow")
        self.force_style_update(self.refresh_button)


    def _open_addplayer_window(self):
        """ Opening a window for adding a new player """
        self.add_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self._addplayer_window = AddPlayer(self)
    

    def addplayer_window_closed(self):
        """ Opening a window for adding a new player """
        self.add_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
    

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
    

    def change_row_color(self, row: int, color: str):
        """ Changes """
        for column in range(self.player_table.columnCount()):
            widget = self.player_table.cellWidget(row, column)
            if not widget == None and type(widget) == QLabel:
                widget.setProperty("background", color)
                self.force_style_update(widget)


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
        row = self.player_table.rowCount()
        self.player_table.insertRow(row)
        # Adding labels
        for i in range(4):
            widget = QLabel(self.player_table)
            self.player_table.setCellWidget(row, i, widget)
        # Adding label text
        self.player_table.cellWidget(row, 0).setText(str(player["id"]))
        self.player_table.cellWidget(row, 1).setText(player["nick"])
        # Adding buttons
        for i in range(4, 7):
            widget = QPushButton(self.player_table)
            widget.setCursor(QCursor(Qt.PointingHandCursor))
            self.player_table.setCellWidget(row, i, widget)
        # Adding button settings
        self.player_table.cellWidget(row, 4).setText("Show player profile")
        self.player_table.cellWidget(row, 4).setProperty("background", "blue")
        self.player_table.cellWidget(row, 4).clicked.connect(player.show_profile)
        self.player_table.cellWidget(row, 5).setText("Show more info")
        self.player_table.cellWidget(row, 5).setProperty("background", "yellow")
        self.player_table.cellWidget(row, 6).setText("Delete this player")
        self.player_table.cellWidget(row, 6).setProperty("background", "red")
        if not self._loader.isFinished():
            self.player_table.cellWidget(row, 6).setEnabled(False)
        # Forcing button style update
        for i in range(4, 7):
            self.force_style_update(self.player_table.cellWidget(row, i))

    
    def update_player_variables(self, player: Player):
        """ Print out player variables into table """
        # Adding label for current player name
        widget = self.player_table.cellWidget(self.get_row(player), 2)
        if not player.error == None:
            widget.setText(player.error)
            widget.setAlignment(Qt.AlignCenter)
            widget.setProperty("type", "error")
        else:
            widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            widget.setText(player.name)
            widget.setProperty("type", None)
        self.force_style_update(widget)
        # Adding label for the last time this player was active
        widget = self.player_table.cellWidget(self.get_row(player), 3)
        if not player.error == None:
            widget.setText(None)
            widget.setProperty("color", None)
        else:
            widget.setText(player.active)
            widget.setProperty("color", player.get_active_color())
        self.force_style_update(widget)
    

    def set_button_enabled(self, column: int, enabled: bool):
        """ Sets "enabled" property to a specified value for each button in the column """
        for i in range(self.player_table.rowCount()):
            widget = self.player_table.cellWidget(i, column)
            if not widget == None and type(widget) == QPushButton:
                widget.setEnabled(enabled)
    
    
    def get_row(self, player: Player):
        """ Returns row index """
        for row in range(self.player_table.rowCount()):
            widget = self.player_table.cellWidget(row, 0)
            if not widget == None:
                if widget.text() == str(player["id"]):
                    return row
        return -1
    

    def keyPressEvent(self, event):
        """ Reacts to pressing keys """
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.search_bar.setFocus()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker')
    overview = Overview()
    sys.exit(app.exec_())