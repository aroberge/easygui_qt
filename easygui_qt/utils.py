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
            add_text_to_layout(layout, value)
        elif kind.lower() == "image":
            add_image_to_layout(layout, value)
        elif kind.lower() == "list of images":
            add_list_of_images_to_layout(layout, value)
        elif kind.lower() == "list of images with captions":
            add_list_of_images_with_captions_to_layout(layout, value)
        else:
            print("Unrecognized page item: {}".format(kind))
    new_page.setLayout(layout)
    return new_page


def add_text_to_layout(layout, text):
    '''adds some text, as a QLabel, to a layout'''
    label = QtGui.QLabel(text)
    label.setWordWrap(True)
    layout.addWidget(label)

def add_image_to_layout(layout, image_file_name):
    '''adds an image, as a QLabel, to a layout'''
    label =  QtGui.QLabel()
    pixmap =  QtGui.QPixmap(image_file_name)
    label.setPixmap(pixmap)
    layout.addWidget(label)

def add_list_of_images_to_layout(layout, images):
    ''' adds a list of images shown in a horizontal layout to an
        already existing layout'''
    h_layout = QtGui.QHBoxLayout()
    h_box = QtGui.QGroupBox('')
    for image in images:
        add_image_to_layout(h_layout, image)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)

def add_list_of_images_with_captions_to_layout(layout, images):
    ''' adds a list of images shown in a horizontal layout with
        caption underneath to an already existing layout'''
    h_layout = QtGui.QHBoxLayout()
    h_box = QtGui.QGroupBox('')
    for image, caption in images:
        widget = QtGui.QWidget()
        v_layout = QtGui.QVBoxLayout()
        add_image_to_layout(v_layout, image)
        add_text_to_layout(v_layout, caption)
        widget.setLayout(v_layout)
        h_layout.addWidget(widget)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)


class MyPageDialog(QtGui.QDialog):
    """Creates a "complex" dialog based on a description as a "page"."""
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
            ("text", "More text"),
            ("list of images with captions",
                 [("../ignore/images/python.jpg", "caption"),
                  ("../ignore/images/python.jpg", "a much longer caption"),
                  ("../ignore/images/python.jpg", "yet another long caption")
                  ]),
            ("list of images", ["../ignore/images/python.jpg",
                                "../ignore/images/python.jpg",
                                "../ignore/images/python.jpg"])
           ]
    dialog = MyPageDialog(title="Hello World", page=page)
    dialog.exec_()
    app.quit()

