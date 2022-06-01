from PyQt5 import QtWidgets

from tabs.Tab import *


class TabInfo(Tab):
    """Class for showing player information
    """


    def __init__(self, parent, identifier: int = None):
        """Init

        Args:
            parent (MainWindow): Parent window
            identifier (int): Player ID
        """
        self.id = identifier
        super().__init__(parent)
    

    def createLayout(self):
        """Creating tab layout
        """
        # Creating input field for player ID
        self.identifierInput = QtWidgets.QLineEdit(self)
        if self.id is not None:
            self.identifierInput.setText(str(self.id))
        else:
            self.identifierInput.setFocus()
        self.identifierInput.textChanged.connect(self.startLoading)
        self.layout.addWidget(self.identifierInput)
    

    def startLoading(self) -> bool:
        """Starting page (re)loading
        """
        if self.identifierInput.text() is None or self.identifierInput.text() == "":
            return False
        try:
            self.id = int(self.identifierInput.text())
        except:
            self.id = None
            self.status.resultMessage("Entered ID is not a number", False)
            return False
        else:
            for i in range(self.parent.tabWidget.count()):
                if self != self.parent.tabWidget.widget(i) and isinstance(self.parent.tabWidget.widget(i), type(self)):
                    if self.id == self.parent.tabWidget.widget(i).id:
                        self.parent.removeTab(self.parent.tabWidget.currentIndex())
                        self.parent.tabWidget.setCurrentIndex(i)
                        return False
        return True
    

    def localKeyPressEvent(self, event):
        """Handling key press events

        Args:
            event: Event
        """
        key = event.key()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Setting focus to ID input field
            if key == QtCore.Qt.Key_F:
                self.identifierInput.setFocus()
                self.identifierInput.selectAll()