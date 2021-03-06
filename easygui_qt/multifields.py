import sys
from collections import OrderedDict

try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWidgets as qt_widgets

if sys.version_info >= (3,):
    unicode = str

class MultipleFieldsDialog(qt_widgets.QDialog):
    """Dialog with multiple fields stored in a dict, with the label
       being the key and the entry being the corresponding value"""
    def __init__(self, labels=None, title="Demo", masks=None, parent=None):
        super(MultipleFieldsDialog, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)

        if parent is None:
            raise Exception("Parent must be a valid object")


        self.parent = parent
        self.parent.o_dict = OrderedDict()
        self.setWindowTitle(title)

        # set up a special case for quick demo
        if labels is None:
            labels = ["Regular field", "Masked field"]
            masks = [False, True]
            self.setWindowTitle("MultipleFieldsDialog demo")

        if masks is not None:
            assert len(masks) == len(labels)

        layout = qt_widgets.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self._labels_ = []
        self.fields = []
        for index, choice in enumerate(labels):
            self._labels_.append(qt_widgets.QLabel())
            self._labels_[index].setText(choice)
            self.fields.append(qt_widgets.QLineEdit())
            self.fields[index].setText('')
            self.parent.o_dict[choice] = ''
            if masks is not None and masks[index]:
                self.fields[index].setEchoMode(qt_widgets.QLineEdit.Password)
            layout.addWidget(self._labels_[index], index, 0)
            layout.addWidget(self.fields[index], index, 1)

        button_box = qt_widgets.QDialogButtonBox()
        confirm_button = button_box.addButton(qt_widgets.QDialogButtonBox.Ok)
        layout.addWidget(button_box, index+1, 1)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def confirm(self):
        """Selection completed, set the value and close"""
        o_dict = self.parent.o_dict
        for index, item in enumerate(self._labels_):
            o_dict[unicode(item.text())] = unicode(self.fields[index].text())
        self.close()


if __name__ == '__main__':
    app = qt_widgets.QApplication([])
    class Parent:
        pass
    parent = Parent()
    dialog = MultipleFieldsDialog(parent=parent)
    dialog.exec_()
    print(parent.o_dict)