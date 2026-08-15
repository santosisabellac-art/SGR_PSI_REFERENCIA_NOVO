from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
)

from app.services.aprendiz_service import AprendizService
from app.services.documento_service import DocumentoService


class DocumentoDialog(QDialog):

    def __init__(self, parent=None, aprendiz_id=None, documento=None):
        super().__init__(parent)

        self.documento_service = DocumentoService()
        self.aprendiz_service = AprendizService()
        self.aprendiz_id = aprendiz_id
        self.documento = documento
        self.editando = documento is not None

        self.setWindowTitle(
            "Editar Documento" if self.editando else "Novo Documento"
        )
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
        self.preencher_formulario()

    def carregar_aprendizes(self):
        aprendizes = [
            aprendiz
            for aprendiz in self.aprendiz_service.listar()
            if getattr(aprendiz, "ativo", True)
        ]

        for aprendiz in aprendizes:
            self.aprendiz.addItem(aprendiz.nome, aprendiz.id)

    def preencher_formulario(self):
        if self.documento is not None:
            indice = self.aprendiz.findData(self.documento.aprendiz_id)
            if indice >= 0:
                self.aprendiz.setCurrentIndex(indice)

            tipo = self.documento.tipo or ""
            indice_tipo = self.tipo.findText(tipo)
            if indice_tipo >= 0:
                self.tipo.setCurrentIndex(indice_tipo)
            else:
                self.tipo.setCurrentText(tipo)

            if self.documento.prazo:
                self.prazo.setDate(
                    QDate(
                        self.documento.prazo.year,
                        self.documento.prazo.month,
                        self.documento.prazo.day,
                    )
                )
                self.sem_prazo.setChecked(False)
            else:
                self.sem_prazo.setChecked(True)

            self.observacoes.setPlainText(
                self.documento.observacoes or ""
            )

        elif self.aprendiz_id is not None:
            indice = self.aprendiz.findData(self.aprendiz_id)
            if indice >= 0:
                self.aprendiz.setCurrentIndex(indice)
                self.aprendiz.setEnabled(False)

    def salvar(self):
        tipo = self.tipo.currentText().strip()
        aprendiz_id = self.aprendiz.currentData()

        if aprendiz_id is None:
            QMessageBox.warning(
                self,
                "Aprendiz obrigatório",
                "Cadastre ou selecione um aprendiz antes de salvar o documento.",
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

        observacoes = self.observacoes.toPlainText().strip()

        if self.documento is None:
            self.documento_service.criar(
                aprendiz_id=aprendiz_id,
                tipo=tipo,
                prazo=prazo,
                observacoes=observacoes,
            )
        else:
            self.documento_service.atualizar(
                documento_id=self.documento.id,
                aprendiz_id=aprendiz_id,
                tipo=tipo,
                prazo=prazo,
                observacoes=observacoes,
            )

        self.accept()
