from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.aprendiz_service import AprendizService
from app.services.dashboard_service import DashboardService
from app.services.documento_service import DocumentoService
from app.services.pendencia_service import PendenciaService


class DashboardPage(QWidget):
    aprendiz_solicitado = Signal(object)

    def __init__(self):
        super().__init__()

        self.service = DashboardService()
        self.aprendiz_service = AprendizService()
        self.pendencia_service = PendenciaService()
        self.documento_service = DocumentoService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        cabecalho = QHBoxLayout()
        titulo = QLabel("Dashboard Operacional")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.botao_atualizar = QPushButton("Atualizar")
        self.botao_atualizar.clicked.connect(self.atualizar_dashboard)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_atualizar)
        layout.addLayout(cabecalho)

        subtitulo = QLabel("Prioridades para acompanhar no trabalho de hoje.")
        subtitulo.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitulo)

        cards = QHBoxLayout()
        _, self.total_aprendizes = self.criar_card(cards, "Aprendizes ativos")
        _, self.total_pendencias = self.criar_card(cards, "Pendências abertas")
        _, self.total_documentos = self.criar_card(cards, "Documentos pendentes")
        _, self.total_vencidos = self.criar_card(cards, "Documentos vencidos")
        _, self.total_agenda = self.criar_card(cards, "Agenda de hoje")
        layout.addLayout(cards)

        titulo_agenda = QLabel("Agenda de hoje")
        titulo_agenda.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(titulo_agenda)
        self.tabela_agenda = QTableWidget()
        self.tabela_agenda.setColumnCount(3)
        self.tabela_agenda.setHorizontalHeaderLabels(["Aprendiz", "Horário", "Sala"])
        self.tabela_agenda.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_agenda.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_agenda.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_agenda.setMinimumHeight(180)
        self.tabela_agenda.doubleClicked.connect(self.abrir_aprendiz_da_agenda)
        layout.addWidget(self.tabela_agenda)

        titulo_prioridades = QLabel("Prioridades")
        titulo_prioridades.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(titulo_prioridades)
        self.tabela_prioridades = QTableWidget()
        self.tabela_prioridades.setColumnCount(3)
        self.tabela_prioridades.setHorizontalHeaderLabels(["Tipo", "Aprendiz", "Detalhe"])
        self.tabela_prioridades.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_prioridades.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_prioridades.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_prioridades.setMinimumHeight(210)
        self.tabela_prioridades.doubleClicked.connect(self.abrir_aprendiz_da_prioridade)
        self.tabela_prioridades.itemSelectionChanged.connect(self.atualizar_acoes_prioridade)
        layout.addWidget(self.tabela_prioridades)

        acoes_prioridade = QHBoxLayout()
        self.botao_abrir_prioridade = QPushButton("Abrir Painel 360º")
        self.botao_concluir_pendencia = QPushButton("Concluir pendência")
        self.botao_entregar_documento = QPushButton("Marcar documento como entregue")
        self.botao_abrir_prioridade.clicked.connect(self.abrir_prioridade_selecionada)
        self.botao_concluir_pendencia.clicked.connect(self.concluir_pendencia_selecionada)
        self.botao_entregar_documento.clicked.connect(self.entregar_documento_selecionado)
        acoes_prioridade.addWidget(self.botao_abrir_prioridade)
        acoes_prioridade.addWidget(self.botao_concluir_pendencia)
        acoes_prioridade.addWidget(self.botao_entregar_documento)
        acoes_prioridade.addStretch()
        layout.addLayout(acoes_prioridade)

        titulo_alertas = QLabel("Alertas de cadastro")
        titulo_alertas.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(titulo_alertas)
        self.lista_alertas = QListWidget()
        self.lista_alertas.setMaximumHeight(160)
        layout.addWidget(self.lista_alertas)

        self.atualizar_dashboard()

    def criar_card(self, layout, titulo):
        card = QFrame()
        card.setStyleSheet("QFrame { background: white; border: 1px solid #DDDDDD; border-radius: 12px; }")
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
        self.total_pendencias.setText(str(dados["total_pendencias_abertas"]))
        self.total_documentos.setText(str(dados["total_documentos_pendentes"]))
        self.total_vencidos.setText(str(dados["total_documentos_vencidos"]))
        self.total_agenda.setText(str(len(dados["agenda"])))

        agenda = dados["agenda"]
        self.tabela_agenda.setRowCount(len(agenda))
        for linha, item in enumerate(agenda):
            for coluna, valor in enumerate([item["nome"], item["horario"], item["sala"]]):
                self.tabela_agenda.setItem(linha, coluna, QTableWidgetItem(str(valor)))

        prioridades = dados["prioridades"]
        self.tabela_prioridades.setRowCount(len(prioridades))
        for linha, prioridade in enumerate(prioridades):
            for coluna, valor in enumerate([prioridade["prioridade"], prioridade["aprendiz"], prioridade["detalhe"]]):
                item = QTableWidgetItem(str(valor))
                item.setData(Qt.UserRole, prioridade.get("registro_id"))
                self.tabela_prioridades.setItem(linha, coluna, item)

        self.lista_alertas.clear()
        alertas = dados["alertas"]
        self.lista_alertas.addItems(alertas or ["Nenhum alerta de cadastro."])
        self.atualizar_acoes_prioridade()

    def prioridade_selecionada(self):
        linha = self.tabela_prioridades.currentRow()
        prioridades = self.service.resumo()["prioridades"]
        if linha < 0 or linha >= len(prioridades):
            return None
        return prioridades[linha]

    def atualizar_acoes_prioridade(self):
        prioridade = self.prioridade_selecionada()
        habilitar = prioridade is not None
        self.botao_abrir_prioridade.setEnabled(habilitar)
        self.botao_concluir_pendencia.setEnabled(habilitar and prioridade.get("prioridade") == "Pendência aberta")
        self.botao_entregar_documento.setEnabled(habilitar and prioridade.get("prioridade") == "Documento vencido")

    def abrir_prioridade_selecionada(self):
        prioridade = self.prioridade_selecionada()
        if prioridade is not None:
            self._emitir_aprendiz(prioridade.get("aprendiz_id"))

    def concluir_pendencia_selecionada(self):
        prioridade = self.prioridade_selecionada()
        if prioridade is None or prioridade.get("prioridade") != "Pendência aberta":
            return
        titulo = prioridade.get("detalhe", "esta pendência")
        resposta = QMessageBox.question(self, "Concluir pendência", f"Deseja realmente concluir a pendência:\n\n{titulo}?", QMessageBox.Yes | QMessageBox.No)
        if resposta != QMessageBox.Yes:
            return
        pendencia = next((p for p in self.service.pendencias_abertas() if p.id == prioridade.get("registro_id")), None)
        if pendencia is None:
            QMessageBox.warning(self, "Pendência não encontrada", "A pendência selecionada não está mais disponível.")
            self.atualizar_dashboard()
            return
        resultado = self.pendencia_service.concluir(pendencia.id)
        if resultado:
            self.atualizar_dashboard()
            QMessageBox.information(self, "Pendência concluída", "A pendência foi concluída com sucesso.")
        else:
            QMessageBox.warning(self, "Conclusão não realizada", "Não foi possível concluir a pendência selecionada.")
            self.atualizar_dashboard()

    def entregar_documento_selecionado(self):
        prioridade = self.prioridade_selecionada()
        if prioridade is None or prioridade.get("prioridade") != "Documento vencido":
            return
        tipo = prioridade.get("detalhe", "este documento")
        resposta = QMessageBox.question(self, "Marcar documento como entregue", f"Deseja marcar como entregue:\n\n{tipo}?", QMessageBox.Yes | QMessageBox.No)
        if resposta != QMessageBox.Yes:
            return
        documento = next((d for d in self.service.documentos_vencidos() if d.id == prioridade.get("registro_id")), None)
        if documento is None:
            QMessageBox.warning(self, "Documento não encontrado", "O documento selecionado não está mais disponível.")
            self.atualizar_dashboard()
            return
        resultado = self.documento_service.marcar_como_entregue(documento.id)
        if resultado:
            self.atualizar_dashboard()
            QMessageBox.information(self, "Documento atualizado", "O documento foi marcado como entregue com sucesso.")
        else:
            QMessageBox.warning(self, "Operação não realizada", "Não foi possível atualizar o documento selecionado.")
            self.atualizar_dashboard()

    def _emitir_aprendiz(self, aprendiz_id):
        if aprendiz_id is None:
            return
        aprendiz = self.aprendiz_service.buscar(aprendiz_id)
        if aprendiz is not None:
            self.aprendiz_solicitado.emit(aprendiz)

    def abrir_aprendiz_da_agenda(self, index):
        if not index.isValid():
            return
        item = self.service.resumo()["agenda"][index.row()]
        self._emitir_aprendiz(item.get("aprendiz_id"))

    def abrir_aprendiz_da_prioridade(self, index):
        if not index.isValid():
            return
        item = self.service.resumo()["prioridades"][index.row()]
        self._emitir_aprendiz(item.get("aprendiz_id"))
