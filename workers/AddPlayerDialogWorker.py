from PyQt5 import QtCore

from misc.Functions import *
from dialogs.Dialog import *


class AddPlayerDialogWorker(QtCore.QThread):
    """Worker class is for executing background tasks
    """


    setPlayerNickname = QtCore.pyqtSignal(str)


    def __init__(self, dialog: Dialog):
        """Initialising QtCore.QThread, connecting slots

        Args:
            dialog (Dialog): Dialog object that this class was instantiated in
        """
        super().__init__()
        self.dialog = dialog
        self.cancel = False
        self.setPlayerNickname.connect(self.dialog.nick.setText)
    

    def run(self):
        """Running the Worker task
        """
        response = None
        try:
            response = createRequest("https://stats.xonotic.org/player/" + str(self.dialog.id))
            self.showRate.emit(response.headers["X-Ratelimit-Remaining"], response.headers["X-Ratelimit-Limit"])
        except:
            pass
        # Canceling
        if self.cancel:
            return
        # Checking response
        if response is not None and response:
            data = response.json()
            self.setPlayerNickname.emit(processNick( data["player"]["nick"] ))