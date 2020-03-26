#!/usr/bin/python3

import mainwindow

import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = mainwindow.MainWindow("test.bd")
    w.show()

    sys.exit(app.exec_())

