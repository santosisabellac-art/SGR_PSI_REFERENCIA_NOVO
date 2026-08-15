from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
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

from app.services.avaliacao_service import AvaliacaoService


class AvaliacaoDialog(QDialog):

    def __init__(self, aprendiz_id, parent=None, avaliacao=None):
        super().__init__(parent)
        self.aprendiz_id = aprendiz_id
        self.avaliacao = avaliacao
        self.service = AvaliacaoService()

        self.setWindowTitle("Editar Avaliação" if avaliacao else "Nova Avaliação")
        self.resize(580, 460)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDate(QDate.currentDate())

        self.instrumento = QComboBox()
        self.instrumento.setEditable(True)
        self.instrumento.addItems(["VB-MAPP", "ABLLS-R", "AFLS", "PEP-3", "Avaliação comportamental", "Outro"])

        self.responsavel = QLineEdit()
        self.sintese = QTextEdit()
        self.proximos_passos = QTextEdit()

        formulario.addRow("Data", self.data)
        formulario.addRow("Instrumento", self.instrumento)
        formulario.addRow("Responsável", self.responsavel)
        formulario.addRow("Síntese", self.sintese)
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

        if avaliacao:
            self.data.setDate(QDate.fromString(avaliacao.data.strftime("yyyy-MM-dd"), "yyyy-MM-dd"))
            self.instrumento.setCurrentText(avaliacao.instrumento or "")
            self.responsavel.setText(avaliacao.responsavel or "")
            self.sintese.setPlainText(avaliacao.sintese or "")
            self.proximos_passos.setPlainText(avaliacao.proximos_passos or "")

    def salvar(self):
        instrumento = self.instrumento.currentText().strip()
        responsavel = self.responsavel.text().strip()
        sintese = self.sintese.toPlainText().strip()
        if not instrumento:
            QMessageBox.warning(self, "Instrumento obrigatório", "Informe o instrumento ou tipo de avaliação.")
            return
        if not responsavel:
            QMessageBox.warning(self, "Responsável obrigatório", "Informe o responsável pela avaliação.")
            return
        if not sintese:
            QMessageBox.warning(self, "Síntese obrigatória", "Registre uma síntese da avaliação.")
            return

        dados = dict(
            aprendiz_id=self.aprendiz_id,
            data=self.data.date().toPython(),
            instrumento=instrumento,
            responsavel=responsavel,
            sintese=sintese,
            proximos_passos=self.proximos_passos.toPlainText().strip(),
        )
        if self.avaliacao:
            self.service.atualizar(self.avaliacao.id, **{k: v for k, v in dados.items() if k != "aprendiz_id"})
        else:
            self.service.criar(**dados)
        self.accept()
