
from PyQt4.QtGui import QApplication, QLabel, QPixmap

app = QApplication([])

label = QLabel()
pixmap = QPixmap("images/reeborg.png")
label.setPixmap(pixmap)
label.move(10, 10)
label.show()

label2 = QLabel()
pixmap = QPixmap("images/python.jpg")
label2.setPixmap(pixmap)
label2.move(200, 10)
label2.show()

app.exec_()

app.quit()
