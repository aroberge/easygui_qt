"""  Launcher

Demonstrates each component at the click of a button
"""

import subprocess
import os
import sys
from PyQt4 import QtCore, QtGui

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.getcwd(), "../"))
    import easygui_qt as easy
else:
    import easygui_qt as easy


def launch(function):
    function = 'launch_' + function
    if __name__ == "__main__":
        arg = 'python {}.pyw'.format(function)
    else:
        pth = os.path.join(os.path.dirname(__file__), function)
        arg = 'python {}.pyw'.format(pth)
    kwd = {'universal_newlines': True}
    return subprocess.check_output(arg, **kwd)



class Dialog(QtGui.QDialog):

    def __init__(self, parent=None):
        flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
        super().__init__(parent, flags=flags)

        self.openFilesPath = ''

        self.errorMessageDialog = QtGui.QErrorMessage(self)

        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.integerLabel = QtGui.QLabel()
        self.integerLabel.setFrameStyle(frameStyle)
        self.integerButton = QtGui.QPushButton("get_string()")

        self.doubleLabel = QtGui.QLabel()
        self.doubleLabel.setFrameStyle(frameStyle)
        self.doubleButton = QtGui.QPushButton("QInputDialog.get&Double()")

        self.itemLabel = QtGui.QLabel()
        self.itemLabel.setFrameStyle(frameStyle)
        self.itemButton = QtGui.QPushButton("QInputDialog.getIte&m()")

        self.textLabel = QtGui.QLabel()
        self.textLabel.setFrameStyle(frameStyle)
        self.textButton = QtGui.QPushButton("QInputDialog.get&Text()")

        self.colorLabel = QtGui.QLabel()
        self.colorLabel.setFrameStyle(frameStyle)
        self.colorButton = QtGui.QPushButton("QColorDialog.get&Color()")

        self.fontLabel = QtGui.QLabel()
        self.fontLabel.setFrameStyle(frameStyle)
        self.fontButton = QtGui.QPushButton("QFontDialog.get&Font()")

        self.directoryLabel = QtGui.QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QtGui.QPushButton("QFileDialog.getE&xistingDirectory()")

        self.openFileNameLabel = QtGui.QLabel()
        self.openFileNameLabel.setFrameStyle(frameStyle)
        self.openFileNameButton = QtGui.QPushButton("QFileDialog.get&OpenFileName()")

        self.openFileNamesLabel = QtGui.QLabel()
        self.openFileNamesLabel.setFrameStyle(frameStyle)
        self.openFileNamesButton = QtGui.QPushButton("QFileDialog.&getOpenFileNames()")

        self.saveFileNameLabel = QtGui.QLabel()
        self.saveFileNameLabel.setFrameStyle(frameStyle)
        self.saveFileNameButton = QtGui.QPushButton("QFileDialog.get&SaveFileName()")

        self.criticalLabel = QtGui.QLabel()
        self.criticalLabel.setFrameStyle(frameStyle)
        self.criticalButton = QtGui.QPushButton("QMessageBox.critica&l()")

        self.informationLabel = QtGui.QLabel()
        self.informationLabel.setFrameStyle(frameStyle)
        self.informationButton = QtGui.QPushButton("QMessageBox.i&nformation()")

        self.questionLabel = QtGui.QLabel()
        self.questionLabel.setFrameStyle(frameStyle)
        self.questionButton = QtGui.QPushButton("QMessageBox.&question()")

        self.warningLabel = QtGui.QLabel()
        self.warningLabel.setFrameStyle(frameStyle)
        self.warningButton = QtGui.QPushButton("QMessageBox.&warning()")

        self.errorLabel = QtGui.QLabel()
        self.errorLabel.setFrameStyle(frameStyle)
        self.errorButton = QtGui.QPushButton("QErrorMessage.show&M&essage()")

        self.integerButton.clicked.connect(self.get_string)
        self.doubleButton.clicked.connect(self.setDouble)
        self.itemButton.clicked.connect(self.setItem)
        self.textButton.clicked.connect(self.setText)
        self.colorButton.clicked.connect(self.setColor)
        self.fontButton.clicked.connect(self.setFont)
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.openFileNameButton.clicked.connect(self.setOpenFileName)
        self.openFileNamesButton.clicked.connect(self.setOpenFileNames)
        self.saveFileNameButton.clicked.connect(self.setSaveFileName)
        self.criticalButton.clicked.connect(self.criticalMessage)
        self.informationButton.clicked.connect(self.informationMessage)
        self.questionButton.clicked.connect(self.questionMessage)
        self.warningButton.clicked.connect(self.warningMessage)
        self.errorButton.clicked.connect(self.errorMessage)

        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()

        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)
        layout.addWidget(self.integerButton, 0, 0)
        layout.addWidget(self.integerLabel, 0, 1)
        layout.addWidget(self.doubleButton, 1, 0)
        layout.addWidget(self.doubleLabel, 1, 1)
        layout.addWidget(self.itemButton, 2, 0)
        layout.addWidget(self.itemLabel, 2, 1)
        layout.addWidget(self.textButton, 3, 0)
        layout.addWidget(self.textLabel, 3, 1)
        layout.addWidget(self.colorButton, 4, 0)
        layout.addWidget(self.colorLabel, 4, 1)
        layout.addWidget(self.fontButton, 5, 0)
        layout.addWidget(self.fontLabel, 5, 1)
        layout.addWidget(self.directoryButton, 6, 0)
        layout.addWidget(self.directoryLabel, 6, 1)
        layout.addWidget(self.openFileNameButton, 7, 0)
        layout.addWidget(self.openFileNameLabel, 7, 1)
        layout.addWidget(self.openFileNamesButton, 8, 0)
        layout.addWidget(self.openFileNamesLabel, 8, 1)
        layout.addWidget(self.saveFileNameButton, 9, 0)
        layout.addWidget(self.saveFileNameLabel, 9, 1)
        layout.addWidget(self.criticalButton, 10, 0)
        layout.addWidget(self.criticalLabel, 10, 1)
        layout.addWidget(self.informationButton, 11, 0)
        layout.addWidget(self.informationLabel, 11, 1)
        layout.addWidget(self.questionButton, 12, 0)
        layout.addWidget(self.questionLabel, 12, 1)
        layout.addWidget(self.warningButton, 13, 0)
        layout.addWidget(self.warningLabel, 13, 1)
        layout.addWidget(self.errorButton, 14, 0)
        layout.addWidget(self.errorLabel, 14, 1)
        layout.addWidget(self.native, 15, 0)
        self.setLayout(layout)

        self.setWindowTitle("EasyGUI_Qt launcher")


    def get_string(self):
        output = launch('get_string')
        self.integerLabel.setText("{}".format(output))


    def setDouble(self):
        d, ok = QtGui.QInputDialog.getDouble(self, "QInputDialog.getDouble()",
                "Amount:", 37.56, -10000, 10000, 2)
        if ok:
            self.doubleLabel.setText("$%g" % d)

    def setItem(self):
        items = ("Spring", "Summer", "Fall", "Winter")

        item, ok = QtGui.QInputDialog.getItem(self, "QInputDialog.getItem()",
                "Season:", items, 0, False)
        if ok and item:
            self.itemLabel.setText(item)

    def setText(self):
        text, ok = QtGui.QInputDialog.getText(self, "QInputDialog.getText()",
                "User name:", QtGui.QLineEdit.Normal,
                QtCore.QDir.home().dirName())
        if ok and text != '':
            self.textLabel.setText(text)

    def setColor(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.green, self)
        if color.isValid():
            self.colorLabel.setText(color.name())
            self.colorLabel.setPalette(QtGui.QPalette(color))
            self.colorLabel.setAutoFillBackground(True)

    def setFont(self):
        font, ok = QtGui.QFontDialog.getFont(QtGui.QFont(self.fontLabel.text()), self)
        if ok:
            self.fontLabel.setText(font.key())
            self.fontLabel.setFont(font)

    def setExistingDirectory(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "QFileDialog.getExistingDirectory()",
                self.directoryLabel.text(), options)
        if directory:
            self.directoryLabel.setText(directory)

    def setOpenFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()",
                self.openFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)", options)
        if fileName:
            self.openFileNameLabel.setText(fileName)

    def setOpenFileNames(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        files = QtGui.QFileDialog.getOpenFileNames(self,
                "QFileDialog.getOpenFileNames()", self.openFilesPath,
                "All Files (*);;Text Files (*.txt)", options)
        if files:
            self.openFilesPath = files[0]
            self.openFileNamesLabel.setText("[%s]" % ', '.join(files))

    def setSaveFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                self.saveFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)", options)
        if fileName:
            self.saveFileNameLabel.setText(fileName)

    def criticalMessage(self):
        reply = QtGui.QMessageBox.critical(self, "QMessageBox.critical()",
                Dialog.MESSAGE,
                QtGui.QMessageBox.Abort | QtGui.QMessageBox.Retry | QtGui.QMessageBox.Ignore)
        if reply == QtGui.QMessageBox.Abort:
            self.criticalLabel.setText("Abort")
        elif reply == QtGui.QMessageBox.Retry:
            self.criticalLabel.setText("Retry")
        else:
            self.criticalLabel.setText("Ignore")

    def informationMessage(self):
        reply = QtGui.QMessageBox.information(self,
                "QMessageBox.information()", Dialog.MESSAGE)
        if reply == QtGui.QMessageBox.Ok:
            self.informationLabel.setText("OK")
        else:
            self.informationLabel.setText("Escape")

    def questionMessage(self):
        reply = QtGui.QMessageBox.question(self, "QMessageBox.question",
                Dialog.MESSAGE,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            self.questionLabel.setText("Yes")
        elif reply == QtGui.QMessageBox.No:
            self.questionLabel.setText("No")
        else:
            self.questionLabel.setText("Cancel")

    def warningMessage(self):
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "QMessageBox.warning()", Dialog.MESSAGE,
                QtGui.QMessageBox.NoButton, self)
        msgBox.addButton("Save &Again", QtGui.QMessageBox.AcceptRole)
        msgBox.addButton("&Continue", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            self.warningLabel.setText("Save Again")
        else:
            self.warningLabel.setText("Continue")

    def errorMessage(self):
        self.errorMessageDialog.showMessage("This dialog shows and remembers "
                "error messages. If the checkbox is checked (as it is by "
                "default), the shown message will be shown again, but if the "
                "user unchecks the box the message will not appear again if "
                "QErrorMessage.showMessage() is called with the same message.")
        self.errorLabel.setText("If the box is unchecked, the message won't "
                "appear again.")


def main():
    _ = QtGui.QApplication([])
    dialog = Dialog()
    dialog.exec_()

if __name__ == '__main__':
    main()
