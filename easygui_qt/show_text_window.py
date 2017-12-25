"""A simple text window used to display either Python code with some
simple syntax highlighting, or some other document which will be formatted as
though it was an html file or a simple text file.

The syntax highlighter for Python code is really inadequate;  HELP!! :-)
"""

try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWidgets as qt_widgets

import keyword
import sys
if sys.version_info < (3,):
    from cStringIO import StringIO
else:
    from io import StringIO


class TextWindow(qt_widgets.QMainWindow):
    def __init__(self, file_name=None, title="Title", text_type='text',
                 text='Default text'):
        """Simple text window whose input comes from a file, if a file_name 
           is specified, or from a supplied string.

           text_type can be one of  4 values: 'text', 'code', 'html', 'python'.
           If 'python' is specified, some basic syntax highlighting is added.
        """
        super(TextWindow, self).__init__(None)

        self.setWindowTitle(title)
        self.resize(900, 600)
        self.editor = qt_widgets.QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.editor.setFocus()

        if file_name is not None:
            text = self.load(file_name)

        if text_type == 'text' or text_type == 'html':
            self.set_text_font()
        elif text_type == 'code':
            self.set_monospace_font()
        elif text_type == 'python':
            self.set_monospace_font()
            self.highlighter = Highlighter(self.editor.document())
        else:
            self.set_text_font()
            text = "Unknown text_type: {}".format(text_type)

        if text_type == 'html':
            self.editor.setHtml(text)
        else:
            self.editor.setPlainText(text)


    def set_text_font(self):
        font = QtGui.QFont()
        font.setFamily('Arial')
        font.setFixedPitch(False)
        font.setPointSize(12)
        self.editor.setFont(font)

    def set_monospace_font(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.editor.setFont(font)


    def load(self, f):
        if not QtCore.QFile.exists(f):
            self.text_type = 'text'
            return "File %s could not be found." % f

        try:
            file_handle = QtCore.QFile(f)
            file_handle.open(QtCore.QFile.ReadOnly)
            data = file_handle.readAll()
            codec = QtCore.QTextCodec.codecForHtml(data)
            return codec.toUnicode(data)
        except:
            self.text_type = 'text'
            return 'Problem reading file %s' % f


class Highlighter(QtGui.QSyntaxHighlighter):
    """Adapted from example included with PyQt distribution"""
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.blue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywordPatterns = ["\\b{}\\b".format(k) for k in keyword.kwlist]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QtGui.QTextCharFormat()
        classFormat.setFontWeight(QtGui.QFont.Bold)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.gray)
        self.highlightingRules.append((QtCore.QRegExp("#[^\n]*"),
                singleLineCommentFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))
        self.highlightingRules.append((QtCore.QRegExp("'.*'"),
                quotationFormat))


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


if __name__ == '__main__':
    app = qt_widgets.QApplication([])

    editor1 = TextWindow(file_name="../README.rst",
                         title="Demo of text file",
                         text_type = 'text')
    editor1.move(10, 10)
    editor1.show()

    editor2 = TextWindow(file_name = "readme.html",
                         title="Demo of html file",
                         text_type="html")
    editor2.move(840, 10)
    editor2.show()

    editor3 = TextWindow(title="Demo of Python file", file_name=__file__, text_type='python')
    editor3.move(440, 410)
    editor3.show()

    editor4 = TextWindow(file_name="../README.rst",
                         title="Demo of unknown test_type",
                         text_type = 'unknown')
    editor4.show()

    sys.exit(app.exec_())
