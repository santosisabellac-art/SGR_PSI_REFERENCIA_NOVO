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

    def __init__(self, aprendiz_id, parent=None):
        super().__init__(parent)

        self.aprendiz_id = aprendiz_id
        self.service = SupervisaoService()

        self.setWindowTitle("Nova Supervisão")
        self.resize(580, 480)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDate(QDate.currentDate())

        self.responsavel = QLineEdit()
        self.responsavel.setPlaceholderText(
            "Nome do profissional responsável"
        )

        self.resumo = QTextEdit()
        self.resumo.setPlaceholderText("O que foi discutido na supervisão?")

        self.orientacoes = QTextEdit()
        self.orientacoes.setPlaceholderText("Orientações definidas")

        self.proximos_passos = QTextEdit()
        self.proximos_passos.setPlaceholderText("Ações para acompanhamento")

        formulario.addRow("Data", self.data)
        formulario.addRow("Responsável", self.responsavel)
        formulario.addRow("Resumo", self.resumo)
        formulario.addRow("Orientações", self.orientacoes)
        formulario.addRow("Próximos passos", self.proximos_passos)

        layout.addLayout(formulario)

        botoes = QHBoxLayout()
        botao_cancelar = QPushButton("Cancelar")
        botao_salvar = QPushButton("Salvar")

        botoes.addStretch()
        botoes.addWidget(botao_cancelar)
        botoes.addWidget(botao_salvar)

        layout.addLayout(botoes)

        botao_cancelar.clicked.connect(self.reject)
        botao_salvar.clicked.connect(self.salvar)

    def salvar(self):
        responsavel = self.responsavel.text().strip()
        resumo = self.resumo.toPlainText().strip()

        if not responsavel:
            QMessageBox.warning(
                self,
                "Responsável obrigatório",
                "Informe o responsável pela supervisão.",
            )
            return

        if not resumo:
            QMessageBox.warning(
                self,
                "Resumo obrigatório",
                "Registre um resumo da supervisão.",
            )
            return

        self.service.criar(
            aprendiz_id=self.aprendiz_id,
            data=self.data.date().toPython(),
            responsavel=responsavel,
            resumo=resumo,
            orientacoes=self.orientacoes.toPlainText().strip(),
            proximos_passos=self.proximos_passos.toPlainText().strip(),
        )

        self.accept()
