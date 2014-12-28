from PyQt4 import QtGui


def get_string(prompt="What is your name? ", title="Title",
               default_response="PyQt4", app=None):
    """GUI equivalent of input()."""

    if app is None:
        app = QtGui.QApplication([])
    app.dialog = QtGui.QInputDialog()
    text, ok = app.dialog.getText(None, title, prompt,
                                  QtGui.QLineEdit.Normal,
                                  default_response)
    app.quit()
    if ok:
        return text

if __name__ == '__main__':
    print(get_string())
    app2 = QtGui.QApplication([])
    print(get_string(app=app2))
