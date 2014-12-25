"""  Launcher

Demonstrates EasyGUI_Qt components at the click of a button
"""

import locale
import subprocess
import os
from PyQt4 import QtCore, QtGui

def launch(name):
    """Executes a script designed specifically for this launcher.

       The parameter "name" is the name of the function to be tested
       which is passed as an argument to the script.
    """
    filename = '_launch_widget.pyw'
    if __name__ != "__main__":
        filename = os.path.join(os.path.dirname(__file__), filename)
    output = subprocess.check_output('python {} {}'.format(filename, name))
    try:
        output = output.decode(encoding='UTF-8')
    except:
        try:
            output = output.decode(encoding=locale.getdefaultlocale()[1])
        except:
            print("could not decode")
    return output


class Dialog(QtGui.QDialog):

    def __init__(self, parent=None):
        flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
        super().__init__(parent, flags=flags)

        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self.get_string_button = QtGui.QPushButton("get_string()")
        self.get_string_button.clicked.connect(self.get_string)
        self.get_string_label = QtGui.QLabel()
        self.get_string_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_string_button, 0, 0)
        layout.addWidget(self.get_string_label, 0, 1)

        self.get_int_button = QtGui.QPushButton("get_int() / get_integer()")
        self.get_int_button.clicked.connect(self.get_int)
        self.get_int_label = QtGui.QLabel()
        self.get_int_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_int_button, 1, 0)
        layout.addWidget(self.get_int_label, 1, 1)

        self.get_float_button = QtGui.QPushButton("get_float()")
        self.get_float_button.clicked.connect(self.get_float)
        self.get_float_label = QtGui.QLabel()
        self.get_float_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_float_button, 2, 0)
        layout.addWidget(self.get_float_label, 2, 1)

        self.get_choice_button = QtGui.QPushButton("get_choice()")
        self.get_choice_button.clicked.connect(self.get_choice)
        self.get_choice_label = QtGui.QLabel()
        self.get_choice_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_choice_button, 3, 0)
        layout.addWidget(self.get_choice_label, 3, 1)


        self.setLayout(layout)
        self.setWindowTitle("EasyGUI_Qt launcher")


    def get_string(self):
        output = launch('get_string')
        self.get_string_label.setText("{}".format(output))

    def get_int(self):
        output = launch('get_int')
        self.get_int_label.setText("{}".format(output))

    def get_float(self):
        output = launch('get_float')
        self.get_float_label.setText("{}".format(output))

    def get_choice(self):
        output = launch('get_choice')
        self.get_choice_label.setText("{}".format(output))


def main():
    _ = QtGui.QApplication([])
    dialog = Dialog()
    dialog.exec_()

if __name__ == '__main__':
    main()
