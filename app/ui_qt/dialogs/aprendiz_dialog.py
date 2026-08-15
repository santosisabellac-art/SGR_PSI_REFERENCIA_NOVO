from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.services.aprendiz_service import AprendizService


class AprendizDialog(QDialog):

    def __init__(self, parent=None, aprendiz=None):
        super().__init__(parent)

        self.service = AprendizService()
        self.aprendiz = aprendiz

        self.setWindowTitle(
            "Editar Aprendiz"
            if aprendiz
            else "Novo Aprendiz"
        )

        self.resize(520, 500)

        layout = QVBoxLayout(self)

        formulario = QFormLayout()

        self.nome = QLineEdit()
        self.codigo = QLineEdit()

        self.nivel = QComboBox()
        self.nivel.addItems([
            "Nível 1",
            "Nível 2",
            "Nível 3",
        ])

        self.sala = QLineEdit()
        self.dias = QLineEdit()
        self.horario = QLineEdit()
        self.carga = QLineEdit()
        self.observacoes = QTextEdit()

        formulario.addRow("Nome", self.nome)
        formulario.addRow("Código", self.codigo)
        formulario.addRow("Nível", self.nivel)
        formulario.addRow("Sala", self.sala)
        formulario.addRow("Dias", self.dias)
        formulario.addRow("Horário", self.horario)
        formulario.addRow("Carga ABA", self.carga)
        formulario.addRow("Observações", self.observacoes)

        layout.addLayout(formulario)

        botoes = QHBoxLayout()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_salvar = QPushButton("Salvar")

        botoes.addStretch()
        botoes.addWidget(self.btn_cancelar)
        botoes.addWidget(self.btn_salvar)

        layout.addLayout(botoes)

        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_salvar.clicked.connect(self.salvar)

        if aprendiz:
            self.preencher_campos()

    def preencher_campos(self):

        self.nome.setText(self.aprendiz.nome)
        self.codigo.setText(self.aprendiz.codigo)

        self.nivel.setCurrentText(
            self.aprendiz.nivel_suporte
        )

        self.sala.setText(self.aprendiz.sala or "")
        self.dias.setText(self.aprendiz.dias_atendimento or "")
        self.horario.setText(self.aprendiz.horario or "")
        self.carga.setText(
            self.aprendiz.carga_horaria_aba or ""
        )
        self.observacoes.setPlainText(
            self.aprendiz.observacoes or ""
        )

    def salvar(self):

        if not self.nome.text().strip():

            QMessageBox.warning(
                self,
                "Erro",
                "Informe o nome."
            )
            return

        if self.aprendiz:

            self.service.atualizar(
                aprendiz_id=self.aprendiz.id,
                nome=self.nome.text().strip(),
                codigo=self.codigo.text().strip(),
                nivel_suporte=self.nivel.currentText(),
                dias_atendimento=self.dias.text().strip(),
                horario=self.horario.text().strip(),
                sala=self.sala.text().strip(),
                carga_horaria_aba=self.carga.text().strip(),
                observacoes=self.observacoes.toPlainText().strip(),
            )

        else:

            self.service.criar(
                nome=self.nome.text().strip(),
                codigo=self.codigo.text().strip(),
                nivel_suporte=self.nivel.currentText(),
                dias_atendimento=self.dias.text().strip(),
                horario=self.horario.text().strip(),
                sala=self.sala.text().strip(),
                carga_horaria_aba=self.carga.text().strip(),
                observacoes=self.observacoes.toPlainText().strip(),
            )

        self.accept()