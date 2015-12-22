

import sys
try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PyQt5 import QtGui, QtCore  # untested

class MultipleChoicesDialog(QtGui.QDialog):
    """Dialog with the possibility of selecting one or more
       items from a list"""
    def __init__(self, choices=None, title="Title"):
        super(MultipleChoicesDialog, self).__init__(None, QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        if choices is None:
            choices = ["Item %d"%i for i in range(10)]
        self.setWindowTitle(title)
        self.selection = []

        main_widget = QtGui.QWidget()
        main_layout = QtGui.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.choices_widget = QtGui.QListWidget()
        self.choices_widget.setSelectionMode(
                                    QtGui.QAbstractItemView.ExtendedSelection)
        for choice in choices:
            item = QtGui.QListWidgetItem()
            item.setText(choice)
            self.choices_widget.addItem(item)
        main_layout.addWidget(self.choices_widget)

        button_box_layout = QtGui.QGridLayout()
        selection_completed_btn = QtGui.QPushButton("Ok")
        selection_completed_btn.clicked.connect(self.selection_completed)
        select_all_btn = QtGui.QPushButton("Select all")
        select_all_btn.clicked.connect(self.select_all)
        clear_all_btn = QtGui.QPushButton("Clear all")
        clear_all_btn.clicked.connect(self.clear_all)
        cancel_btn = QtGui.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)

        button_box = QtGui.QWidget()
        button_box_layout.addWidget(selection_completed_btn, 0, 0)
        button_box_layout.addWidget(cancel_btn, 0, 1)
        button_box_layout.addWidget(select_all_btn, 1, 0)
        button_box_layout.addWidget(clear_all_btn, 1, 1)
        button_box.setLayout(button_box_layout)

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.show()
        self.raise_()

    def selection_completed(self):
        """Selection completed, set the value and close"""
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]
        self.close()

    def select_all(self):
        """Set all possible values as selected"""
        self.choices_widget.selectAll()
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]

    def clear_all(self):
        """Reset to have no selected values"""
        self.choices_widget.clearSelection()
        self.selection = []

    def cancel(self):
        """cancel and set the selection to an empty list"""
        self.selection = []
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    dialog = MultipleChoicesDialog()
    dialog.exec_()
    if sys.version_info < (3,):
        print([unicode(item) for item in dialog.selection])
    print(dialog.selection)