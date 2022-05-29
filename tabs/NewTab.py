from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from tabs.Tab import *


class NewTab(Tab):
    """Class for a new tab page
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
    

    def createLayout(self):
        self.layout.addStretch()
        # Top row of buttons
        top = QtWidgets.QHBoxLayout()
        self.layout.addLayout(top)
        top.addStretch()
        # Player list
        playerListButton = ColoredToolButton(self, "blue")
        playerListButton.setIcon(qta.icon("fa.list", color="#FFFFFF"))
        playerListButton.setText("Player list")
        playerListButton.setToolTip("List of tracked players")
        top.addWidget(playerListButton)
        # XonStat home page
        homePageButton = ColoredToolButton(self, "grey")
        homePageButton.setIcon(qta.icon("ph.house-line-fill", color="#FFFFFF"))
        homePageButton.setText("XonStat home")
        homePageButton.setToolTip("XonStat homepage")
        top.addWidget(homePageButton)
        # Search
        searchButton = ColoredToolButton(self, "yellow")
        searchButton.setIcon(qta.icon("fa.search", color="#FFFFFF"))
        searchButton.setText("Search")
        searchButton.setToolTip("Search for players, maps, servers...")
        top.addWidget(searchButton)
        top.addStretch()
        # Bottom row of buttons
        bottom = QtWidgets.QHBoxLayout()
        self.layout.addLayout(bottom)
        bottom.addStretch()
        # Player info
        playerInfoButton = ColoredToolButton(self, "orange")
        playerInfoButton.setIcon(qta.icon("fa.user", color="#FFFFFF"))
        playerInfoButton.setText("Player info")
        playerInfoButton.setToolTip("Player information")
        bottom.addWidget(playerInfoButton)
        # Game info
        gameInfoButton = ColoredToolButton(self, "red")
        gameInfoButton.setIcon(qta.icon("fa.users", color="#FFFFFF"))
        gameInfoButton.setText("Game info")
        gameInfoButton.setToolTip("Game information")
        bottom.addWidget(gameInfoButton)
        # Server info
        serverInfoButton = ColoredToolButton(self, "green")
        serverInfoButton.setIcon(qta.icon("fa.server", color="#FFFFFF"))
        serverInfoButton.setText("Server info")
        serverInfoButton.setToolTip("Server information")
        bottom.addWidget(serverInfoButton)
        # Map info
        mapInfoButton = ColoredToolButton(self, "pink")
        mapInfoButton.setIcon(qta.icon("fa.map", color="#FFFFFF"))
        mapInfoButton.setText("Map info")
        mapInfoButton.setToolTip("Map information")
        bottom.addWidget(mapInfoButton)
        bottom.addStretch()
        self.layout.addStretch()