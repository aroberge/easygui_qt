"""  Launcher

Demonstrates EasyGUI_Qt components at the click of a button
"""
import locale
import subprocess
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import easygui_qt

from PyQt4 import QtCore, QtGui

def launch(name, *args):
    """Executes a script designed specifically for this launcher.

       The parameter "name" is the name of the function to be tested
       which is passed as an argument to the script.
    """

    filename = os.path.join(os.path.dirname(__file__), '_launch_widget.py')
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

        # generate a bunch of function-demo buttons and output labels:
        self.button = {}
        self.setStyleSheet("""QToolTip {
                           color: black;
                           }
                           QLabel{
                           background-color: white;
                           }
                           QPushButton {
                           font-weight: bold;
                           }""")
        self.label = {}
        fxns = ['get_string', 'get_password', 'get_username_password',
                'get_int', 'get_float',
                'get_choice', 'get_list_of_choices',
                'get_yes_or_no', 'get_continue_or_cancel',
                'get_color_hex', 'get_color_rgb',
                'get_date', 'get_directory_name',
                'get_file_names', 'get_save_file_name',
                'select_language', 'set_font_size']
        for n, fxn in enumerate(fxns):
            self.button[fxn] = QtGui.QPushButton(fxn + "()")
            self.button[fxn].clicked.connect(getattr(self, fxn))
            self.button[fxn].setToolTip(getattr(easygui_qt, fxn).__doc__)
            self.label[fxn] = QtGui.QLabel()
            self.label[fxn].setFrameStyle(frameStyle)
            layout.addWidget(self.button[fxn], n, 0)
            layout.addWidget(self.label[fxn], n, 1)

        # handle special-case display items separately:
        n += 1
        self.python_version_label = QtGui.QLabel()
        layout.addWidget(self.python_version_label, n, 0, 2, 2)
        output = subprocess.check_output(
                         ['python', '-c', "import sys;print(sys.version)"])
        self.python_version_label.setText(
                                  "Python version: {}".format(output.decode()))

        n += 2
        self.cancel_btn = QtGui.QPushButton("Quit")
        self.cancel_btn.clicked.connect(self.close)
        layout.addWidget(self.cancel_btn, n, 0)

        self._layout = layout
        self.setLayout(layout)
        self.setWindowTitle("EasyGUI_Qt Widget Launcher")
        self.show()
        self.raise_()
        self.activateWindow()

    def get_string(self):
        output = launch('get_string')
        if sys.version_info < (3,):
            output = output.encode(encoding=locale.getdefaultlocale()[1])
        self.label['get_string'].setText("{}".format(output))

    def get_password(self):
        output = launch('get_password')
        if sys.version_info < (3,):
            output = output.encode(encoding=locale.getdefaultlocale()[1])
        self.label['get_password'].setText("{}".format(output))

    def get_username_password(self):
        output = launch('get_username_password')
        if sys.version_info < (3,):
            output = output.encode(encoding=locale.getdefaultlocale()[1])
        self.label['get_username_password'].setText("{}".format(output))

    def get_int(self):
        output = launch('get_int')
        self.label['get_int'].setText("{}".format(output))

    def get_float(self):
        output = launch('get_float')
        self.label['get_float'].setText("{}".format(output))

    def get_choice(self):
        output = launch('get_choice')
        self.label['get_choice'].setText("{}".format(output))

    def get_list_of_choices(self):
        output = launch('get_list_of_choices')
        self.label['get_list_of_choices'].setText("{}".format(output))

    def get_yes_or_no(self):
        output = launch('get_yes_or_no')
        self.label['get_yes_or_no'].setText("{}".format(output))

    def get_continue_or_cancel(self):
        output = launch('get_continue_or_cancel')
        self.label['get_continue_or_cancel'].setText("{}".format(output))

    def get_color_hex(self):
        color = launch('get_color_hex')
        self.label['get_color_hex'].setText(color)

    def get_color_rgb(self):
        color = launch('get_color_rgb')
        self.label['get_color_rgb'].setText(color)

    def get_date(self):
        output = launch('get_date')
        if sys.version_info < (3,):
            output = output.encode(encoding=locale.getdefaultlocale()[1])
        self.label['get_date'].setText("{}".format(output))

    def get_directory_name(self):
        output = launch('get_directory_name')
        self.label['get_directory_name'].setText("{}".format(output))

    def get_file_names(self):
        output = launch('get_file_names')
        self.label['get_file_names'].setText("{}".format(output))
        self.label['get_file_names'].setWordWrap(True)
        self.adjustSize()

    def get_save_file_name(self):
        output = launch('get_save_file_name')
        self.label['get_save_file_name'].setText("{}".format(output))

    def select_language(self):
        output = launch('select_language')
        output = output.split()[0]
        self.label['select_language'].setText("{}".format(output))

    def set_language(self):
        _loc = launch('get_string', "Enter desired language code: 'fr', 'es', etc.")
        output = launch('set_language', _loc)
        self.set_language_label.setText("{}".format(output))

    def set_font_size(self):
        font_size = launch('get_int', "Enter desired font-size.", "title",
                           "12", "10", "20")
        output = launch('set_font_size', font_size)
        output = output.split()[0]
        self.label['set_font_size'].setText("{}".format(output))


def main():
    _ = QtGui.QApplication([])
    dialog = Dialog()
    dialog.exec_()

if __name__ == '__main__':
    main()
