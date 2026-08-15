from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.documento_service import DocumentoService
from app.ui_qt.dialogs.documento_dialog import DocumentoDialog


class DocumentosPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = DocumentoService()
        self.documentos = []
        self.lista_visivel = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        cabecalho = QHBoxLayout()

        titulo = QLabel("Documentos")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.botao_novo = QPushButton("+ Novo Documento")
        self.botao_entregar = QPushButton("Marcar como Entregue")
        self.botao_excluir = QPushButton("Excluir")

        self.botao_novo.clicked.connect(self.abrir_novo_documento)
        self.botao_entregar.clicked.connect(self.marcar_como_entregue)
        self.botao_excluir.clicked.connect(self.excluir_documento)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_entregar)
        cabecalho.addWidget(self.botao_excluir)
        cabecalho.addWidget(self.botao_novo)

        layout.addLayout(cabecalho)

        filtros = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Pesquisar aprendiz ou documento...")
        self.pesquisa.textChanged.connect(self.aplicar_filtros)

        self.filtro_situacao = QComboBox()
        self.filtro_situacao.addItem("Todas as situações", "todas")
        self.filtro_situacao.addItem("Pendentes", "pendente")
        self.filtro_situacao.addItem("Entregues", "entregue")
        self.filtro_situacao.addItem("Vencidos", "vencido")
        self.filtro_situacao.currentIndexChanged.connect(
            self.aplicar_filtros
        )

        filtros.addWidget(self.pesquisa)
        filtros.addWidget(self.filtro_situacao)

        layout.addLayout(filtros)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Aprendiz",
                "Documento",
                "Prazo",
                "Situação",
                "Observações",
            ]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.itemSelectionChanged.connect(self.atualizar_botoes)

        layout.addWidget(self.tabela)

        self.carregar_documentos()

    def carregar_documentos(self):
        self.documentos = self.service.listar()
        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto = self.pesquisa.text().lower().strip()
        situacao_filtro = self.filtro_situacao.currentData()

        documentos = []

        for documento in self.documentos:
            aprendiz = documento.aprendiz.nome if documento.aprendiz else ""
            situacao = self.service.situacao(documento).lower()

            corresponde_texto = (
                not texto
                or texto in aprendiz.lower()
                or texto in documento.tipo.lower()
            )
            corresponde_situacao = (
                situacao_filtro == "todas"
                or situacao == situacao_filtro
            )

            if corresponde_texto and corresponde_situacao:
                documentos.append(documento)

        self.lista_visivel = documentos
        self.tabela.setRowCount(len(documentos))

        for linha, documento in enumerate(documentos):
            aprendiz = (
                documento.aprendiz.nome
                if documento.aprendiz
                else "Aprendiz não encontrado"
            )
            prazo = (
                documento.prazo.strftime("%d/%m/%Y")
                if documento.prazo
                else "Sem prazo"
            )
            valores = [
                aprendiz,
                documento.tipo,
                prazo,
                self.service.situacao(documento),
                documento.observacoes or "",
            ]

            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(valor)

                if coluna == 3 and valor == "Vencido":
                    item.setForeground(Qt.red)

                self.tabela.setItem(linha, coluna, item)

        self.atualizar_botoes()

    def abrir_novo_documento(self):
        dialog = DocumentoDialog(self)

        if dialog.exec():
            self.carregar_documentos()

    def documento_selecionado(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return None

        return self.lista_visivel[linha]

    def atualizar_botoes(self):
        documento = self.documento_selecionado()
        selecionado = documento is not None

        self.botao_excluir.setEnabled(selecionado)
        self.botao_entregar.setEnabled(
            selecionado
            and self.service.situacao(documento) != "Entregue"
        )

    def marcar_como_entregue(self):
        documento = self.documento_selecionado()

        if documento is None:
            return

        self.service.marcar_como_entregue(documento.id)
        self.carregar_documentos()

    def excluir_documento(self):
        documento = self.documento_selecionado()

        if documento is None:
            return

        resposta = QMessageBox.question(
            self,
            "Excluir documento",
            "Deseja realmente excluir o documento selecionado?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        self.service.excluir(documento.id)
        self.carregar_documentos()
