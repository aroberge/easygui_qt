"""  Launcher

Demonstrates EasyGUI_Qt components at the click of a button
"""
import locale
import subprocess
import os
import sys

from PyQt4 import QtCore, QtGui

def launch(name, *args):
    """Executes a script designed specifically for this launcher.

       The parameter "name" is the name of the function to be tested
       which is passed as an argument to the script.
    """
    filename = '_launch_widget.py'
    if __name__ != "__main__":
        filename = os.path.join(os.path.dirname(__file__), filename)


    command = ['python', filename, name]
    if args:
        command.extend(args)
    output = subprocess.check_output(command)

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
        super(Dialog, self).__init__(parent, flags=flags)

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
        self.get_list_of_choices_button = QtGui.QPushButton(
                                                       "get_list_of_choices()")
        self.get_list_of_choices_button.clicked.connect(
                                                      self.get_list_of_choices)
        self.get_list_of_choices_label = QtGui.QLabel()
        self.get_list_of_choices_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_list_of_choices_button, n, 0)
        layout.addWidget(self.get_list_of_choices_label, n, 1)
        n += 1
        self.get_yes_or_no_button = QtGui.QPushButton("get_yes_or_no()")
        self.get_yes_or_no_button.clicked.connect(self.get_yes_or_no)
        self.get_yes_or_no_label = QtGui.QLabel()
        self.get_yes_or_no_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_yes_or_no_button, n, 0)
        layout.addWidget(self.get_yes_or_no_label, n, 1)
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
        self.get_save_file_button = QtGui.QPushButton("get_save_file_name()")
        self.get_save_file_button.clicked.connect(self.get_save_file_name)
        self.get_save_file_label = QtGui.QLabel()
        self.get_save_file_label.setFrameStyle(frameStyle)
        layout.addWidget(self.get_save_file_button, n, 0)
        layout.addWidget(self.get_save_file_label, n, 1)
        n += 1
        self.select_language_button = QtGui.QPushButton("select_language()")
        self.select_language_button.clicked.connect(self.select_language)
        self.select_language_label = QtGui.QLabel()
        self.select_language_label.setFrameStyle(frameStyle)
        layout.addWidget(self.select_language_button, n, 0)
        layout.addWidget(self.select_language_label, n, 1)
        n += 1
        self.set_language_button = QtGui.QPushButton("set_language()")
        self.set_language_button.clicked.connect(self.set_language)
        self.set_language_label = QtGui.QLabel()
        self.set_language_label.setFrameStyle(frameStyle)
        layout.addWidget(self.set_language_button, n, 0)
        layout.addWidget(self.set_language_label, n, 1)
        n += 1
        self.set_font_size_button = QtGui.QPushButton("set_font_size()")
        self.set_font_size_button.clicked.connect(self.set_font_size)
        self.set_font_size_label = QtGui.QLabel()
        self.set_font_size_label.setFrameStyle(frameStyle)
        layout.addWidget(self.set_font_size_button, n, 0)
        layout.addWidget(self.set_font_size_label, n, 1)
        n += 1
        self.python_version_label = QtGui.QLabel()
        #self.python_version_label.setFrameStyle(frameStyle)
        layout.addWidget(self.python_version_label, n, 0, 2, 2)
        output = subprocess.check_output(
                         ['python', '-c', "import sys;print(sys.version)"])
        self.python_version_label.setText(
                                  "Python version: {}".format(output.decode()))

        self._layout = layout
        self.setLayout(layout)
        self.setWindowTitle("EasyGUI_Qt Widget Launcher")


    def get_string(self):
        output = launch('get_string')
        if sys.version_info < (3,):
            output = output.encode(encoding=locale.getdefaultlocale()[1])
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

    def get_list_of_choices(self):
        output = launch('get_list_of_choices')
        self.get_list_of_choices_label.setText("{}".format(output))

    def get_yes_or_no(self):
        output = launch('get_yes_or_no')
        self.get_yes_or_no_label.setText("{}".format(output))

    def get_directory_name(self):
        output = launch('get_directory_name')
        self.get_directory_label.setText("{}".format(output))

    def get_file_names(self):
        output = launch('get_file_names')
        self.get_files_label.setText("{}".format(output))
        self.get_files_label.setWordWrap(True)
        self.adjustSize()

    def get_save_file_name(self):
        output = launch('get_save_file_name')
        self.get_save_file_label.setText("{}".format(output))

    def select_language(self):
        output = launch('select_language')
        output = output.split()[0]
        self.select_language_label.setText("{}".format(output))

    def set_language(self):
        _loc = launch('get_string', "Enter desired language code: 'fr', 'es', etc.")
        output = launch('set_language', _loc)
        self.set_language_label.setText("{}".format(output))

    def set_font_size(self):
        font_size = launch('get_int', "Enter desired font-size.", "title",
                           "12", "10", "20")
        output = launch('set_font_size', font_size)
        output = output.split()[0]
        self.set_font_size_label.setText("{}".format(output))




def main():
    _ = QtGui.QApplication([])
    dialog = Dialog()
    dialog.exec_()

if __name__ == '__main__':
    main()
