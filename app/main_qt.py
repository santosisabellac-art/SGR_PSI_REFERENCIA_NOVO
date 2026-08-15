import sys

from PySide6.QtWidgets import QApplication

from app.database.database import criar_banco
from app.ui_qt.main_window import MainWindow


def main():
    criar_banco()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
