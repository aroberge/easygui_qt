'''Utily functions go here'''
import collections
import os
import sys

try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWidgets as qt_widgets

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

def create_page(page, parent=None):
    """A page is a custom layout made by stacking vertically various
       widgets which can be themselves horizontal collections of widgets

       :param page: an interable containing tuples of names of special widget
                    to position as well as their value.
       """
    new_page = qt_widgets.QWidget()
    layout = qt_widgets.QVBoxLayout()
    for kind, value in page:
        if kind.lower() == "text":
            add_text_to_layout(layout, value)
        elif kind.lower() == "image":
            add_image_to_layout(layout, value)
        elif kind.lower() == "list of images":
            add_list_of_images_to_layout(layout, value)
        elif kind.lower() == "list of images with captions":
            add_list_of_images_with_captions_to_layout(layout, value)
        elif kind.lower() == "list of images with buttons":
            add_list_of_images_with_buttons_to_layout(layout, value, parent)
        elif kind.lower() == "list of buttons":
            add_list_of_buttons_to_layout(layout, value, parent)
        elif kind.lower() == "button":
            add_button(layout, value, parent)
        else:
            print("Unrecognized page item: {}".format(kind))
    new_page.setLayout(layout)
    return new_page


def add_text_to_layout(layout, text):
    '''adds some text, as a QLabel, to a layout'''
    label = qt_widgets.QLabel(text)
    label.setWordWrap(True)
    layout.addWidget(label)

def add_image_to_layout(layout, image_file_name):
    '''adds an image, as a QLabel, to a layout'''
    label =  qt_widgets.QLabel()
    pixmap =  QtGui.QPixmap(image_file_name)
    label.setPixmap(pixmap)
    layout.addWidget(label)

def add_list_of_images_to_layout(layout, images):
    ''' adds a list of images shown in a horizontal layout to an
        already existing layout'''
    h_layout = qt_widgets.QHBoxLayout()
    h_box = qt_widgets.QGroupBox('')
    for image in images:
        add_image_to_layout(h_layout, image)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)

def add_list_of_images_with_captions_to_layout(layout, images):
    ''' adds a list of images shown in a horizontal layout with
        caption underneath to an already existing layout'''
    h_layout = qt_widgets.QHBoxLayout()
    h_box = qt_widgets.QGroupBox('')
    for image, caption in images:
        widget = qt_widgets.QWidget()
        v_layout = qt_widgets.QVBoxLayout()
        add_image_to_layout(v_layout, image)
        add_text_to_layout(v_layout, caption)
        widget.setLayout(v_layout)
        h_layout.addWidget(widget)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)

def add_list_of_images_with_buttons_to_layout(layout, images, parent):
    ''' adds a list of images shown in a horizontal layout with
        button underneath to an already existing layout'''
    h_layout = qt_widgets.QHBoxLayout()
    h_box = qt_widgets.QGroupBox('')
    for image, label in images:
        widget = qt_widgets.QWidget()
        v_layout = qt_widgets.QVBoxLayout()
        add_image_to_layout(v_layout, image)
        add_button(v_layout, label, parent)
        widget.setLayout(v_layout)
        h_layout.addWidget(widget)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)

def add_list_of_buttons_to_layout(layout, button_labels, parent):
    ''' adds a list of buttons shown in a horizontal layout to an
        already existing layout'''
    h_layout = qt_widgets.QHBoxLayout()
    h_box = qt_widgets.QGroupBox('')
    for label in button_labels:
        add_button(h_layout, label, parent)
    h_box.setLayout(h_layout)
    layout.addWidget(h_box)

def add_button(layout, label, parent):
    btn = qt_widgets.QPushButton(label)
    btn.clicked.connect(parent.button_clicked)
    width = btn.fontMetrics().boundingRect(label).width() + 15
    btn.setMaximumWidth(width)
    layout.addWidget(btn)


class MyPageDialog(qt_widgets.QDialog):
    """Creates a "complex" dialog based on a description as a "page"."""
    def __init__(self, title="title", page=None, response=None):
        super(MyPageDialog, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(title)
        if page is None:
            raise AttributeError
        self.response = response

        layout = qt_widgets.QVBoxLayout()
        widget = create_page(page, parent=self)
        layout.addWidget(widget)
        self.setLayout(layout)

    def button_clicked(self):
        sender = self.sender()
        self.response.append(sender.text())
        self.close()


if __name__ == '__main__':
    app = qt_widgets.QApplication([])
    page = [("text", "This is a sample text"),
            ("image", "../ignore/images/python.jpg"),
            ("text", "More text"),
            ("button", "button"),
            ("button", "button 2"),
            ("list of images with captions",
                 [("../ignore/images/python.jpg", "caption"),
                  ("../ignore/images/reeborg.png", "a much longer caption"),
                  ("../ignore/images/python.jpg", "yet another long caption")
                  ]),
            ("list of images with buttons",
                 [("../ignore/images/python.jpg", "button"),
                  ("../ignore/images/python.jpg", "another button"),
                  ("../ignore/images/python.jpg", "a button with longer label")
                  ]),
            ("list of images", ["../ignore/images/python.jpg",
                                "../ignore/images/python.jpg",
                                "../ignore/images/python.jpg"]),
            ("list of buttons", ["button A",
                                "buttton B",
                                "button C",
                                "button D",
                                "button E"])
           ]
    response = []
    dialog = MyPageDialog(title="Hello World", page=page, response=response)
    dialog.exec_()
    app.quit()
    print(response)

