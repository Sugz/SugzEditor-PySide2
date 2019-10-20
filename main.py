#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QMainWindow
from Widgets import Editor
from Syntaxs.python import PythonSyntax

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fontSize = 10
        self.font = QFont("Consolas", self.fontSize)
        self.editor = Editor(self)
        self.editor.setFont(self.font)
        self.editor.setHighlighter(PythonSyntax())
        self.setCentralWidget(self.editor)

        # Window
        with open('./Stylesheets/dark.css') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # file to open as test
        with open('./main.py') as tempCode:
            self.editor.setText(tempCode.read())

        self.setWindowTitle('SgzEditor')
        self.resize(1400, 800)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()

    app.exec_()
