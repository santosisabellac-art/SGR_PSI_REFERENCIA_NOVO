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

    def __init__(self, aprendiz_id, parent=None, pendencia=None):
        super().__init__(parent)

        self.service = PendenciaService()
        self.aprendiz_id = aprendiz_id
        self.pendencia = pendencia

        self.setWindowTitle(
            "Editar Pendência" if pendencia else "Nova Pendência"
        )
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

        if self.pendencia is not None:
            self.titulo.setText(self.pendencia.titulo or "")
            self.descricao.setPlainText(self.pendencia.descricao or "")

    def salvar(self):
        titulo = self.titulo.text().strip()

        if not titulo:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o título da pendência.",
            )
            return

        descricao = self.descricao.toPlainText().strip()

        if self.pendencia is None:
            self.service.criar(
                aprendiz_id=self.aprendiz_id,
                titulo=titulo,
                descricao=descricao,
            )
        else:
            self.service.atualizar(
                pendencia_id=self.pendencia.id,
                titulo=titulo,
                descricao=descricao,
            )

        self.accept()
