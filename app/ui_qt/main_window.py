from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from app.ui_qt.components.sidebar import Sidebar
from app.ui_qt.pages.home_page import HomePage
from app.ui_qt.pages.aprendizes_page import AprendizesPage
from app.ui_qt.theme.theme import Theme


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SGR - Psicóloga de Referência")
        self.resize(
            Theme.WINDOW_WIDTH,
            Theme.WINDOW_HEIGHT,
        )

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Menu lateral
        self.sidebar = Sidebar()

        # Área de páginas
        self.stack = QStackedWidget()

        self.home = HomePage()
        self.aprendizes = AprendizesPage()

        self.stack.addWidget(self.home)         # índice 0
        self.stack.addWidget(self.aprendizes)   # índice 1

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        # Conecta o clique do menu
        self.sidebar.pagina_selecionada.connect(self.trocar_pagina)

    def trocar_pagina(self, pagina):

        if pagina == "home":
            self.stack.setCurrentIndex(0)

        elif pagina == "aprendizes":
            self.stack.setCurrentIndex(1)