import sys

from PySide6.QtWidgets import QApplication, QLabel


app = QApplication(sys.argv)

label = QLabel("PySide6 funcionando!")

label.resize(400, 120)

label.show()

app.exec()