"""A simple text window used to display either Python code with some
simple syntax highlighting, or some other document which will be formatted as
though it was an html file or a simple text file.

The syntax highlighter for Python code is really inadequate;  HELP!! :-)
"""

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PyQt5 import QtGui, QtCore  # untested

import keyword
import sys
if sys.version_info < (3,):
    from cStringIO import StringIO
else:
    from io import StringIO


class TextWindow(QtGui.QMainWindow):
    def __init__(self, file_name=None, title="Title", file_type='text',
                 code=None):
        super(TextWindow, self).__init__(None)

        self.setWindowTitle(title)
        self.resize(900, 600)
        self.editor = QtGui.QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.editor.setFocus()

        self.handle_file(file_name, file_type, code)



    def handle_file(self, file_name, file_type, code):
        '''handling of file'''
        if file_name is None:
            if code is None:
                file_name = __file__ # use this very file as a default
                file_type = "code"
            else:
                self.handle_code(code)
                return
        text = self.load(file_name)

        if file_type == 'text':
            self.editor.setPlainText(text)
        elif file_type == 'code':
            self.set_editor_default()
            if file_name.endswith('py') or file_name.endswith('pyw'):
                self.highlighter = Highlighter(self.editor.document())
                self.editor.setPlainText(text)
        elif file_type == 'html':
            self.editor.setHtml(text)
        else:
            title = "Problem found"
            message = "Unknown file_type: {}".format(file_type)
            reply = QtGui.QMessageBox.critical(None, title, message,
            QtGui.QMessageBox.Abort | QtGui.QMessageBox.Ignore)
            if reply == QtGui.QMessageBox.Abort:
                sys.exit()
            else:
                pass

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
        return codec.toUnicode(data)

    def handle_code(self, text):
        '''Handling of code passed as a string'''
        self.set_editor_default()
        if text == "import this":  # surprise :-)
            zen = StringIO()
            old_stdout = sys.stdout
            sys.stdout = zen
            import this
            sys.stdout = old_stdout
            text = zen.getvalue()
        self.editor.setPlainText(text)


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
    app = QtGui.QApplication([])

    editor1 = TextWindow(file_name="../README.rst",
                         title="README.rst (current version)",
                         file_type = 'text')
    editor1.move(10, 10)
    editor1.show()

    editor2 = TextWindow(file_name = "readme.html",
                         title="readme.html (old version)",
                         file_type="html")
    editor2.move(840, 10)
    editor2.show()

    editor3 = TextWindow(title="Demo of Python file")
    editor3.move(440, 410)
    editor3.show()

    editor4 = TextWindow(file_name="../README.rst",
                         title="README.rst (current version)",
                         file_type = 'Dummy')

    sys.exit(app.exec_())
