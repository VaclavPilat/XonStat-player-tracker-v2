#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class Oveview(QWidget):
    """ Class for creating a window that contains a table with currently tracked players """

    def __init__(self):
        super().__init__()
        self._set_window_properties()
        self._create_window_layout()
        self.show()
    

    def _set_window_properties(self):
        """ Setting winow properties """

        # Setting window title and size
        self.setWindowTitle("XonStat player tracker - Overview")
        self.setGeometry(0, 0, 1200, 800)

        # Moving window to the center of the screen
        frameGeometry = self.frameGeometry()
        frameGeometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frameGeometry.topLeft())
    

    def _create_window_layout(self):
        """ Creates widnow layout with widgets """

        # Creating the layout itself
        self.window_layout = QVBoxLayout()
        self.setLayout(self.window_layout)

        # Creating table widget
        self._create_player_table()


    def _create_player_table(self):
        """ Creating table of players """

        self.player_table = QTableWidget()

        # Setting columns
        table_headers = ["ID", "Player nickname", "Current player name", "Last played", 
                        "Player profile", "More information", "Delete player"]
        self.player_table.setColumnCount( len(table_headers) )
        self.player_table.setHorizontalHeaderLabels(table_headers)

        # Filling the table with data
        self.player_table.setRowCount(10)
        self.player_table.setItem(0,0, QTableWidgetItem("Name"))

        # Enabling horizontal stretching
        self.player_table.horizontalHeader().setStretchLastSection(True)
        self.player_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Adding table to the window layout
        self.window_layout.addWidget(self.player_table)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overview = Oveview()
    sys.exit(app.exec_())