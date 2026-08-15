from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QHBoxLayout, QMessageBox, QPushButton,
    QHeaderView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QLabel, QLineEdit,
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
        self.botao_editar = QPushButton("✏ Editar")
        self.botao_status = QPushButton("Marcar como Entregue")
        self.botao_excluir = QPushButton("Excluir")
        self.botao_novo.clicked.connect(self.abrir_novo_documento)
        self.botao_editar.clicked.connect(self.editar_documento)
        self.botao_status.clicked.connect(self.alterar_status)
        self.botao_excluir.clicked.connect(self.excluir_documento)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_editar)
        cabecalho.addWidget(self.botao_status)
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
        self.filtro_situacao.currentIndexChanged.connect(self.aplicar_filtros)
        filtros.addWidget(self.pesquisa)
        filtros.addWidget(self.filtro_situacao)
        layout.addLayout(filtros)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["Aprendiz", "Documento", "Prazo", "Situação", "Observações"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.doubleClicked.connect(self.editar_documento)
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
            if ((not texto or texto in aprendiz.lower() or texto in (documento.tipo or "").lower())
                    and (situacao_filtro == "todas" or situacao == situacao_filtro)):
                documentos.append(documento)
        self.lista_visivel = documentos
        self.tabela.setRowCount(len(documentos))
        for linha, documento in enumerate(documentos):
            aprendiz = documento.aprendiz.nome if documento.aprendiz else "Aprendiz não encontrado"
            prazo = documento.prazo.strftime("%d/%m/%Y") if documento.prazo else "Sem prazo"
            valores = [aprendiz, documento.tipo, prazo, self.service.situacao(documento), documento.observacoes or ""]
            for coluna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                if coluna == 3 and valor == "Vencido":
                    item.setForeground(Qt.red)
                self.tabela.setItem(linha, coluna, item)
        self.atualizar_botoes()

    def documento_selecionado(self):
        linha = self.tabela.currentRow()
        return self.lista_visivel[linha] if 0 <= linha < len(self.lista_visivel) else None

    def atualizar_botoes(self):
        documento = self.documento_selecionado()
        selecionado = documento is not None
        self.botao_editar.setEnabled(selecionado)
        self.botao_excluir.setEnabled(selecionado)
        self.botao_status.setEnabled(selecionado)
        if not selecionado:
            self.botao_status.setText("Marcar como Entregue")
            return
        self.botao_status.setText("Reabrir documento" if self.service.situacao(documento) == "Entregue" else "Marcar como Entregue")

    def abrir_novo_documento(self):
        if DocumentoDialog(self).exec():
            self.carregar_documentos()

    def editar_documento(self):
        documento = self.documento_selecionado()
        if documento is None:
            QMessageBox.information(self, "Editar documento", "Selecione um documento.")
            return
        if DocumentoDialog(self, documento=documento).exec():
            self.carregar_documentos()

    def alterar_status(self):
        documento = self.documento_selecionado()
        if documento is None:
            return
        entregue = self.service.situacao(documento) == "Entregue"
        resultado = (
            self.service.marcar_como_pendente(documento.id)
            if entregue
            else self.service.marcar_como_entregue(documento.id)
        )
        if resultado is None:
            QMessageBox.warning(self, "Operação não concluída", "O documento não foi localizado no banco de dados.")
            return
        self.carregar_documentos()
        QMessageBox.information(self, "Documento atualizado", "A situação do documento foi atualizada com sucesso.")

    def excluir_documento(self):
        documento = self.documento_selecionado()
        if documento is None:
            QMessageBox.information(self, "Excluir documento", "Selecione um documento.")
            return
        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Deseja realmente excluir o documento?\n\n{documento.tipo}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if resposta != QMessageBox.Yes:
            return
        resultado = self.service.excluir(documento.id)
        if not resultado:
            QMessageBox.warning(self, "Exclusão não concluída", "O documento não foi localizado ou não pôde ser excluído.")
            self.carregar_documentos()
            return
        self.carregar_documentos()
        QMessageBox.information(self, "Exclusão concluída", "O documento foi excluído com sucesso.")
