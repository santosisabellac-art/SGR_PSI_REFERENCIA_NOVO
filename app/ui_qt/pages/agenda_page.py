from datetime import datetime

from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont

from app.services.aprendiz_service import AprendizService


class AgendaPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = AprendizService()
        self.aprendizes = []
        self.lista_visivel = []

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

        filtros = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Pesquisar aprendiz, sala ou horário...")
        self.pesquisa.textChanged.connect(self.aplicar_filtros)

        self.filtro_dia = QComboBox()
        self.filtro_dia.addItem("Todos os dias", "todos")
        self.filtro_dia.addItem("Hoje", "hoje")
        self.filtro_dia.currentIndexChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.pesquisa, 1)
        filtros.addWidget(self.filtro_dia)
        layout.addLayout(filtros)

        self.resumo = QLabel()
        self.resumo.setStyleSheet("color: #374151; font-weight: 600;")
        layout.addWidget(self.resumo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["Aprendiz", "Dias", "Horário", "Sala", "Carga ABA", "Status"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(self.tabela)

        self.aviso = QLabel()
        self.aviso.setStyleSheet("color: #D97706;")
        layout.addWidget(self.aviso)

        self.carregar_agenda()

    def carregar_agenda(self):
        self.aprendizes = [
            aprendiz
            for aprendiz in self.service.listar()
            if getattr(aprendiz, "ativo", True)
        ]
        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto = self.pesquisa.text().lower().strip()
        modo_dia = self.filtro_dia.currentData()

        hoje = datetime.now().weekday()
        nomes_dias = {
            0: ("segunda", "seg", "segunda-feira"),
            1: ("terça", "terca", "ter", "terça-feira", "terca-feira"),
            2: ("quarta", "qua", "quarta-feira"),
            3: ("quinta", "qui", "quinta-feira"),
            4: ("sexta", "sex", "sexta-feira"),
            5: ("sábado", "sabado", "sáb", "sab"),
            6: ("domingo", "dom"),
        }
        dias_hoje = nomes_dias[hoje]

        filtrados = []

        for aprendiz in self.aprendizes:
            dias = (aprendiz.dias_atendimento or "").lower()
            horario = (aprendiz.horario or "").lower()
            sala = (aprendiz.sala or "").lower()
            nome = (aprendiz.nome or "").lower()

            corresponde_texto = (
                not texto
                or texto in nome
                or texto in sala
                or texto in horario
            )

            corresponde_dia = (
                modo_dia == "todos"
                or any(dia in dias for dia in dias_hoje)
            )

            if corresponde_texto and corresponde_dia:
                filtrados.append(aprendiz)

        filtrados.sort(
            key=lambda aprendiz: (
                aprendiz.horario or "",
                aprendiz.nome.lower(),
            )
        )

        self.lista_visivel = filtrados
        self.tabela.setRowCount(len(filtrados))

        sem_agenda = 0

        for linha, aprendiz in enumerate(filtrados):
            dias = aprendiz.dias_atendimento or "Não informado"
            horario = aprendiz.horario or "Não informado"

            if not aprendiz.dias_atendimento or not aprendiz.horario:
                sem_agenda += 1

            valores = [
                aprendiz.nome,
                dias,
                horario,
                aprendiz.sala or "Não informada",
                aprendiz.carga_horaria_aba or "Não informada",
                aprendiz.status or "Ativo",
            ]

            for coluna, valor in enumerate(valores):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor)),
                )

        self.resumo.setText(
            f"{len(filtrados)} aprendiz(es) encontrado(s)."
        )

        if sem_agenda:
            self.aviso.setText(
                f"Atenção: {sem_agenda} aprendiz(es) desta visualização "
                "estão sem dia ou horário cadastrado."
            )
        elif not filtrados:
            self.aviso.setText("Nenhum atendimento encontrado para o filtro atual.")
        else:
            self.aviso.setText("")
