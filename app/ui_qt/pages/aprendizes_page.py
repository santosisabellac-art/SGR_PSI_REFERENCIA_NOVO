from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QHeaderView,
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
        self.botao_status = QPushButton("Inativar")
        self.botao_excluir = QPushButton("🗑 Excluir")

        self.botao_novo.clicked.connect(self.abrir_dialog)
        self.botao_painel.clicked.connect(self.abrir_painel_360)
        self.botao_editar.clicked.connect(self.editar_aprendiz)
        self.botao_status.clicked.connect(self.alterar_status)
        self.botao_excluir.clicked.connect(self.excluir_aprendiz)

        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self.botao_painel)
        cabecalho.addWidget(self.botao_editar)
        cabecalho.addWidget(self.botao_status)
        cabecalho.addWidget(self.botao_excluir)
        cabecalho.addWidget(self.botao_novo)
        layout.addLayout(cabecalho)

        filtros = QHBoxLayout()
        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Pesquisar por nome, código, sala ou nível...")
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
        self.tabela.setHorizontalHeaderLabels(["Nome", "Código", "Nível", "Sala", "Dias", "Horário", "Carga ABA", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.itemSelectionChanged.connect(self.atualizar_botoes)
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
            status = aprendiz.status or ("Ativo" if getattr(aprendiz, "ativo", True) else "Inativo")
            valores = [aprendiz.nome, aprendiz.codigo, aprendiz.nivel_suporte, aprendiz.sala or "", aprendiz.dias_atendimento or "", aprendiz.horario or "", aprendiz.carga_horaria_aba or "", status]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(valor)))
        self.resumo.setText(f"{len(lista)} aprendiz(es) exibido(s).")
        self.atualizar_botoes()

    def aplicar_filtros(self):
        texto = self.pesquisa.text().lower().strip()
        status_filtro = self.filtro_status.currentData()
        nivel_filtro = self.filtro_nivel.currentData()
        filtrados = []
        for aprendiz in self.aprendizes:
            status = (aprendiz.status or "").lower().strip() or ("ativo" if getattr(aprendiz, "ativo", True) else "inativo")
            nivel = (aprendiz.nivel_suporte or "").lower().strip()
            corresponde_texto = not texto or texto in (aprendiz.nome or "").lower() or texto in (aprendiz.codigo or "").lower() or texto in (aprendiz.sala or "").lower() or texto in nivel
            corresponde_status = status_filtro == "todos" or status == status_filtro
            corresponde_nivel = nivel_filtro == "todos" or nivel.replace("nível", "nivel") == nivel_filtro.replace("nível", "nivel")
            if corresponde_texto and corresponde_status and corresponde_nivel:
                filtrados.append(aprendiz)
        self.preencher_tabela(filtrados)

    def aprendiz_selecionado(self):
        linha = self.tabela.currentRow()
        return self.lista_visivel[linha] if 0 <= linha < len(self.lista_visivel) else None

    def atualizar_botoes(self):
        aprendiz = self.aprendiz_selecionado()
        habilitado = aprendiz is not None
        self.botao_editar.setEnabled(habilitado)
        self.botao_status.setEnabled(habilitado)
        self.botao_excluir.setEnabled(habilitado)
        self.botao_painel.setEnabled(habilitado)
        self.botao_status.setText("Reativar" if aprendiz and not getattr(aprendiz, "ativo", True) else "Inativar")

    def abrir_dialog(self):
        dialog = AprendizDialog(self)
        if dialog.exec():
            self.carregar_aprendizes()

    def editar_aprendiz(self):
        aprendiz = self.aprendiz_selecionado()
        if aprendiz is None:
            QMessageBox.information(self, "Editar", "Selecione um aprendiz.")
            return
        dialog = AprendizDialog(self, aprendiz=aprendiz)
        if dialog.exec():
            self.carregar_aprendizes()

    def alterar_status(self):
        aprendiz = self.aprendiz_selecionado()
        if aprendiz is None:
            return
        ativo_atual = getattr(aprendiz, "ativo", True)
        acao = "reativar" if not ativo_atual else "inativar"
        resposta = QMessageBox.question(self, "Alterar status", f"Deseja {acao} o aprendiz\n\n{aprendiz.nome}?", QMessageBox.Yes | QMessageBox.No)
        if resposta != QMessageBox.Yes:
            return
        self.service.alterar_status(aprendiz.id, not ativo_atual)
        self.carregar_aprendizes()

    def abrir_painel_360(self):
        aprendiz = self.aprendiz_selecionado()
        if aprendiz is None:
            QMessageBox.information(self, "Painel 360°", "Selecione um aprendiz.")
            return
        self.painel_solicitado.emit(aprendiz)

    def excluir_aprendiz(self):
        aprendiz = self.aprendiz_selecionado()
        if aprendiz is None:
            QMessageBox.information(self, "Excluir", "Selecione um aprendiz.")
            return
        resposta = QMessageBox.question(self, "Confirmar exclusão", f"Deseja realmente excluir o aprendiz\n\n{aprendiz.nome}?", QMessageBox.Yes | QMessageBox.No)
        if resposta != QMessageBox.Yes:
            return
        self.service.excluir(aprendiz.id)
        self.carregar_aprendizes()
