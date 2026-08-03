from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):

    pagina_selecionada = Signal(str)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(240)

        self.setStyleSheet("""
            QWidget{
                background:#F8F9FC;
                border-right:1px solid #DDDDDD;
            }

            QPushButton{

                border:none;
                text-align:left;

                padding:10px;

                font-size:13px;

            }

            QPushButton:hover{

                background:#E8EEFF;

            }

        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20,20,20,20)

        titulo = QLabel("SGR")

        titulo.setFont(QFont("Segoe UI",22,QFont.Bold))

        titulo.setStyleSheet("""
            color:#2F5BEA;
        """)

        layout.addWidget(titulo)

        layout.addSpacing(30)

        self.criar_botao(layout,"home","🏠  Início")

        self.criar_botao(layout,"aprendizes","👤  Aprendizes")

        self.criar_botao(layout,"agenda","📅  Agenda")

        self.criar_botao(layout,"documentos","📄  Documentos")

        self.criar_botao(layout,"dashboard","📊  Dashboard")

        self.criar_botao(layout,"configuracoes","⚙  Configurações")

        layout.addStretch()

    def criar_botao(self,layout,pagina,texto):

        botao = QPushButton(texto)

        botao.clicked.connect(

            lambda _, p=pagina:

            self.pagina_selecionada.emit(p)

        )

        layout.addWidget(botao)