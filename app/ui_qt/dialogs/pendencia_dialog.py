from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.services.pendencia_service import PendenciaService


class PendenciaDialog(QDialog):

    def __init__(self, aprendiz_id, parent=None):
        super().__init__(parent)

        self.service = PendenciaService()
        self.aprendiz_id = aprendiz_id

        self.setWindowTitle("Nova Pendência")
        self.resize(500, 300)

        layout = QVBoxLayout(self)

        formulario = QFormLayout()

        self.titulo = QLineEdit()
        self.descricao = QTextEdit()

        formulario.addRow("Título", self.titulo)
        formulario.addRow("Descrição", self.descricao)

        layout.addLayout(formulario)

        observacao = QLabel(
            "Exemplos: Atualizar PEI, Fazer supervisão, "
            "Aplicar VB-MAPP, Contatar família..."
        )

        observacao.setWordWrap(True)

        layout.addWidget(observacao)

        botoes = QHBoxLayout()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_salvar = QPushButton("Salvar")

        botoes.addStretch()
        botoes.addWidget(self.btn_cancelar)
        botoes.addWidget(self.btn_salvar)

        layout.addLayout(botoes)

        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_salvar.clicked.connect(self.salvar)

    def salvar(self):

        titulo = self.titulo.text().strip()

        if titulo == "":

            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o título da pendência."
            )

            return

        self.service.criar(
            aprendiz_id=self.aprendiz_id,
            titulo=titulo,
            descricao=self.descricao.toPlainText().strip(),
        )

        self.accept()