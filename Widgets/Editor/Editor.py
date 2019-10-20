#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QTextEdit, QCommonStyle
from PySide2.QtGui import QTextOption, QFont, QFontMetrics, QTextCursor, QTextBlockFormat, QPalette, QBrush, QPainter, \
    QColor
from PySide2.QtCore import Qt, QRect
from .MaxLineLength import MaxLineLength
from .LineNumberArea import LineNumberArea


class Editor(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWordWrapMode(QTextOption.NoWrap)

        # Widgets
        self.maxLineLength = MaxLineLength(self)
        self.lineNumberArea = LineNumberArea(self)

        self.__lineHeight = self.fontMetrics().height()
        self.__lineHeightMultiplier = 1  # TODO: find a way for this to work... (should be 1.35)
        self.__bottomLines = 3
        self.__tabStop = 4

        self.__highlighter = None

        self.__setStyle()
        self.__setBottomMargin()

        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.textChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.updateLineNumberArea)

    # region LineNumberArea
    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.document().blockCount())))
        return self.fontMetrics().width('9') * digits + \
               self.lineNumberArea.leftMargin + self.lineNumberArea.rightMargin

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self):
        rect = self.contentsRect()
        self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        self.updateLineNumberAreaWidth()

        dy = self.verticalScrollBar().sliderPosition()
        if dy > -1:
            self.lineNumberArea.scroll(0, dy)

        # Adjust slider to always see the number of the currently being edited line...
        first_block_id = self.getFirstVisibleBlockId()
        if first_block_id == 0 or self.textCursor().block().blockNumber() == first_block_id - 1:
            self.verticalScrollBar().setSliderPosition(dy - int(self.document().documentMargin()))

    def getFirstVisibleBlockId(self):
        """
        Detect the first block for which bounding rect - once translated in absolute coordinated -
        is contained by the editor's text area
        :return: the first visible block
        """

        if self.verticalScrollBar().sliderPosition() == 0:
            return 0

        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.Start)
        for i in range(self.document().blockCount()):
            block = cursor.block()
            r1 = self.viewport().geometry()
            r2 = self.document().documentLayout().blockBoundingRect(block).translated(
                self.viewport().geometry().x(),
                self.viewport().geometry().y() - self.verticalScrollBar().sliderPosition()
            ).toRect()

            if r1.contains(r2, True):
                return i

            cursor.movePosition(QTextCursor.NextBlock)

        return 0

    def lineNumberAreaPaintEvent(self, e):
        self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition())

        painter = QPainter(self.lineNumberArea)

        # draw the background
        background = self.lineNumberArea.palette().color(self.lineNumberArea.backgroundRole())
        painter.fillRect(e.rect(), background)

        currentBlockNumber = self.textCursor().blockNumber()
        blockNumber = self.getFirstVisibleBlockId()
        block = self.document().findBlockByNumber(blockNumber)

        prev_block = self.document().findBlockByNumber(blockNumber - 1) if blockNumber > 0 else block
        translate_y = - self.verticalScrollBar().sliderPosition() if blockNumber > 0 else 0

        # Adjust text position according to the previous "non entirely visible" block if applicable
        # Also takes in consideration the document's margin offset.
        if blockNumber == 0:
            # Simply adjust to document's margin
            additional_margin = self.document().documentMargin() - 1 - self.verticalScrollBar().sliderPosition()
        else:
            # Getting the height of the visible part of the previous "non entirely visible" block
            # additional_margin = self.document().documentLayout().blockBoundingRect(prev_block).translated(
            #     0, translate_y).intersect(self.viewport().geometry().height())
            additional_margin = self.document().documentLayout().blockBoundingRect(prev_block).translated(
                0, translate_y).intersected(self.viewport().geometry()).height()

        # Shift the starting point
        top = self.viewport().geometry().top() + additional_margin
        bottom = top + self.document().documentLayout().blockBoundingRect(block).height()

        col_1 = QColor(90, 255, 30)     # Current line (custom green)
        col_0 = QColor(120, 120, 120)   # Other lines  (custom darkgrey)

        # Draw the numbers (displaying the current line number in green)
        while block.isValid() and top <= e.rect().bottom():
            if block.isVisible() and bottom >= e.rect().top():
                number = str(int(blockNumber + 1))
                painter.setPen(col_1 if currentBlockNumber == blockNumber else col_0)
                painter.drawText(0,
                                 top,
                                 self.lineNumberArea.width() - self.lineNumberArea.rightMargin,
                                 self.fontMetrics().height(),
                                 Qt.AlignRight,
                                 number)

            block = block.next()
            top = bottom
            bottom = top + self.document().documentLayout().blockBoundingRect(block).height()
            blockNumber += 1
    # endregion

    def __setStyle(self):
        # disable selection color to keep syntax highlighting when a selection occurs
        palette = self.palette()
        palette.setBrush(QPalette.HighlightedText, QBrush(Qt.NoBrush))
        self.setPalette(palette)

        # remove scrollbars style
        self.verticalScrollBar().setStyle(QCommonStyle())
        self.horizontalScrollBar().setStyle(QCommonStyle())

    def __setLineHeight(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        fmt = QTextBlockFormat()
        fmt.setLineHeight(self.__lineHeight, QTextBlockFormat.FixedHeight)
        cursor.setBlockFormat(fmt)

    def __setBottomMargin(self):
        maxVisibleLines = self.contentsRect().height() / self.__lineHeight
        frameFormat = self.document().rootFrame().frameFormat()
        frameFormat.setBottomMargin((maxVisibleLines - self.__bottomLines) * self.__lineHeight)
        self.document().rootFrame().setFrameFormat(frameFormat)

    def setFont(self, qFont):
        qFont.setStyleHint(QFont.Monospace)
        qFont.setFixedPitch(True)
        fontMetrics = QFontMetrics(qFont)
        self.setTabStopWidth(self.__tabStop * fontMetrics.width(' '))
        self.__lineHeight = fontMetrics.height() * self.__lineHeightMultiplier

        super().setFont(qFont)
        self.__setLineHeight()

    def setHighlighter(self, highlighter):
        self.__highlighter = highlighter
        highlighter.setDocument(self.document())

    def resizeEvent(self, event):
        """Reset the bottom margin on resize"""
        super(Editor, self).resizeEvent(event)
        self.__setBottomMargin()

        # lineNumberArea
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        self.maxLineLength.setGeometry(QRect(0, 0, self.width(), self.height()))
