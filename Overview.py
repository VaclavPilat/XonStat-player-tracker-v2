#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QHeaderView
from Window import *
from Status import *
from OverviewWorker import *
from AddPlayer import *
from ColoredWidgets import *


class Overview(Window):
    """ Class for creating a window that contains a table with currently tracked players """

    players = [] # List of players


    def __init__(self):
        super().__init__()
        """ Initialising GUI and a worker thread """
        self._loader = OverviewLoader(self)
        self._updater = OverviewUpdater(self)
        self._loader.start()
        self._loader.finished.connect(self._update_player_data)
        self.update_refreshbutton_visuals(False)
    

    def set_window_properties(self):
        """ Setting winow properties """
        # Setting window title and size
        self.setWindowTitle("XonStat player tracker - Overview")
        self.resize(1300, 800)
    

    def create_window_layout(self):
        """ Creates widnow layout with widgets """
        # Creating the layout itself
        window_widget = QWidget()
        window_layout = QVBoxLayout()
        window_widget.setLayout(window_layout)
        self.setCentralWidget(window_widget)
        # Adding widgets to layout
        window_layout.addLayout(self._create_top_widgets())
        window_layout.addWidget(self._create_player_table())
        self.status = Status(self)
        window_layout.addWidget(self.status)
    

    def _create_top_widgets(self):
        """ Creates a box layout with search bar and a few buttons """
        layout = QHBoxLayout()
        # Creating search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search by player ID, nickname or current player name")
        self.search_bar.textChanged.connect(self._search)
        layout.addWidget(self.search_bar)
        # Creating button for refreshing table
        self.refresh_button = ColoredButton(self, None, None, False)
        self.refresh_button.clicked.connect(self._update_player_data)
        layout.addWidget(self.refresh_button)
        # Creating button for adding new player
        self.add_button = ColoredButton(self, "Add new player", "green", False)
        self.add_button.clicked.connect(self._open_addplayer_window)
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
            self.refresh_button.setBackground("orange")
        else:
            self.refresh_button.setText("Refresh table")
            self.refresh_button.setBackground("yellow")


    def _open_addplayer_window(self):
        """ Opening a window for adding a new player """
        self.add_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self._addplayer_window = AddPlayer(self)
        #self._addplayer_window.destroyed.connect(lambda: print("objekt zničen"))
    

    def addplayer_window_closed(self):
        """ Opening a window for adding a new player """
        self.add_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
    

    def _search(self, text: str):
        """ Hiding and showing rows in the table based on input """
        for row in range(self.player_table.rowCount()):
            contains_text = False
            for column in range(0, 3):
                widget = self.player_table.cellWidget(row, column)
                if not widget == None and type(widget) == ColoredLabel:
                    if text.lower() in widget.text().lower():
                        contains_text = True
                        break
            self.player_table.setRowHidden(row, not contains_text)
    

    def change_row_color(self, row: int, color: str):
        """ Changes """
        for column in range(self.player_table.columnCount()):
            widget = self.player_table.cellWidget(row, column)
            if not widget == None and type(widget) == ColoredLabel:
                widget.setBackground(color)


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
            self.player_table.setCellWidget(row, i, ColoredLabel(self.player_table))
        # Adding label text
        self.player_table.cellWidget(row, 0).setText(str(player["id"]))
        self.player_table.cellWidget(row, 1).setText(player["nick"])
        # Adding buttons
        self.player_table.setCellWidget(row, 4, ColoredButton(self.player_table, "Show player profile", "blue"))
        self.player_table.cellWidget(row, 4).clicked.connect(player.show_profile)
        self.player_table.setCellWidget(row, 5, ColoredButton(self.player_table, "Show more info", "yellow"))
        self.player_table.setCellWidget(row, 6, ColoredButton(self.player_table, "Delete this player", "red"))
        self.player_table.cellWidget(row, 6).clicked.connect(lambda: self._delete_player(player))
        if not self._loader.isFinished():
            self.player_table.cellWidget(row, 6).setEnabled(False)

    
    def update_player_variables(self, player: Player):
        """ Print out player variables into table """
        # Adding label for current player name
        widget = self.player_table.cellWidget(self.get_row(player), 2)
        if not player.error == None:
            widget.setText(player.error)
            widget.setAlignment(Qt.AlignCenter)
        else:
            widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            widget.setText(player.name)
        # Adding label for the last time this player was active
        widget = self.player_table.cellWidget(self.get_row(player), 3)
        if not player.error == None:
            widget.setText(None)
            widget.setColor(None)
        else:
            widget.setText(player.active)
            widget.setColor(player.get_active_color())
    

    def set_button_enabled(self, column: int, enabled: bool):
        """ Sets "enabled" property to a specified value for each button in the column """
        for i in range(self.player_table.rowCount()):
            widget = self.player_table.cellWidget(i, column)
            if not widget == None and type(widget) == ColoredButton:
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
        if key == Qt.Key_Return or key == Qt.Key_Enter or ((event.modifiers() & Qt.ControlModifier) and key == Qt.Key_F):
            self.search_bar.setFocus()
    

    def _delete_player(self, player: Player):
        """ Attempts to remove a player """
        try:
            answer = QMessageBox.question(self, 'XonStat player tracker', "Are you sure you want to delete player \"" \
                                        + player["nick"] + "\" (ID " + str(player["id"]) + ") ?", \
                                        QMessageBox.Yes | QMessageBox.Cancel)
            if answer == QMessageBox.Yes:
                self._remover = OverviewRemover(self, player)
                self._remover.start()
        except:
            self.status.result_message("An error occured while removing \"" + player["nick"] + "\" (ID " + str(player["id"]) + ")", False)
            self.set_button_enabled(6, True)
    

    def remove_player_from_table(self, player: Player):
        """ Removes player from table """
        self.player_table.removeRow(self.get_row(player))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker')
    overview = Overview()
    sys.exit(app.exec_())