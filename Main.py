#!/usr/bin/env python3
from PyQt5 import QtWidgets
import faulthandler

from Overview import *



if __name__ == '__main__':
    faulthandler.enable()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker')
    overview = Overview()
    sys.exit(app.exec_())