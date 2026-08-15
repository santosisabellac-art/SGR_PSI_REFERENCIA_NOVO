from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from app.ui_qt.components.sidebar import Sidebar
from app.ui_qt.pages.agenda_page import AgendaPage
from app.ui_qt.pages.home_page import HomePage
from app.ui_qt.pages.aprendizes_page import AprendizesPage
from app.ui_qt.pages.configuracoes_page import ConfiguracoesPage
from app.ui_qt.pages.dashboard_page import DashboardPage
from app.ui_qt.pages.documentos_page import DocumentosPage
from app.ui_qt.pages.painel_360_documento_page import Painel360DocumentoPage
from app.ui_qt.theme.theme import Theme


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SGR - Psicóloga de Referência")
        self.resize(Theme.WINDOW_WIDTH, Theme.WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.stack = QStackedWidget()

        self.home = HomePage()
        self.aprendizes = AprendizesPage()
        self.agenda = AgendaPage()
        self.documentos = DocumentosPage()
        self.dashboard = DashboardPage()
        self.configuracoes = ConfiguracoesPage()
        self.painel_360 = None

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.aprendizes)
        self.stack.addWidget(self.agenda)
        self.stack.addWidget(self.documentos)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.configuracoes)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.sidebar.pagina_selecionada.connect(self.trocar_pagina)
        self.aprendizes.painel_solicitado.connect(self.abrir_painel_360)

    def trocar_pagina(self, pagina):
        if pagina == "home":
            self.stack.setCurrentWidget(self.home)
        elif pagina == "aprendizes":
            self.aprendizes.carregar_aprendizes()
            self.stack.setCurrentWidget(self.aprendizes)
        elif pagina == "agenda":
            self.agenda.carregar_agenda()
            self.stack.setCurrentWidget(self.agenda)
        elif pagina == "documentos":
            self.documentos.carregar_documentos()
            self.stack.setCurrentWidget(self.documentos)
        elif pagina == "dashboard":
            self.dashboard.atualizar_dashboard()
            self.stack.setCurrentWidget(self.dashboard)
        elif pagina == "configuracoes":
            self.configuracoes.carregar_backups()
            self.stack.setCurrentWidget(self.configuracoes)

    def abrir_painel_360(self, aprendiz):
        if self.painel_360 is not None:
            self.stack.removeWidget(self.painel_360)
            self.painel_360.deleteLater()

        self.painel_360 = Painel360DocumentoPage(aprendiz)
        self.painel_360.aprendiz_atualizado.connect(
            self.aprendizes.carregar_aprendizes
        )

        self.stack.addWidget(self.painel_360)
        self.stack.setCurrentWidget(self.painel_360)
