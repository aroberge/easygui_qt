'''Utily functions go here'''
import collections
import os
import sys
from PyQt4 import QtGui,  QtCore

if sys.version_info >= (3,):
    unicode = str

def find_qm_files():
    """looking for files with names == qt_locale.qm"""
    all_files = collections.OrderedDict()
    for root, _, files in os.walk(os.path.join(QtGui.__file__, "..")):
        for fname in files:
            if (fname.endswith('.qm') and fname.startswith("qt_")
                    and not fname.startswith("qt_help")):
                locale = fname[3:-3]
                all_files[locale] = root
    return all_files

def create_page(page):
    """A page is a custom layout made by stacking vertically various
       widgets which can be themselves horizontal collections of widgets

       :param page: an interable containing tuples of names of special widget
                    to position as well as their value.
       """
    new_page = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    for kind, value in page:
        if kind.lower() == "text":
            label = QtGui.QLabel(value)
            label.setWordWrap(True)
            layout.addWidget(label)
        elif kind.lower() == "image":
            label =  QtGui.QLabel()
            pixmap =  QtGui.QPixmap(value)
            label.setPixmap(pixmap)
            layout.addWidget(label)
        elif kind.lower() == "image_list":
            h_layout = QtGui.QHBoxLayout()
            h_box = QtGui.QGroupBox('')
            for image in value:
                label =  QtGui.QLabel()
                pixmap =  QtGui.QPixmap(image)
                label.setPixmap(pixmap)
                h_layout.addWidget(label)
            h_box.setLayout(h_layout)
            layout.addWidget(h_box)
    new_page.setLayout(layout)
    return new_page


class MyPageDialog(QtGui.QDialog):
    """docstring to be added """
    def __init__(self, title="title", page=None):
        super(MyPageDialog, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(title)
        if page is None:
            raise AttributeError

        layout = QtGui.QVBoxLayout()

        widget = create_page(page)
        layout.addWidget(widget)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    page = [("text", "This is a sample text"),
         ("image", "../ignore/images/python.jpg"),
         ("text", "More text")]
    dialog = MyPageDialog(title="Hello World", page=page)
    dialog.exec_()
    app.quit()

