from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.aprendiz_service import AprendizService
from app.ui_qt.dialogs.aprendiz_dialog import AprendizDialog


class AprendizesPage(QWidget):

    painel_solicitado = Signal(object)

    def __init__(self):
        super().__init__()

        self.service = AprendizService()
        self.aprendizes = []
        self.lista_visivel = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Cabeçalho
        cabecalho = QHBoxLayout()

        titulo = QLabel("Aprendizes")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        self.botao_novo = QPushButton("➕ Novo Aprendiz")
        self.botao_painel = QPushButton("Painel 360°")
        self.botao_editar = QPushButton("✏ Editar")
        self.botao_excluir = QPushButton("🗑 Excluir")

        self.botao_novo.clicked.connect(self.abrir_dialog)
        self.botao_painel.clicked.connect(self.abrir_painel_360)
        self.botao_editar.clicked.connect(self.editar_aprendiz)
        self.botao_excluir.clicked.connect(self.excluir_aprendiz)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_painel)
        cabecalho.addWidget(self.botao_editar)
        cabecalho.addWidget(self.botao_excluir)
        cabecalho.addWidget(self.botao_novo)

        layout.addLayout(cabecalho)

        # Pesquisa
        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Pesquisar aprendiz...")
        self.pesquisa.textChanged.connect(self.filtrar_tabela)

        layout.addWidget(self.pesquisa)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Nome",
                "Código",
                "Nível",
                "Sala",
                "Dias",
                "Horário",
                "Carga ABA",
                "Status",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.tabela.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabela.doubleClicked.connect(self.editar_aprendiz)

        layout.addWidget(self.tabela)

        self.carregar_aprendizes()

    def carregar_aprendizes(self):
        self.aprendizes = self.service.listar()
        self.preencher_tabela(self.aprendizes)

    def preencher_tabela(self, lista):
        self.lista_visivel = lista
        self.tabela.setRowCount(len(lista))

        for linha, aprendiz in enumerate(lista):
            valores = [
                aprendiz.nome,
                aprendiz.codigo,
                aprendiz.nivel_suporte,
                aprendiz.sala or "",
                aprendiz.dias_atendimento or "",
                aprendiz.horario or "",
                aprendiz.carga_horaria_aba or "",
                aprendiz.status or "Ativo",
            ]

            for coluna, valor in enumerate(valores):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor)),
                )

    def filtrar_tabela(self):
        texto = self.pesquisa.text().lower().strip()

        if texto == "":
            self.preencher_tabela(self.aprendizes)
            return

        filtrados = [
            aprendiz
            for aprendiz in self.aprendizes
            if texto in aprendiz.nome.lower()
            or texto in aprendiz.codigo.lower()
            or texto in (aprendiz.sala or "").lower()
            or texto in (aprendiz.nivel_suporte or "").lower()
        ]

        self.preencher_tabela(filtrados)

    def abrir_dialog(self):
        dialog = AprendizDialog(self)

        if dialog.exec():
            self.carregar_aprendizes()

    def editar_aprendiz(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.information(
                self,
                "Editar",
                "Selecione um aprendiz.",
            )
            return

        aprendiz = self.lista_visivel[linha]

        dialog = AprendizDialog(
            self,
            aprendiz=aprendiz,
        )

        if dialog.exec():
            self.carregar_aprendizes()

    def abrir_painel_360(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.information(
                self,
                "Painel 360°",
                "Selecione um aprendiz.",
            )
            return

        self.painel_solicitado.emit(self.lista_visivel[linha])

    def excluir_aprendiz(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.information(
                self,
                "Excluir",
                "Selecione um aprendiz.",
            )
            return

        aprendiz = self.lista_visivel[linha]

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Deseja realmente excluir o aprendiz\n\n{aprendiz.nome}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        self.service.excluir(aprendiz.id)
        self.carregar_aprendizes()
