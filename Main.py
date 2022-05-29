#!/usr/bin/env python3
from PyQt5 import QtWidgets
import faulthandler, sys

from Overview import *



if __name__ == '__main__':
    faulthandler.enable()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker v2.3')
    overview = Overview()
    sys.exit(app.exec_())