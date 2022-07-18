from PyQt5 import QtWidgets, QtCore
import qtawesome as qta

from tabs.Tab import *
from tabs.PlayerList import *
from tabs.Search import *
from tabs.Settings import *


class NewTab(Tab):
    """Class for a new tab page
    """


    def __init__(self, parent):
        """Init

        Args:
            parent (MainWindow): Parent window
        """
        super().__init__(parent)
        self.name = "New Tab"
    

    def createLayout(self):
        self.layout.addStretch(2)
        # Adding label
        appName = ColoredLabel(self, QtWidgets.QApplication.instance().applicationName())
        appName.setAlignment(QtCore.Qt.AlignCenter)
        appName.setProperty("class", "appName")
        self.layout.addWidget(appName)
        self.layout.addStretch(1)
        # Top row of buttons
        top = QtWidgets.QHBoxLayout()
        self.layout.addLayout(top)
        top.addStretch()
        # Player list
        playerListButton = ColoredToolButton(self, "blue")
        playerListButton.setIcon(qta.icon("fa.list", color="#FFFFFF"))
        playerListButton.setText("Player list")
        playerListButton.setToolTip("List of tracked players")
        playerListButton.clicked.connect(lambda: self.parent.openTab(PlayerList))
        top.addWidget(playerListButton)
        # Search
        searchButton = ColoredToolButton(self, "yellow")
        searchButton.setIcon(qta.icon("fa.search", color="#FFFFFF"))
        searchButton.setText("Search")
        searchButton.setToolTip("Search for players, maps, servers...")
        searchButton.clicked.connect(lambda: self.parent.openTab(Search))
        top.addWidget(searchButton)
        # Settings
        settingsButton = ColoredToolButton(self, "grey")
        settingsButton.setIcon(qta.icon("mdi.hammer-screwdriver", color="#FFFFFF"))
        settingsButton.setText("Settings")
        settingsButton.setToolTip("App settings")
        settingsButton.clicked.connect(lambda: self.parent.openTab(Settings))
        top.addWidget(settingsButton)
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
        playerInfoButton.clicked.connect(lambda: self.parent.openPlayerInfo())
        bottom.addWidget(playerInfoButton)
        # Game info
        gameInfoButton = ColoredToolButton(self, "red")
        gameInfoButton.setIcon(qta.icon("fa.users", color="#FFFFFF"))
        gameInfoButton.setText("Game info")
        gameInfoButton.setToolTip("Game information")
        gameInfoButton.clicked.connect(lambda: self.parent.openGameInfo())
        bottom.addWidget(gameInfoButton)
        # Server info
        serverInfoButton = ColoredToolButton(self, "green")
        serverInfoButton.setIcon(qta.icon("fa.server", color="#FFFFFF"))
        serverInfoButton.setText("Server info")
        serverInfoButton.setToolTip("Server information")
        serverInfoButton.clicked.connect(lambda: self.parent.openServerInfo())
        bottom.addWidget(serverInfoButton)
        # Map info
        mapInfoButton = ColoredToolButton(self, "pink")
        mapInfoButton.setIcon(qta.icon("fa.map", color="#FFFFFF"))
        mapInfoButton.setText("Map info")
        mapInfoButton.setToolTip("Map information")
        mapInfoButton.clicked.connect(lambda: self.parent.openMapInfo())
        bottom.addWidget(mapInfoButton)
        bottom.addStretch()
        self.layout.addStretch(3)