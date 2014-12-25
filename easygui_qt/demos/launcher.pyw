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
        n = 0
        self.get_string_button = QtGui.QPushButton("get_string()")
        self.get_string_button.clicked.connect(self.get_string)
        self.get_string_label = QtGui.QLabel()
        self.get_string_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_string_button, n, 0)
        layout.addWidget(self.get_string_label, n, 1)
        n += 1
        self.get_int_button = QtGui.QPushButton("get_int() / get_integer()")
        self.get_int_button.clicked.connect(self.get_int)
        self.get_int_label = QtGui.QLabel()
        self.get_int_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_int_button, n, 0)
        layout.addWidget(self.get_int_label, n, 1)
        n += 1
        self.get_float_button = QtGui.QPushButton("get_float()")
        self.get_float_button.clicked.connect(self.get_float)
        self.get_float_label = QtGui.QLabel()
        self.get_float_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_float_button, n, 0)
        layout.addWidget(self.get_float_label, n, 1)
        n += 1
        self.get_choice_button = QtGui.QPushButton("get_choice()")
        self.get_choice_button.clicked.connect(self.get_choice)
        self.get_choice_label = QtGui.QLabel()
        self.get_choice_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_choice_button, n, 0)
        layout.addWidget(self.get_choice_label, n, 1)
        n += 1
        self.get_directory_button = QtGui.QPushButton("get_directory_name()")
        self.get_directory_button.clicked.connect(self.get_directory_name)
        self.get_directory_label = QtGui.QLabel()
        self.get_directory_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_directory_button, n, 0)
        layout.addWidget(self.get_directory_label, n, 1)
        n += 1
        self.get_files_button = QtGui.QPushButton("get_file_names()")
        self.get_files_button.clicked.connect(self.get_file_names)
        self.get_files_label = QtGui.QLabel()
        self.get_files_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_files_button, n, 0)
        layout.addWidget(self.get_files_label, n, 1)
        n += 1
        self.set_save_file_button = QtGui.QPushButton("set_save_file_name()")
        self.set_save_file_button.clicked.connect(self.set_save_file_name)
        self.set_save_file_label = QtGui.QLabel()
        self.set_save_file_label.setFrameStyle(frameStyle)
        layout.addWidget(self.set_save_file_button, n, 0)
        layout.addWidget(self.set_save_file_label, n, 1)


        self._layout = layout
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

    def get_directory_name(self):
        output = launch('get_directory_name')
        self.get_directory_label.setText("{}".format(output))

    def get_file_names(self):
        output = launch('get_file_names')
        self.get_files_label.setText("{}".format(output))
        self.get_files_label.setWordWrap(True)
        self.adjustSize()

    def set_save_file_name(self):
        output = launch('set_save_file_name')
        self.set_save_file_label.setText("{}".format(output))


def main():
    _ = QtGui.QApplication([])
    dialog = Dialog()
    dialog.exec_()

if __name__ == '__main__':
    main()
