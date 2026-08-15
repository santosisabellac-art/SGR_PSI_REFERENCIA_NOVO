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

    def __init__(self, aprendiz_id, parent=None):
        super().__init__(parent)

        self.aprendiz_id = aprendiz_id
        self.service = AvaliacaoService()

        self.setWindowTitle("Nova Avaliação")
        self.resize(580, 460)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDate(QDate.currentDate())

        self.instrumento = QComboBox()
        self.instrumento.setEditable(True)
        self.instrumento.addItems(
            [
                "VB-MAPP",
                "ABLLS-R",
                "AFLS",
                "PEP-3",
                "Avaliação comportamental",
                "Outro",
            ]
        )

        self.responsavel = QLineEdit()
        self.responsavel.setPlaceholderText(
            "Nome do profissional responsável"
        )

        self.sintese = QTextEdit()
        self.sintese.setPlaceholderText(
            "Síntese dos resultados e pontos relevantes"
        )

        self.proximos_passos = QTextEdit()
        self.proximos_passos.setPlaceholderText(
            "Encaminhamentos ou ações definidas"
        )

        formulario.addRow("Data", self.data)
        formulario.addRow("Instrumento", self.instrumento)
        formulario.addRow("Responsável", self.responsavel)
        formulario.addRow("Síntese", self.sintese)
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
        instrumento = self.instrumento.currentText().strip()
        responsavel = self.responsavel.text().strip()
        sintese = self.sintese.toPlainText().strip()

        if not instrumento:
            QMessageBox.warning(
                self,
                "Instrumento obrigatório",
                "Informe o instrumento ou tipo de avaliação.",
            )
            return

        if not responsavel:
            QMessageBox.warning(
                self,
                "Responsável obrigatório",
                "Informe o responsável pela avaliação.",
            )
            return

        if not sintese:
            QMessageBox.warning(
                self,
                "Síntese obrigatória",
                "Registre uma síntese da avaliação.",
            )
            return

        self.service.criar(
            aprendiz_id=self.aprendiz_id,
            data=self.data.date().toPython(),
            instrumento=instrumento,
            responsavel=responsavel,
            sintese=sintese,
            proximos_passos=self.proximos_passos.toPlainText().strip(),
        )

        self.accept()
