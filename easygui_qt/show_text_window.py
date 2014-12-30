"""A simple text window used to display either Python code with some
simple syntax highlighting, or some other document which will be formatted as
though it was an html file ... and one other possibility which you can
see by looking at the code below.

The syntax highlighter for Python code is really inadequate;  HELP!! :-)
"""

from PyQt4 import QtCore, QtGui
import keyword

class TextWindow(QtGui.QMainWindow):
    def __init__(self, file_name=None, title="Title", html=False):
        super(TextWindow, self).__init__(None)

        self.setWindowTitle(title)
        self.resize(900, 600)
        self.editor = QtGui.QTextEdit(self)


        self.setCentralWidget(self.editor)
        self.editor.setFocus()
        if file_name is None:
            file_name = __file__
        self.load(file_name)

        if file_name.endswith('py') or file_name.endswith('pyw'):
            self.set_editor_default()
            self.highlighter = Highlighter(self.editor.document())
            self.editor.setPlainText(self.text)
        elif html:
            self.editor.setHtml(self.text)
        else:
            self.set_editor_default()
            self.editor.setPlainText(self.text)

    def set_editor_default(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.editor.setFont(font)

    def load(self, f):
        if not QtCore.QFile.exists(f):
            self.text = "<h1>File could not be found</h1>"
            return

        file_handle = QtCore.QFile(f)
        file_handle.open(QtCore.QFile.ReadOnly)
        data = file_handle.readAll()
        codec = QtCore.QTextCodec.codecForHtml(data)
        self.text = codec.toUnicode(data)


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
    import sys
    app = QtGui.QApplication([])

    editor1 = TextWindow("../README.rst", title="README.rst (current version)")
    editor1.move(10, 10)
    editor1.show()

    editor2 = TextWindow("readme.html", title="readme.html (old version)",
                         html=True)
    editor2.move(840, 10)
    editor2.show()

    editor3 = TextWindow(title="Demo of Python file")
    editor3.move(440, 410)
    editor3.show()

    sys.exit(app.exec_())
