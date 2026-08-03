from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.aprendiz_service import AprendizService
from app.ui_qt.dialogs.aprendiz_dialog import AprendizDialog


class AprendizesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = AprendizService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # ===========================
        # Cabeçalho
        # ===========================

        cabecalho = QHBoxLayout()

        titulo = QLabel("Aprendizes")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.botao_novo = QPushButton("➕ Novo Aprendiz")
        self.botao_novo.setMinimumHeight(40)
        self.botao_novo.clicked.connect(self.abrir_dialog)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_novo)

        layout.addLayout(cabecalho)

        subtitulo = QLabel(
            "Gerencie os aprendizes da sua referência."
        )

        subtitulo.setStyleSheet("color:#6B7280;")

        layout.addWidget(subtitulo)

        layout.addSpacing(20)

        # ===========================
        # Tabela
        # ===========================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(5)

        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Código",
            "Nível",
            "Sala",
            "Status",
        ])

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.tabela.setAlternatingRowColors(True)

        layout.addWidget(self.tabela)

        self.carregar_aprendizes()

    # =====================================

    def carregar_aprendizes(self):

        aprendizes = self.service.listar()

        self.tabela.setRowCount(len(aprendizes))

        for linha, aprendiz in enumerate(aprendizes):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(aprendiz.nome),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(aprendiz.codigo),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(aprendiz.nivel_suporte),
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(aprendiz.sala or ""),
            )

            self.tabela.setItem(
                linha,
                4,
                QTableWidgetItem(aprendiz.status),
            )

    # =====================================

    def abrir_dialog(self):

        dialog = AprendizDialog(self)

        if dialog.exec():

            self.carregar_aprendizes()