
try:
    from . import utils
except:
    import utils

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PyQt5 import QtGui, QtCore  # untested

class LanguageSelector(QtGui.QDialog):
    """A specially constructed dialog which uses informations about
       available language (qm) files which can be used to change the
       default language of the basic PyQt ui components.
    """

    def __init__(self, parent, title="Language selection",
                 name="Language codes",
                 instruction="Click button when you are done"):
        super(LanguageSelector, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        self.qm_files_choices = {}
        self.parent = parent
        qm_files = utils.find_qm_files()

        # ========= check boxes ==============
        group_box = QtGui.QGroupBox(name)
        group_box_layout = QtGui.QGridLayout()
        for i, locale in enumerate(qm_files):
            check_box = QtGui.QCheckBox(locale)
            check_box.setAutoExclusive(True)
            self.qm_files_choices[check_box] = locale
            check_box.toggled.connect(self.check_box_toggled)
            group_box_layout.addWidget(check_box, i / 4, i % 4)
        # adding default language option. When using the PyQt distribution
        # no "en" files were found and yet "en" was the obvious default.
        # We need this option in case we want to revert a change.
        check_box = QtGui.QCheckBox("default")
        check_box.setAutoExclusive(True)
        self.qm_files_choices[check_box] = "default"
        check_box.toggled.connect(self.check_box_toggled)
        i = len(qm_files)
        group_box_layout.addWidget(check_box, i / 4, i % 4)
        group_box.setLayout(group_box_layout)

        # ========= buttons ==============
        button_box = QtGui.QDialogButtonBox()
        confirm_button = button_box.addButton(QtGui.QDialogButtonBox.Ok)
        confirm_button.clicked.connect(self.confirm)

        # ========= finalizing layout ====
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(group_box)
        main_layout.addWidget(QtGui.QLabel(instruction))
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def check_box_toggled(self):
        """Callback when a checkbox is toggled"""
        self.locale = self.qm_files_choices[self.sender()]

    def confirm(self):
        """Callback from confirm_button used to set the locale"""
        if self.locale != self.parent.config['locale']:
            self.parent.set_locale(self.locale)
        print(self.locale)  # feedback to launcher
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    # mocks
    app.config = {'locale': None}
    app.set_locale = lambda x: x
    #
    selector = LanguageSelector(app, title="title")
    selector.exec_()
    app.quit()