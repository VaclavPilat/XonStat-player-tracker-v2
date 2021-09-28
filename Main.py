#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
from Overview import *



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('XonStat player tracker')
    overview = Overview()
    sys.exit(app.exec_())