from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.services.dashboard_service import DashboardService


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        self.dashboard = DashboardService()

        dados = self.dashboard.resumo()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        titulo = QLabel("Bem-vinda, Isabella 👋")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        subtitulo = QLabel(
            "Sistema de Gestão da Psicóloga de Referência"
        )
        subtitulo.setStyleSheet("color:#6B7280;")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # ------------------------
        # CARD APRENDIZES
        # ------------------------

        card = QFrame()
        card.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:12px;
            }
        """)

        card_layout = QVBoxLayout(card)

        titulo_card = QLabel("👥 Aprendizes Ativos")
        titulo_card.setFont(QFont("Segoe UI", 12, QFont.Bold))

        quantidade = QLabel(
            str(dados["total_aprendizes"])
        )

        quantidade.setFont(
            QFont("Segoe UI", 34, QFont.Bold)
        )

        quantidade.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(titulo_card)
        card_layout.addWidget(quantidade)

        layout.addWidget(card)

        # ------------------------
        # CARD PENDÊNCIAS
        # ------------------------

        pendencias = QFrame()

        pendencias.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:12px;
            }
        """)

        pendencias_layout = QVBoxLayout(pendencias)

        titulo_pendencias = QLabel("📋 Pendências Abertas")
        titulo_pendencias.setFont(QFont("Segoe UI", 12, QFont.Bold))

        quantidade_pendencias = QLabel(
            str(dados["total_pendencias_abertas"])
        )

        quantidade_pendencias.setFont(
            QFont("Segoe UI", 34, QFont.Bold)
        )

        quantidade_pendencias.setAlignment(Qt.AlignCenter)

        pendencias_layout.addWidget(titulo_pendencias)
        pendencias_layout.addWidget(quantidade_pendencias)

        if dados["pendencias_abertas"]:

            for pendencia in dados["pendencias_abertas"]:

                pendencias_layout.addWidget(
                    QLabel(
                        f'• {pendencia["aprendiz"]} — '
                        f'{pendencia["titulo"]}'
                    )
                )

        else:

            pendencias_layout.addWidget(
                QLabel("Nenhuma pendência aberta.")
            )

        layout.addWidget(pendencias)

        # ------------------------
        # AGENDA
        # ------------------------

        agenda = QFrame()

        agenda.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:12px;
            }
        """)

        agenda_layout = QVBoxLayout(agenda)

        titulo_agenda = QLabel("📅 Agenda")
        titulo_agenda.setFont(
            QFont("Segoe UI", 12, QFont.Bold)
        )

        agenda_layout.addWidget(titulo_agenda)

        if dados["agenda"]:

            for item in dados["agenda"]:

                texto = QLabel(
                    f'{item["horario"]}   '
                    f'{item["nome"]}   '
                    f'Sala {item["sala"]}'
                )

                agenda_layout.addWidget(texto)

        else:

            agenda_layout.addWidget(
                QLabel("Nenhum atendimento cadastrado.")
            )

        layout.addWidget(agenda)

        # ------------------------
        # ALERTAS
        # ------------------------

        alertas = QFrame()

        alertas.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:12px;
            }
        """)

        alerta_layout = QVBoxLayout(alertas)

        titulo_alerta = QLabel("⚠ Alertas")
        titulo_alerta.setFont(
            QFont("Segoe UI", 12, QFont.Bold)
        )

        alerta_layout.addWidget(titulo_alerta)

        if dados["alertas"]:

            for alerta in dados["alertas"]:

                alerta_layout.addWidget(
                    QLabel("• " + alerta)
                )

        else:

            alerta_layout.addWidget(
                QLabel("Nenhum alerta.")
            )

        layout.addWidget(alertas)

        layout.addStretch()
