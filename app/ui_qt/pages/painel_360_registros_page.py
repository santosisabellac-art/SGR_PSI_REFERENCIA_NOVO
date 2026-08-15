from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QPushButton

from app.ui_qt.dialogs.supervisao_dialog import SupervisaoDialog
from app.ui_qt.pages.painel_360_avaliacao_page import Painel360AvaliacaoPage


class Painel360RegistrosPage(Painel360AvaliacaoPage):
    """Painel 360º com edição de avaliações e supervisões."""

    def _criar_supervisoes(self, layout):
        super()._criar_supervisoes(layout)

        self.botao_editar_supervisao = QPushButton("✏ Editar supervisão")
        self.botao_editar_supervisao.clicked.connect(
            self.editar_supervisao_selecionada
        )
        self.acoes_supervisao.layout().insertWidget(
            0, self.botao_editar_supervisao
        )

    def atualizar_acoes_supervisao(self):
        item = self.lista_supervisoes.currentItem()
        habilitar = (
            item is not None
            and item.data(Qt.UserRole) is not None
        )
        self.botao_excluir_supervisao.setEnabled(habilitar)
        self.botao_editar_supervisao.setEnabled(habilitar)

    def editar_supervisao_selecionada(self):
        item = self.lista_supervisoes.currentItem()

        if item is None or item.data(Qt.UserRole) is None:
            return

        supervisao_id = item.data(Qt.UserRole)
        supervisao = next(
            (
                registro
                for registro in self.supervisao_service.listar_por_aprendiz(
                    self.aprendiz.id
                )
                if registro.id == supervisao_id
            ),
            None,
        )

        if supervisao is None:
            QMessageBox.warning(
                self,
                "Supervisão não encontrada",
                "Não foi possível localizar a supervisão selecionada.",
            )
            return

        dialog = SupervisaoDialog(
            self.aprendiz.id,
            parent=self,
            supervisao=supervisao,
        )

        if dialog.exec():
            self.atualizar_supervisoes()
