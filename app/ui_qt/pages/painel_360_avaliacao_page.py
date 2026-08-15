from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QPushButton

from app.ui_qt.pages.painel_360_page import Painel360Page
from app.ui_qt.dialogs.avaliacao_dialog import AvaliacaoDialog


class Painel360AvaliacaoPage(Painel360Page):
    """Extensão do Painel 360º com edição de avaliações."""

    def _criar_avaliacoes(self, layout):
        super()._criar_avaliacoes(layout)

        self.botao_editar_avaliacao = QPushButton("✏ Editar avaliação")
        self.botao_editar_avaliacao.clicked.connect(
            self.editar_avaliacao_selecionada
        )

        self.acoes_avaliacao.layout().insertWidget(
            0, self.botao_editar_avaliacao
        )

    def atualizar_acoes_avaliacao(self):
        item = self.lista_avaliacoes.currentItem()
        habilitar = (
            item is not None
            and item.data(Qt.UserRole) is not None
        )

        self.botao_excluir_avaliacao.setEnabled(habilitar)
        self.botao_editar_avaliacao.setEnabled(habilitar)

    def editar_avaliacao_selecionada(self):
        item = self.lista_avaliacoes.currentItem()

        if item is None or item.data(Qt.UserRole) is None:
            return

        avaliacao_id = item.data(Qt.UserRole)
        avaliacao = next(
            (
                registro
                for registro in self.avaliacao_service.listar_por_aprendiz(
                    self.aprendiz.id
                )
                if registro.id == avaliacao_id
            ),
            None,
        )

        if avaliacao is None:
            QMessageBox.warning(
                self,
                "Avaliação não encontrada",
                "Não foi possível localizar a avaliação selecionada.",
            )
            return

        dialog = AvaliacaoDialog(
            self.aprendiz.id,
            parent=self,
            avaliacao=avaliacao,
        )

        if dialog.exec():
            self.atualizar_avaliacoes()
