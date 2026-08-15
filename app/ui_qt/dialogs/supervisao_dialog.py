from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.services.supervisao_service import SupervisaoService


class SupervisaoDialog(QDialog):

    def __init__(self, aprendiz_id, parent=None, supervisao=None):
        super().__init__(parent)
        self.aprendiz_id = aprendiz_id
        self.supervisao = supervisao
        self.service = SupervisaoService()
        self.setWindowTitle("Editar Supervisão" if supervisao else "Nova Supervisão")
        self.resize(580, 480)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()
        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDate(QDate.currentDate())
        self.responsavel = QLineEdit()
        self.resumo = QTextEdit()
        self.orientacoes = QTextEdit()
        self.proximos_passos = QTextEdit()
        formulario.addRow("Data", self.data)
        formulario.addRow("Responsável", self.responsavel)
        formulario.addRow("Resumo", self.resumo)
        formulario.addRow("Orientações", self.orientacoes)
        formulario.addRow("Próximos passos", self.proximos_passos)
        layout.addLayout(formulario)

        botoes = QHBoxLayout()
        cancelar = QPushButton("Cancelar")
        salvar = QPushButton("Salvar")
        botoes.addStretch()
        botoes.addWidget(cancelar)
        botoes.addWidget(salvar)
        layout.addLayout(botoes)
        cancelar.clicked.connect(self.reject)
        salvar.clicked.connect(self.salvar)

        if supervisao:
            self._carregar_supervisao()

    def _carregar_supervisao(self):
        self.data.setDate(
            QDate(
                self.supervisao.data.year,
                self.supervisao.data.month,
                self.supervisao.data.day,
            )
        )
        self.responsavel.setText(self.supervisao.responsavel or "")
        self.resumo.setPlainText(self.supervisao.resumo or "")
        self.orientacoes.setPlainText(self.supervisao.orientacoes or "")
        self.proximos_passos.setPlainText(self.supervisao.proximos_passos or "")

    def salvar(self):
        responsavel = self.responsavel.text().strip()
        resumo = self.resumo.toPlainText().strip()
        if not responsavel:
            QMessageBox.warning(self, "Responsável obrigatório", "Informe o responsável pela supervisão.")
            return
        if not resumo:
            QMessageBox.warning(self, "Resumo obrigatório", "Registre um resumo da supervisão.")
            return

        dados = dict(
            data=self.data.date().toPython(),
            responsavel=responsavel,
            resumo=resumo,
            orientacoes=self.orientacoes.toPlainText().strip(),
            proximos_passos=self.proximos_passos.toPlainText().strip(),
        )
        if self.supervisao:
            self.service.atualizar(self.supervisao.id, **dados)
        else:
            self.service.criar(aprendiz_id=self.aprendiz_id, **dados)
        self.accept()
