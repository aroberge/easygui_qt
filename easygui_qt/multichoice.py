
import sys

try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWidgets as qt_widgets

class MultipleChoicesDialog(qt_widgets.QDialog):
    """Dialog with the possibility of selecting one or more
       items from a list"""
    def __init__(self, choices=None, title="Title"):
        super(MultipleChoicesDialog, self).__init__(None, QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        if choices is None:
            choices = ["Item %d"%i for i in range(10)]
        self.setWindowTitle(title)
        self.selection = []

        main_widget = qt_widgets.QWidget()
        main_layout = qt_widgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.choices_widget = qt_widgets.QListWidget()
        self.choices_widget.setSelectionMode(
                                    qt_widgets.QAbstractItemView.ExtendedSelection)
        for choice in choices:
            item = qt_widgets.QListWidgetItem()
            item.setText(choice)
            self.choices_widget.addItem(item)
        main_layout.addWidget(self.choices_widget)

        button_box_layout = qt_widgets.QGridLayout()
        selection_completed_btn = qt_widgets.QPushButton("Ok")
        selection_completed_btn.clicked.connect(self.selection_completed)
        select_all_btn = qt_widgets.QPushButton("Select all")
        select_all_btn.clicked.connect(self.select_all)
        clear_all_btn = qt_widgets.QPushButton("Clear all")
        clear_all_btn.clicked.connect(self.clear_all)
        cancel_btn = qt_widgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)

        button_box = qt_widgets.QWidget()
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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.cancel()
        elif e.key() == QtCore.Qt.Key_Enter:
            self.selection_completed()
        else:
            super(MultipleChoicesDialog, self).keyPressEvent(e)

if __name__ == '__main__':
    app = qt_widgets.QApplication([])
    dialog = MultipleChoicesDialog()
    dialog.exec_()
    if sys.version_info < (3,):
        print([unicode(item) for item in dialog.selection])
    print(dialog.selection)