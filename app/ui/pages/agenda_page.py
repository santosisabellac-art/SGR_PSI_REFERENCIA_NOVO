from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.aprendiz_service import AprendizService


class AgendaPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = AprendizService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Agenda de Atendimentos")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.botao_atualizar = QPushButton("Atualizar")
        self.botao_atualizar.clicked.connect(self.carregar_agenda)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_atualizar)

        layout.addLayout(cabecalho)

        subtitulo = QLabel(
            "Visão dos dias, horários e salas cadastrados para cada aprendiz."
        )
        subtitulo.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitulo)

        self.resumo = QLabel()
        self.resumo.setStyleSheet("color: #374151; font-weight: 600;")
        layout.addWidget(self.resumo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Aprendiz",
                "Dias",
                "Horário",
                "Sala",
                "Carga ABA",
                "Status",
            ]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.tabela.setSelectionMode(
            QAbstractItemView.SingleSelection
        )
        self.tabela.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        layout.addWidget(self.tabela)

        self.aviso = QLabel()
        self.aviso.setStyleSheet("color: #D97706;")
        layout.addWidget(self.aviso)

        self.carregar_agenda()

    def carregar_agenda(self):
        aprendizes = [
            aprendiz
            for aprendiz in self.service.listar()
            if getattr(aprendiz, "ativo", True)
        ]

        aprendizes.sort(
            key=lambda aprendiz: (
                (aprendiz.dias_atendimento or "").lower(),
                aprendiz.horario or "",
                aprendiz.nome.lower(),
            )
        )

        self.tabela.setRowCount(len(aprendizes))

        sem_horario = 0

        for linha, aprendiz in enumerate(aprendizes):
            dias = aprendiz.dias_atendimento or "Não informado"
            horario = aprendiz.horario or "Não informado"

            if not aprendiz.dias_atendimento or not aprendiz.horario:
                sem_horario += 1

            valores = [
                aprendiz.nome,
                dias,
                horario,
                aprendiz.sala or "Não informada",
                aprendiz.carga_horaria_aba or "Não informada",
                aprendiz.status,
            ]

            for coluna, valor in enumerate(valores):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor),
                )

        self.resumo.setText(
            f"{len(aprendizes)} aprendiz(es) ativo(s) na agenda."
        )

        if sem_horario:
            self.aviso.setText(
                f"Atenção: {sem_horario} aprendiz(es) sem dia ou horário "
                "cadastrado."
            )
        else:
            self.aviso.setText("Todos os aprendizes ativos têm agenda cadastrada.")
