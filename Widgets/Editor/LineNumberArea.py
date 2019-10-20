#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QSize


class LineNumberArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__editor = parent

        self.leftMargin = 10
        self.rightMargin = 10

    def sizeHint(self):
        return QSize(self.__editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, e):
        self.__editor.lineNumberAreaPaintEvent(e)
