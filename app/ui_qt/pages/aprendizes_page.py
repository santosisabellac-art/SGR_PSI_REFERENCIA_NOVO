from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
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
        layout.setSpacing(12)

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

        filtros = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText(
            "Pesquisar por nome, código, sala ou nível..."
        )
        self.pesquisa.textChanged.connect(self.aplicar_filtros)

        self.filtro_status = QComboBox()
        self.filtro_status.addItem("Todos os status", "todos")
        self.filtro_status.addItem("Ativos", "ativo")
        self.filtro_status.addItem("Inativos", "inativo")
        self.filtro_status.currentIndexChanged.connect(self.aplicar_filtros)

        self.filtro_nivel = QComboBox()
        self.filtro_nivel.addItem("Todos os níveis", "todos")
        self.filtro_nivel.addItem("Nível 1", "nível 1")
        self.filtro_nivel.addItem("Nível 2", "nível 2")
        self.filtro_nivel.addItem("Nível 3", "nível 3")
        self.filtro_nivel.currentIndexChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.pesquisa, 1)
        filtros.addWidget(self.filtro_status)
        filtros.addWidget(self.filtro_nivel)

        layout.addLayout(filtros)

        self.resumo = QLabel()
        self.resumo.setStyleSheet("color: #374151; font-weight: 600;")
        layout.addWidget(self.resumo)

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
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.doubleClicked.connect(self.editar_aprendiz)

        layout.addWidget(self.tabela)

        self.carregar_aprendizes()

    def carregar_aprendizes(self):
        self.aprendizes = self.service.listar()
        self.aplicar_filtros()

    def preencher_tabela(self, lista):
        self.lista_visivel = lista
        self.tabela.setRowCount(len(lista))

        for linha, aprendiz in enumerate(lista):
            status = aprendiz.status or (
                "Ativo" if getattr(aprendiz, "ativo", True) else "Inativo"
            )

            valores = [
                aprendiz.nome,
                aprendiz.codigo,
                aprendiz.nivel_suporte,
                aprendiz.sala or "",
                aprendiz.dias_atendimento or "",
                aprendiz.horario or "",
                aprendiz.carga_horaria_aba or "",
                status,
            ]

            for coluna, valor in enumerate(valores):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor)),
                )

        self.resumo.setText(f"{len(lista)} aprendiz(es) exibido(s).")

    def aplicar_filtros(self):
        texto = self.pesquisa.text().lower().strip()
        status_filtro = self.filtro_status.currentData()
        nivel_filtro = self.filtro_nivel.currentData()

        filtrados = []

        for aprendiz in self.aprendizes:
            status = (aprendiz.status or "").lower().strip()
            if not status:
                status = "ativo" if getattr(aprendiz, "ativo", True) else "inativo"

            nivel = (aprendiz.nivel_suporte or "").lower().strip()

            corresponde_texto = (
                not texto
                or texto in (aprendiz.nome or "").lower()
                or texto in (aprendiz.codigo or "").lower()
                or texto in (aprendiz.sala or "").lower()
                or texto in nivel
            )

            corresponde_status = (
                status_filtro == "todos"
                or status == status_filtro
            )

            corresponde_nivel = (
                nivel_filtro == "todos"
                or nivel == nivel_filtro
                or nivel.replace("nível", "nivel")
                == nivel_filtro.replace("nível", "nivel")
            )

            if corresponde_texto and corresponde_status and corresponde_nivel:
                filtrados.append(aprendiz)

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
        dialog = AprendizDialog(self, aprendiz=aprendiz)

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
