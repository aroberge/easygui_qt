import sys
from collections import OrderedDict
from PyQt4 import QtGui, QtCore

if sys.version_info >= (3,):
    unicode = str


class UserNamePassword(QtGui.QDialog):
    """A specially constructed two-field dialog to get a user's name (shown)
    and password (masked).
    """
    def __init__(self, parent, title="User name and password"):
        super(UserNamePassword, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)

        self.parent = parent
        self.keys = [key for key in self.parent.o_dict.keys()]

        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self.user_name_label = QtGui.QLabel()
        self.user_name_label.setText(self.keys[0])
        self.user_name_field = QtGui.QLineEdit()
        layout.addWidget(self.user_name_label, 0, 0)
        layout.addWidget(self.user_name_field, 0, 1)

        self.password_label = QtGui.QLabel()
        self.password_label.setText(self.keys[1])
        self.password_field = QtGui.QLineEdit()
        self.password_field.setEchoMode(QtGui.QLineEdit.Password)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_field, 1, 1)

        button_box = QtGui.QDialogButtonBox()
        confirm_button = button_box.addButton(QtGui.QDialogButtonBox.Ok)
        layout.addWidget(button_box, 2, 1)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def confirm(self):
        """Callback from confirm_button"""
        self.parent.o_dict[self.keys[0]] = unicode(self.user_name_field.text())
        self.parent.o_dict[self.keys[1]] = unicode(self.password_field.text())
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    # mocks
    class Parent:
        o_dict = OrderedDict()
    parent = Parent()
    parent.o_dict["User name:"] = ''
    parent.o_dict["Password:"] = ''

    selector = UserNamePassword(parent)
    selector.exec_()
    app.quit()
    print(parent.o_dict)