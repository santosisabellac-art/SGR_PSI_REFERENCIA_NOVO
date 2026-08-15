from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QPushButton

from app.ui_qt.dialogs.documento_dialog import DocumentoDialog
from app.ui_qt.pages.painel_360_registros_page import Painel360RegistrosPage


class Painel360DocumentoPage(Painel360RegistrosPage):
    """Painel 360º com edição de documentos, avaliações e supervisões."""

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
        from PySide6.QtWidgets import QListWidgetItem
        item = QListWidgetItem(texto)
        item.setFlags(Qt.NoItemFlags)
        return item

    def _item_documento(self, texto, documento_id, tooltip):
        from PySide6.QtWidgets import QListWidgetItem
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
