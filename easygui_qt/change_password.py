import sys
from collections import OrderedDict
from PyQt4 import QtGui, QtCore

if sys.version_info >= (3,):
    unicode = str


class ChangePassword(QtGui.QDialog):
    """A specially constructed two-field dialog to get a user's name (shown)
    and password (masked).  This user should provide a
    """
    def __init__(self, parent, title="User name and password",
                 verification=None):
        super(ChangePassword, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)

        if verification == "demo":
            self.verification = self.demo_verification
        else:
            self.verification = verification

        self.parent = parent
        self.keys = [key for key in self.parent.o_dict.keys()]

        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self.old_password_label = QtGui.QLabel()
        self.old_password_label.setText(self.keys[0])
        self.old_password_field = QtGui.QLineEdit()
        self.old_password_field.setEchoMode(QtGui.QLineEdit.Password)
        layout.addWidget(self.old_password_label, 0, 0)
        layout.addWidget(self.old_password_field, 0, 1)

        self.new_password_label = QtGui.QLabel()
        self.new_password_label.setText(self.keys[1])
        self.new_password_field = QtGui.QLineEdit()
        self.new_password_field.setEchoMode(QtGui.QLineEdit.Password)
        layout.addWidget(self.new_password_label, 1, 0)
        layout.addWidget(self.new_password_field, 1, 1)

        self.new_password2_label = QtGui.QLabel()
        self.new_password2_label.setText(self.keys[2])
        self.new_password2_field = QtGui.QLineEdit()
        self.new_password2_field.setEchoMode(QtGui.QLineEdit.Password)
        layout.addWidget(self.new_password2_label, 2, 0)
        layout.addWidget(self.new_password2_field, 2, 1)

        button_box = QtGui.QDialogButtonBox()
        confirm_button = button_box.addButton(QtGui.QDialogButtonBox.Ok)
        layout.addWidget(button_box, 3, 1)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def confirm(self):
        """Callback from confirm_button"""
        o_dict = self.parent.o_dict
        o_dict[self.keys[0]] = unicode(self.old_password_field.text())
        o_dict[self.keys[1]] = unicode(self.new_password_field.text())
        o_dict[self.keys[2]] = unicode(self.new_password2_field.text())
        if self.verification is None:   # no verification
            self.close()
        elif self.verification(self) is None:    # no error raised
            self.close()
        else:
            o_dict[self.keys[0]] = ''
            o_dict[self.keys[1]] = ''
            o_dict[self.keys[2]] = ''
            self.close()


    def demo_verification(self, dummy=None):
        """Silly demo of a verification function.  It requires that the
           original password be "password" and that the two new passwords
           be identical.
        """
        if dummy is not None:
            dummy = self
        message = None
        o_dict = self.parent.o_dict
        if o_dict[self.keys[0]] != "password":
            message = ("Original password does not match expected value " +
                       "[Hint: it's 'password']")
            self.show_message(message)
        elif o_dict[self.keys[1]] != o_dict[self.keys[2]]:
            message = "New password values must be identical."
            self.show_message(message)
        return message

    def show_message(self, message):
        QtGui.QMessageBox.critical(None, ' ', message)


def custom_verification(self):
    message = None
    o_dict = self.parent.o_dict
    for key in self.keys:
        if o_dict[key] != "Python":
            message = "All three fields must be set to 'Python' in this demo"
            break
    return message

if __name__ == '__main__':
    app = QtGui.QApplication([])
    # mocks
    class Parent:
        o_dict = OrderedDict()
        o_dict["Old password:"] = ''
        o_dict["New password:"] = ''
        o_dict["Confirm new password:"] = ''

    ChangePassword.show_message(None, "4 silly demos in a row")

    parent = Parent()
    change = ChangePassword(parent, title="Demo verification",
                            verification="demo")
    change.exec_()
    print(parent.o_dict)

    parent = Parent()
    change = ChangePassword(parent, title="Demo verification",
                            verification="demo")
    change.exec_()
    print(parent.o_dict)

    parent = Parent()
    change = ChangePassword(parent, title="No verification done!!")
    change.exec_()
    print(parent.o_dict)

    parent = Parent()
    change = ChangePassword(parent, verification=custom_verification,
                            title="Silly custom verification")
    change.exec_()
    print(parent.o_dict)

    app.quit()
