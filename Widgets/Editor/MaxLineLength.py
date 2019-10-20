#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt, QSize


class MaxLineLength(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__editor = parent
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.column = 121

    def paintEvent(self, e):
        painter = QPainter(self)
        x = self.column * self.__editor.fontMetrics().averageCharWidth()
        color = self.palette().color(self.backgroundRole())
        painter.setPen(color)
        painter.drawLine(x, 0, x, self.__editor.height())

