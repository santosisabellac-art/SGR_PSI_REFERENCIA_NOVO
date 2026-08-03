import sys

print("1 - Arquivo iniciado")

from PySide6.QtWidgets import QApplication

print("2 - QApplication importada")

from app.ui_qt.main_window import MainWindow

print("3 - MainWindow importada")


def main():
    print("4 - Entrou na função main")

    app = QApplication(sys.argv)
    print("5 - QApplication criada")

    window = MainWindow()
    print("6 - MainWindow criada")

    window.show()
    print("7 - show() executado")

    resultado = app.exec()

    print("8 - Aplicação encerrada")

    sys.exit(resultado)


if __name__ == "__main__":
    print("9 - Executando main")
    main()