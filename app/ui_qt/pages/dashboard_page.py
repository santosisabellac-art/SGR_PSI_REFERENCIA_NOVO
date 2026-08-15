from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.dashboard_service import DashboardService


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = DashboardService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Dashboard Operacional")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.clicked.connect(self.atualizar_dashboard)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(botao_atualizar)

        layout.addLayout(cabecalho)

        subtitulo = QLabel(
            "Prioridades para acompanhar no trabalho de hoje."
        )
        subtitulo.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitulo)

        cards = QHBoxLayout()

        _, self.total_aprendizes = self.criar_card(
            cards,
            "Aprendizes ativos",
        )
        _, self.total_pendencias = self.criar_card(
            cards,
            "Pendências abertas",
        )
        _, self.total_documentos = self.criar_card(
            cards,
            "Documentos pendentes",
        )
        _, self.total_vencidos = self.criar_card(
            cards,
            "Documentos vencidos",
        )

        layout.addLayout(cards)

        titulo_prioridades = QLabel("Prioridades")
        titulo_prioridades.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(titulo_prioridades)

        self.tabela_prioridades = QTableWidget()
        self.tabela_prioridades.setColumnCount(3)
        self.tabela_prioridades.setHorizontalHeaderLabels(
            ["Tipo", "Aprendiz", "Detalhe"]
        )
        self.tabela_prioridades.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tabela_prioridades.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.tabela_prioridades.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.tabela_prioridades.setMinimumHeight(210)

        layout.addWidget(self.tabela_prioridades)

        titulo_alertas = QLabel("Alertas de cadastro")
        titulo_alertas.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(titulo_alertas)

        self.lista_alertas = QListWidget()
        self.lista_alertas.setMaximumHeight(160)
        layout.addWidget(self.lista_alertas)

        self.atualizar_dashboard()

    def criar_card(self, layout, titulo):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)

        titulo_card = QLabel(titulo)
        titulo_card.setFont(QFont("Segoe UI", 11, QFont.Bold))

        quantidade = QLabel("0")
        quantidade.setFont(QFont("Segoe UI", 28, QFont.Bold))

        card_layout.addWidget(titulo_card)
        card_layout.addWidget(quantidade)

        layout.addWidget(card)

        return card, quantidade

    def atualizar_dashboard(self):
        dados = self.service.resumo()

        self.total_aprendizes.setText(str(dados["total_aprendizes"]))
        self.total_pendencias.setText(
            str(dados["total_pendencias_abertas"])
        )
        self.total_documentos.setText(
            str(dados["total_documentos_pendentes"])
        )
        self.total_vencidos.setText(
            str(dados["total_documentos_vencidos"])
        )

        prioridades = dados["prioridades"]
        self.tabela_prioridades.setRowCount(len(prioridades))

        for linha, prioridade in enumerate(prioridades):
            valores = [
                prioridade["prioridade"],
                prioridade["aprendiz"],
                prioridade["detalhe"],
            ]

            for coluna, valor in enumerate(valores):
                self.tabela_prioridades.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor),
                )

        self.lista_alertas.clear()

        alertas = dados["alertas"]
        if alertas:
            self.lista_alertas.addItems(alertas)
        else:
            self.lista_alertas.addItem("Nenhum alerta de cadastro.")
