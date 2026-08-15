from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.services.aprendiz_service import AprendizService
from app.services.documento_service import DocumentoService


class DocumentoDialog(QDialog):

    def __init__(self, parent=None, aprendiz_id=None):
        super().__init__(parent)

        self.documento_service = DocumentoService()
        self.aprendiz_service = AprendizService()
        self.aprendiz_id = aprendiz_id

        self.setWindowTitle("Novo Documento")
        self.resize(520, 360)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.aprendiz = QComboBox()
        self.tipo = QComboBox()
        self.tipo.setEditable(True)
        self.tipo.addItems(
            [
                "PEI",
                "Relatório",
                "Avaliação",
                "Autorização",
                "Documento médico",
                "Outro",
            ]
        )

        self.prazo = QDateEdit()
        self.prazo.setCalendarPopup(True)
        self.prazo.setDate(QDate.currentDate())

        self.sem_prazo = QCheckBox("Sem prazo definido")
        self.sem_prazo.toggled.connect(
            lambda marcado: self.prazo.setEnabled(not marcado)
        )

        self.observacoes = QTextEdit()
        self.observacoes.setPlaceholderText(
            "Ex.: solicitar assinatura da família."
        )

        formulario.addRow("Aprendiz", self.aprendiz)
        formulario.addRow("Tipo de documento", self.tipo)
        formulario.addRow("Prazo", self.prazo)
        formulario.addRow("", self.sem_prazo)
        formulario.addRow("Observações", self.observacoes)

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

        self.carregar_aprendizes()

        if self.aprendiz_id is not None:
            indice = self.aprendiz.findData(self.aprendiz_id)

            if indice >= 0:
                self.aprendiz.setCurrentIndex(indice)
                self.aprendiz.setEnabled(False)

    def carregar_aprendizes(self):
        aprendizes = [
            aprendiz
            for aprendiz in self.aprendiz_service.listar()
            if getattr(aprendiz, "ativo", True)
        ]

        for aprendiz in aprendizes:
            self.aprendiz.addItem(aprendiz.nome, aprendiz.id)

    def salvar(self):
        tipo = self.tipo.currentText().strip()
        aprendiz_id = self.aprendiz.currentData()

        if aprendiz_id is None:
            QMessageBox.warning(
                self,
                "Aprendiz obrigatório",
                "Cadastre ou selecione um aprendiz antes de criar o documento.",
            )
            return

        if not tipo:
            QMessageBox.warning(
                self,
                "Tipo obrigatório",
                "Informe o tipo de documento.",
            )
            return

        prazo = None
        if not self.sem_prazo.isChecked():
            prazo = self.prazo.date().toPython()

        self.documento_service.criar(
            aprendiz_id=aprendiz_id,
            tipo=tipo,
            prazo=prazo,
            observacoes=self.observacoes.toPlainText().strip(),
        )

        self.accept()
