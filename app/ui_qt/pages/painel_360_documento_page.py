from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QListWidget, QListWidgetItem

from app.services.atividade_service import AtividadeService
from app.ui_qt.dialogs.documento_dialog import DocumentoDialog
from app.ui_qt.pages.painel_360_registros_page import Painel360RegistrosPage


class Painel360DocumentoPage(Painel360RegistrosPage):
    """Painel 360º com edição de documentos, avaliações e supervisões."""

    def __init__(self, aprendiz):
        self.atividade_service = AtividadeService()
        super().__init__(aprendiz)
        self._criar_historico_atividades()
        self.atualizar_historico_atividades()

    def _criar_documentos(self, layout):
        super()._criar_documentos(layout)

        self.lista_documentos.itemSelectionChanged.connect(
            self.atualizar_acoes_documento
        )

        self.acoes_documento = QPushButton("✏ Editar documento")
        self.acoes_documento.clicked.connect(
            self.editar_documento_selecionado
        )
        self.acoes_documento.setVisible(False)

        self.card_documentos.layout().addWidget(self.acoes_documento)

    def _criar_historico_atividades(self):
        layout = self.findChild(QListWidget)
        parent_layout = self.layout()
        if parent_layout is None:
            return

        self.card_historico = self._criar_card_historico(parent_layout)

    def _criar_card_historico(self, layout):
        from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout
        from PySide6.QtGui import QFont

        card = QFrame()
        card.setStyleSheet(
            "QFrame { background:white; border:1px solid #DDDDDD; border-radius:12px; }"
        )
        interno = QVBoxLayout(card)
        interno.setContentsMargins(18, 16, 18, 16)
        interno.setSpacing(10)

        cabecalho = QHBoxLayout()
        titulo = QLabel("Histórico de Atividades")
        titulo.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.contador_historico = QLabel()
        self.contador_historico.setStyleSheet("color:#6B7280; font-weight:600;")
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.contador_historico)
        interno.addLayout(cabecalho)

        self.lista_historico = QListWidget()
        self.lista_historico.setMinimumHeight(180)
        self.lista_historico.setStyleSheet(
            "QListWidget { border:1px solid #E5E7EB; border-radius:8px; padding:4px; } "
            "QListWidget::item { padding:8px; }"
        )
        interno.addWidget(self.lista_historico)
        layout.addWidget(card)
        return card

    def atualizar_historico_atividades(self):
        atividades = self.atividade_service.listar_por_aprendiz(self.aprendiz.id)
        total = len(atividades)
        self.contador_historico.setText(
            "1 registro" if total == 1 else f"{total} registros"
        )
        self.lista_historico.clear()

        if not atividades:
            item = QListWidgetItem("Nenhuma atividade registrada ainda.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_historico.addItem(item)
            return

        for atividade in atividades:
            data = (
                atividade.criado_em.strftime("%d/%m/%Y %H:%M")
                if atividade.criado_em
                else "Data não informada"
            )
            item = QListWidgetItem(
                f"{data} — {atividade.tipo}\n{atividade.descricao}"
            )
            item.setData(Qt.UserRole, atividade.id)
            self.lista_historico.addItem(item)

    def atualizar_acoes_documento(self):
        item = self.lista_documentos.currentItem()
        habilitar = (
            item is not None
            and item.data(Qt.UserRole) is not None
        )
        self.acoes_documento.setVisible(self.lista_documentos.isVisible())
        self.acoes_documento.setEnabled(habilitar)

    def alternar_lista_documentos(self):
        super().alternar_lista_documentos()
        self.atualizar_acoes_documento()

    def atualizar_documentos(self):
        documentos = [
            documento
            for documento in self.documento_service.listar()
            if documento.aprendiz_id == self.aprendiz.id
            and self.documento_service.situacao(documento) != "Entregue"
        ]

        self.contador_documentos.setText(
            "1 documento pendente"
            if len(documentos) == 1
            else f"{len(documentos)} documentos pendentes"
        )
        self.lista_documentos.clear()

        if not documentos:
            item = self._item_sem_registro("Nenhum documento pendente.")
            self.lista_documentos.addItem(item)
            self.atualizar_acoes_documento()
            return

        for documento in documentos:
            situacao = self.documento_service.situacao(documento)
            prazo = (
                documento.prazo.strftime("%d/%m/%Y")
                if documento.prazo
                else "sem prazo"
            )
            item = self._item_documento(
                f"{documento.tipo} — {situacao} ({prazo})",
                documento.id,
                documento.observacoes or "",
            )
            self.lista_documentos.addItem(item)

        self.atualizar_acoes_documento()

    def _item_sem_registro(self, texto):
        item = QListWidgetItem(texto)
        item.setFlags(Qt.NoItemFlags)
        return item

    def _item_documento(self, texto, documento_id, tooltip):
        item = QListWidgetItem(texto)
        item.setData(Qt.UserRole, documento_id)
        item.setToolTip(tooltip)
        return item

    def editar_documento_selecionado(self):
        item = self.lista_documentos.currentItem()
        if item is None or item.data(Qt.UserRole) is None:
            return

        documento_id = item.data(Qt.UserRole)
        documento = next(
            (
                registro
                for registro in self.documento_service.listar()
                if registro.id == documento_id
            ),
            None,
        )

        if documento is None:
            QMessageBox.warning(
                self,
                "Documento não encontrado",
                "Não foi possível localizar o documento selecionado.",
            )
            return

        dialog = DocumentoDialog(
            parent=self,
            aprendiz_id=self.aprendiz.id,
            documento=documento,
        )

        if dialog.exec():
            self.atualizar_documentos()
