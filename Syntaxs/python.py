#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PySide2.QtCore import QRegExp, Qt


class PythonSyntax(QSyntaxHighlighter):
    """Syntax Highlighter for Python"""

    def __init__(self, document=None):
        super(PythonSyntax, self).__init__(document)

        self.rules = []

        # keywords
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'with', 'yield',
            'None', 'True', 'False',
        ]
        self.rules += [(QRegExp(r'\b%s\b' % pattern), self.getTextCharFormat(QColor(200, 120, 50)), 0)
                       for pattern in keywords]

        # braces
        braces = ['\(', '\)', '\[', '\]', '\{', '\}']
        self.rules += [(QRegExp(r'%s' % pattern), self.getTextCharFormat(Qt.gray), 0)
                       for pattern in braces]

        # numerics
        numerics = [
            r'\b[+-]?[0-9]+[lL]?\b',
            r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b',
            r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b',
        ]
        self.rules += [(QRegExp('%s' % pattern), self.getTextCharFormat(QColor(106, 149, 185)), 0)
                       for pattern in numerics]

        # operators
        operators = [
            '=',
            # Comparison
            '==', '!=', '<', '<=', '>', '>=',
            # Arithmetic
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            # In-place
            '\+=', '-=', '\*=', '/=', '\%=',
            # Bitwise
            '\^', '\|', '\&', '\~', '>>', '<<',
        ]
        self.rules += [(QRegExp(r'%s' % pattern), self.getTextCharFormat(QColor(210, 160, 160)), 0)
                       for pattern in operators]

        # punctuation
        punctuation = [',', ':']
        self.rules += [(QRegExp(r'%s' % pattern), self.getTextCharFormat(QColor(200, 120, 50)), 0)
                       for pattern in punctuation]

        # self
        self.rules += [(QRegExp(r'\bself\b'), self.getTextCharFormat(QColor(145, 86, 140)), 0)]

        # Built-in Functions
        builtins = [
            '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint',
            'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile',
            'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval',
            'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals',
            'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview',
            'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted',
            'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
        ]
        self.rules += [(QRegExp(r'\b%s\b' % pattern), self.getTextCharFormat(QColor(135, 135, 197)), 0)
                       for pattern in builtins]

        self.rules += [(QRegExp(r'\bsuper\b'), self.getTextCharFormat(QColor(135, 135, 197)), 0)]

        # 'def' or 'class' followed by an identifier
        identifiers = [
            r'\bdef\b\s*(\w+)',
            r'\bclass\b\s*(\w+)',
        ]
        self.rules += [(QRegExp('%s' % pattern), self.getTextCharFormat(QColor(253, 197, 107)), 1)
                       for pattern in identifiers]

        # dunder methods
        # self.rules += [(QRegExp(r'\b__\w+__\b'), self.getTextCharFormat(QColor(173, 1, 177)), 0)]
        self.rules += [(QRegExp(r'\b__[a-zA-Z_]*__\b'), self.getTextCharFormat(QColor(173, 1, 177)), 0)]

        # strings
        strings = [
            # Double-quoted string, possibly containing escape sequences
            r'[f-r]*"[^"\\]*(\\.[^"\\]*)*"',
            # Single-quoted string, possibly containing escape sequences
            r"[f-r]*'[^'\\]*(\\.[^'\\]*)*'",
        ]
        self.rules += [(QRegExp('%s' % pattern), self.getTextCharFormat(QColor(88, 133, 74)), 0)
                       for pattern in strings]

        # decorator
        # self.rules += [(QRegExp(r'@\w+'), self.getTextCharFormat(QColor(185, 180, 40)), 0)]
        self.rules += [(QRegExp(r'@[a-zA-Z_]*'), self.getTextCharFormat(QColor(185, 180, 40)), 0)]

        # From '#' until a newline
        self.rules += [(QRegExp(r'#[^\n]*'), self.getTextCharFormat(Qt.darkGray), 0)]

    def highlightBlock(self, text):
        for regExp, charFormat, nth in self.rules:
            index = regExp.indexIn(text)
            while index >= 0:
                index = regExp.pos(nth)
                length = len(regExp.cap(nth))
                self.setFormat(index, length, charFormat)
                index = regExp.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    def getTextCharFormat(self, color, style=None):
        """Return a QTextCharFormat with the given attributes."""
        textCharFormat = QTextCharFormat()
        textCharFormat.setForeground(color)
        if style is not None:
            if 'bold' in style:
                textCharFormat.setFontWeight(QFont.Bold)
            if 'italic' in style:
                textCharFormat.setFontItalic(True)

        return textCharFormat
