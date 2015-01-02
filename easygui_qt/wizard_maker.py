
from PyQt4 import QtGui, QtCore

class WizardCreator(QtGui.QWizard):
    def __init__(self, title="Title", pages=[]):
        super(WizardCreator, self).__init__(None,
              QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(title)
        for page in pages:
            self.create_page(page)
        self.show()

    def create_page(self, page):
        new_page = QtGui.QWizardPage()
        layout = QtGui.QVBoxLayout()
        for kind, value in page:
            if kind.lower() == "title":
                new_page.setTitle(value)
            elif kind.lower() == "text":
                label = QtGui.QLabel(value)
                label.setWordWrap(True)
                layout.addWidget(label)
            elif kind.lower() == "image":
                label =  QtGui.QLabel()
                pixmap =  QtGui.QPixmap(value)
                label.setPixmap(pixmap)
                layout.addWidget(label)
        new_page.setLayout(layout)
        self.addPage(new_page)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    page1 = [("text", "This is a sample text"),
             ("image", "../ignore/images/python.jpg"),
             ("text", "More text")]
    page2 = [("text", "This is a sample text"),
             ("image", "../images/contribute.png"),
             ("text", "More text")]
    page3 = [("text", "This is another sample text"),
             ("title", "This page has its own (sub) title")]

    pages = [page1, page2, page3]
    wizard = WizardCreator(title="Hello World", pages=pages)
    wizard.exec_()
    app.quit()

