
try:
    from PyQt4 import QtGui, QtCore
    qt_widgets = QtGui
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWidgets as qt_widgets

class WizardCreator(qt_widgets.QWizard):
    def __init__(self, title="Title", pages=[]):
        super(WizardCreator, self).__init__(None,
              QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(title)
        for page in pages:
            self.create_page(page)
        self.show()

    def create_page(self, page):
        new_page = qt_widgets.QWizardPage()
        layout = qt_widgets.QVBoxLayout()
        for kind, value in page:
            if kind.lower() == "title":
                new_page.setTitle(value)
            elif kind.lower() == "text":
                label = qt_widgets.QLabel(value)
                label.setWordWrap(True)
                layout.addWidget(label)
            elif kind.lower() == "image":
                label =  qt_widgets.QLabel()
                pixmap =  QtGui.QPixmap(value)
                label.setPixmap(pixmap)
                layout.addWidget(label)
            elif kind.lower() == "many images":
                h_layout = qt_widgets.QHBoxLayout()
                h_box = qt_widgets.QGroupBox('')
                for image in value:
                    label =  qt_widgets.QLabel()
                    pixmap =  QtGui.QPixmap(image)
                    label.setPixmap(pixmap)
                    h_layout.addWidget(label)
                h_box.setLayout(h_layout)
                layout.addWidget(h_box)
        new_page.setLayout(layout)
        self.addPage(new_page)

if __name__ == '__main__':
    app = qt_widgets.QApplication([])
    page1 = [("text", "This is a sample text"),
             ("image", "../ignore/images/python.jpg"),
             ("text", "More text")]
    page2 = [("text", "This is a sample text"),
             ("image", "../images/contribute.png"),
             ("text", "More text")]
    page3 = [("text", "This is another sample text"),
             ("title", "This page has its own (sub) title")]
    page4 = [("many images", ["../ignore/images/python.jpg",
                               "../ignore/images/reeborg.png"])]
    page5 = [("text", "This is a sample text"),
             ("many images", ("../images/contribute.png",
                              "../images/contribute.png")),
             ("text", "More text")]
    pages = [page1, page2, page3, page4, page5]
    wizard = WizardCreator(title="Hello World", pages=pages)
    wizard.exec_()
    app.quit()

