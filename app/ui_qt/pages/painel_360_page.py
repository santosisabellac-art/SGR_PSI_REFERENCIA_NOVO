from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.aprendiz_service import AprendizService
from app.services.avaliacao_service import AvaliacaoService
from app.services.documento_service import DocumentoService
from app.services.pendencia_service import PendenciaService
from app.services.supervisao_service import SupervisaoService
from app.ui_qt.dialogs.aprendiz_dialog import AprendizDialog
from app.ui_qt.dialogs.avaliacao_dialog import AvaliacaoDialog
from app.ui_qt.dialogs.documento_dialog import DocumentoDialog
from app.ui_qt.dialogs.pendencia_dialog import PendenciaDialog
from app.ui_qt.dialogs.supervisao_dialog import SupervisaoDialog


class Painel360Page(QWidget):

    aprendiz_atualizado = Signal()

    def __init__(self, aprendiz):
        super().__init__()

        self.aprendiz = aprendiz
        self.aprendiz_service = AprendizService()
        self.avaliacao_service = AvaliacaoService()
        self.documento_service = DocumentoService()
        self.pendencia_service = PendenciaService()
        self.supervisao_service = SupervisaoService()
        self.campos = {}

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        conteudo = QWidget()
        scroll.setWidget(conteudo)
        layout_principal.addWidget(scroll)

        layout = QVBoxLayout(conteudo)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.titulo_pagina = QLabel(self.aprendiz.nome)
        self.titulo_pagina.setFont(QFont("Segoe UI", 24, QFont.Bold))

        subtitulo = QLabel("Painel 360º do Aprendiz")
        subtitulo.setStyleSheet("color:#6B7280;")

        layout.addWidget(self.titulo_pagina)
        layout.addWidget(subtitulo)

        # Pendências
        self.card_pendencias = QFrame()
        self.card_pendencias.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        pendencias_layout = QVBoxLayout(self.card_pendencias)
        pendencias_layout.setContentsMargins(18, 16, 18, 16)
        pendencias_layout.setSpacing(10)

        cabecalho_pendencias = QHBoxLayout()

        titulo_pendencias = QLabel("Pendências")
        titulo_pendencias.setFont(QFont("Segoe UI", 13, QFont.Bold))

        self.contador_pendencias = QLabel()
        self.contador_pendencias.setStyleSheet(
            "color: #6B7280; font-weight: 600;"
        )

        cabecalho_pendencias.addWidget(titulo_pendencias)
        cabecalho_pendencias.addStretch()
        cabecalho_pendencias.addWidget(self.contador_pendencias)

        pendencias_layout.addLayout(cabecalho_pendencias)

        botoes_pendencias = QHBoxLayout()

        self.botao_nova_pendencia = QPushButton("+ Nova Pendência")
        self.botao_ver_pendencias = QPushButton("Ver Pendências")

        self.botao_nova_pendencia.clicked.connect(self.abrir_nova_pendencia)
        self.botao_ver_pendencias.clicked.connect(
            self.alternar_lista_pendencias
        )

        botoes_pendencias.addWidget(self.botao_nova_pendencia)
        botoes_pendencias.addWidget(self.botao_ver_pendencias)
        botoes_pendencias.addStretch()

        pendencias_layout.addLayout(botoes_pendencias)

        self.lista_pendencias = QListWidget()
        self.lista_pendencias.setMaximumHeight(170)
        self.lista_pendencias.setVisible(False)
        self.lista_pendencias.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 7px;
            }
        """)
        self.lista_pendencias.itemSelectionChanged.connect(
            self.atualizar_acoes_pendencia
        )

        pendencias_layout.addWidget(self.lista_pendencias)

        self.acoes_pendencia = QWidget()
        acoes_pendencia_layout = QHBoxLayout(self.acoes_pendencia)
        acoes_pendencia_layout.setContentsMargins(0, 0, 0, 0)

        self.botao_concluir_pendencia = QPushButton(
            "Concluir selecionada"
        )
        self.botao_excluir_pendencia = QPushButton(
            "Excluir selecionada"
        )

        self.botao_concluir_pendencia.clicked.connect(
            self.concluir_pendencia_selecionada
        )
        self.botao_excluir_pendencia.clicked.connect(
            self.excluir_pendencia_selecionada
        )

        acoes_pendencia_layout.addWidget(self.botao_concluir_pendencia)
        acoes_pendencia_layout.addWidget(self.botao_excluir_pendencia)
        acoes_pendencia_layout.addStretch()

        self.acoes_pendencia.setVisible(False)
        pendencias_layout.addWidget(self.acoes_pendencia)

        layout.addWidget(self.card_pendencias)

        # Documentos
        self.card_documentos = QFrame()
        self.card_documentos.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        documentos_layout = QVBoxLayout(self.card_documentos)
        documentos_layout.setContentsMargins(18, 16, 18, 16)
        documentos_layout.setSpacing(10)

        cabecalho_documentos = QHBoxLayout()

        titulo_documentos = QLabel("Documentos")
        titulo_documentos.setFont(QFont("Segoe UI", 13, QFont.Bold))

        self.contador_documentos = QLabel()
        self.contador_documentos.setStyleSheet(
            "color: #6B7280; font-weight: 600;"
        )

        cabecalho_documentos.addWidget(titulo_documentos)
        cabecalho_documentos.addStretch()
        cabecalho_documentos.addWidget(self.contador_documentos)

        documentos_layout.addLayout(cabecalho_documentos)

        botoes_documentos = QHBoxLayout()

        self.botao_novo_documento = QPushButton("+ Novo Documento")
        self.botao_ver_documentos = QPushButton("Ver Documentos")

        self.botao_novo_documento.clicked.connect(self.abrir_novo_documento)
        self.botao_ver_documentos.clicked.connect(
            self.alternar_lista_documentos
        )

        botoes_documentos.addWidget(self.botao_novo_documento)
        botoes_documentos.addWidget(self.botao_ver_documentos)
        botoes_documentos.addStretch()

        documentos_layout.addLayout(botoes_documentos)

        self.lista_documentos = QListWidget()
        self.lista_documentos.setMaximumHeight(170)
        self.lista_documentos.setVisible(False)
        self.lista_documentos.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 7px;
            }
        """)

        documentos_layout.addWidget(self.lista_documentos)

        layout.addWidget(self.card_documentos)

        # Supervisões
        self.card_supervisoes = QFrame()
        self.card_supervisoes.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        supervisoes_layout = QVBoxLayout(self.card_supervisoes)
        supervisoes_layout.setContentsMargins(18, 16, 18, 16)
        supervisoes_layout.setSpacing(10)

        cabecalho_supervisoes = QHBoxLayout()

        titulo_supervisoes = QLabel("Supervisões")
        titulo_supervisoes.setFont(QFont("Segoe UI", 13, QFont.Bold))

        self.contador_supervisoes = QLabel()
        self.contador_supervisoes.setStyleSheet(
            "color: #6B7280; font-weight: 600;"
        )

        cabecalho_supervisoes.addWidget(titulo_supervisoes)
        cabecalho_supervisoes.addStretch()
        cabecalho_supervisoes.addWidget(self.contador_supervisoes)

        supervisoes_layout.addLayout(cabecalho_supervisoes)

        botoes_supervisoes = QHBoxLayout()

        self.botao_nova_supervisao = QPushButton("+ Nova Supervisão")
        self.botao_ver_supervisoes = QPushButton("Ver Histórico")

        self.botao_nova_supervisao.clicked.connect(
            self.abrir_nova_supervisao
        )
        self.botao_ver_supervisoes.clicked.connect(
            self.alternar_lista_supervisoes
        )

        botoes_supervisoes.addWidget(self.botao_nova_supervisao)
        botoes_supervisoes.addWidget(self.botao_ver_supervisoes)
        botoes_supervisoes.addStretch()

        supervisoes_layout.addLayout(botoes_supervisoes)

        self.lista_supervisoes = QListWidget()
        self.lista_supervisoes.setMaximumHeight(180)
        self.lista_supervisoes.setVisible(False)
        self.lista_supervisoes.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 7px;
            }
        """)
        self.lista_supervisoes.itemSelectionChanged.connect(
            self.atualizar_acoes_supervisao
        )

        supervisoes_layout.addWidget(self.lista_supervisoes)

        self.acoes_supervisao = QWidget()
        acoes_supervisao_layout = QHBoxLayout(self.acoes_supervisao)
        acoes_supervisao_layout.setContentsMargins(0, 0, 0, 0)

        self.botao_excluir_supervisao = QPushButton(
            "Excluir registro selecionado"
        )
        self.botao_excluir_supervisao.clicked.connect(
            self.excluir_supervisao_selecionada
        )

        acoes_supervisao_layout.addWidget(self.botao_excluir_supervisao)
        acoes_supervisao_layout.addStretch()

        self.acoes_supervisao.setVisible(False)
        supervisoes_layout.addWidget(self.acoes_supervisao)

        layout.addWidget(self.card_supervisoes)

        # Avaliações
        self.card_avaliacoes = QFrame()
        self.card_avaliacoes.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        avaliacoes_layout = QVBoxLayout(self.card_avaliacoes)
        avaliacoes_layout.setContentsMargins(18, 16, 18, 16)
        avaliacoes_layout.setSpacing(10)

        cabecalho_avaliacoes = QHBoxLayout()

        titulo_avaliacoes = QLabel("Avaliações")
        titulo_avaliacoes.setFont(QFont("Segoe UI", 13, QFont.Bold))

        self.contador_avaliacoes = QLabel()
        self.contador_avaliacoes.setStyleSheet(
            "color: #6B7280; font-weight: 600;"
        )

        cabecalho_avaliacoes.addWidget(titulo_avaliacoes)
        cabecalho_avaliacoes.addStretch()
        cabecalho_avaliacoes.addWidget(self.contador_avaliacoes)

        avaliacoes_layout.addLayout(cabecalho_avaliacoes)

        botoes_avaliacoes = QHBoxLayout()

        self.botao_nova_avaliacao = QPushButton("+ Nova Avaliação")
        self.botao_ver_avaliacoes = QPushButton("Ver Histórico")

        self.botao_nova_avaliacao.clicked.connect(self.abrir_nova_avaliacao)
        self.botao_ver_avaliacoes.clicked.connect(
            self.alternar_lista_avaliacoes
        )

        botoes_avaliacoes.addWidget(self.botao_nova_avaliacao)
        botoes_avaliacoes.addWidget(self.botao_ver_avaliacoes)
        botoes_avaliacoes.addStretch()

        avaliacoes_layout.addLayout(botoes_avaliacoes)

        self.lista_avaliacoes = QListWidget()
        self.lista_avaliacoes.setMaximumHeight(180)
        self.lista_avaliacoes.setVisible(False)
        self.lista_avaliacoes.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 7px;
            }
        """)
        self.lista_avaliacoes.itemSelectionChanged.connect(
            self.atualizar_acoes_avaliacao
        )

        avaliacoes_layout.addWidget(self.lista_avaliacoes)

        self.acoes_avaliacao = QWidget()
        acoes_avaliacao_layout = QHBoxLayout(self.acoes_avaliacao)
        acoes_avaliacao_layout.setContentsMargins(0, 0, 0, 0)

        self.botao_excluir_avaliacao = QPushButton(
            "Excluir registro selecionado"
        )
        self.botao_excluir_avaliacao.clicked.connect(
            self.excluir_avaliacao_selecionada
        )

        acoes_avaliacao_layout.addWidget(self.botao_excluir_avaliacao)
        acoes_avaliacao_layout.addStretch()

        self.acoes_avaliacao.setVisible(False)
        avaliacoes_layout.addWidget(self.acoes_avaliacao)

        layout.addWidget(self.card_avaliacoes)

        # Dados do aprendiz
        card = QFrame()

        card.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:12px;
            }
        """)

        card_layout = QVBoxLayout(card)

        def campo(titulo, valor):

            texto = QLabel(f"<b>{titulo}</b><br>{valor}")

            texto.setTextFormat(Qt.RichText)

            card_layout.addWidget(texto)
            self.campos[titulo] = texto

        campo("Código", self.aprendiz.codigo)

        campo("Nível de suporte", self.aprendiz.nivel_suporte)

        campo("Sala", self.aprendiz.sala or "-")

        campo(
            "Dias de atendimento",
            self.aprendiz.dias_atendimento or "-"
        )

        campo(
            "Horário",
            self.aprendiz.horario or "-"
        )

        campo(
            "Carga ABA",
            self.aprendiz.carga_horaria_aba or "-"
        )

        layout.addWidget(card)

        self.observacoes = QTextEdit()

        self.observacoes.setReadOnly(True)

        self.observacoes.setPlainText(
            self.aprendiz.observacoes or ""
        )

        self.observacoes.setMinimumHeight(180)

        layout.addWidget(
            QLabel("Observações")
        )

        layout.addWidget(self.observacoes)

        self.botao_editar = QPushButton(
            "✏ Editar Cadastro"
        )
        self.botao_editar.clicked.connect(self.editar_cadastro)

        layout.addWidget(self.botao_editar)

        layout.addStretch()

        self.atualizar_pendencias()
        self.atualizar_documentos()
        self.atualizar_supervisoes()
        self.atualizar_avaliacoes()

    def atualizar_pendencias(self):
        """Atualiza o contador e a lista de pendências abertas do aprendiz."""
        pendencias = self.pendencia_service.listar_por_aprendiz(
            self.aprendiz.id
        )
        pendencias_abertas = [
            pendencia
            for pendencia in pendencias
            if not pendencia.concluida
        ]

        quantidade = len(pendencias_abertas)
        if quantidade == 1:
            self.contador_pendencias.setText("1 pendência aberta")
        else:
            self.contador_pendencias.setText(
                f"{quantidade} pendências abertas"
            )

        self.lista_pendencias.clear()

        if not pendencias_abertas:
            item = QListWidgetItem("Nenhuma pendência aberta.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_pendencias.addItem(item)
            self.atualizar_acoes_pendencia()
            return

        for pendencia in pendencias_abertas:
            item = QListWidgetItem(pendencia.titulo)
            item.setData(Qt.UserRole, pendencia.id)

            if pendencia.descricao:
                item.setToolTip(pendencia.descricao)

            self.lista_pendencias.addItem(item)

        self.atualizar_acoes_pendencia()

    def abrir_nova_pendencia(self):
        dialog = PendenciaDialog(
            aprendiz_id=self.aprendiz.id,
            parent=self,
        )

        if dialog.exec():
            self.atualizar_pendencias()

    def atualizar_documentos(self):
        documentos = [
            documento
            for documento in self.documento_service.listar()
            if documento.aprendiz_id == self.aprendiz.id
            and self.documento_service.situacao(documento) != "Entregue"
        ]

        quantidade = len(documentos)
        if quantidade == 1:
            self.contador_documentos.setText("1 documento pendente")
        else:
            self.contador_documentos.setText(
                f"{quantidade} documentos pendentes"
            )

        self.lista_documentos.clear()

        if not documentos:
            item = QListWidgetItem("Nenhum documento pendente.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_documentos.addItem(item)
            return

        for documento in documentos:
            situacao = self.documento_service.situacao(documento)
            prazo = (
                documento.prazo.strftime("%d/%m/%Y")
                if documento.prazo
                else "sem prazo"
            )
            item = QListWidgetItem(
                f"{documento.tipo} — {situacao} ({prazo})"
            )

            if documento.observacoes:
                item.setToolTip(documento.observacoes)

            self.lista_documentos.addItem(item)

    def abrir_novo_documento(self):
        dialog = DocumentoDialog(
            parent=self,
            aprendiz_id=self.aprendiz.id,
        )

        if dialog.exec():
            self.atualizar_documentos()

    def alternar_lista_documentos(self):
        mostrar_lista = not self.lista_documentos.isVisible()

        if mostrar_lista:
            self.atualizar_documentos()

        self.lista_documentos.setVisible(mostrar_lista)
        self.botao_ver_documentos.setText(
            "Ocultar Documentos"
            if mostrar_lista
            else "Ver Documentos"
        )

    def atualizar_supervisoes(self):
        supervisoes = self.supervisao_service.listar_por_aprendiz(
            self.aprendiz.id
        )

        quantidade = len(supervisoes)
        if quantidade == 1:
            self.contador_supervisoes.setText("1 supervisão registrada")
        else:
            self.contador_supervisoes.setText(
                f"{quantidade} supervisões registradas"
            )

        self.lista_supervisoes.clear()

        if not supervisoes:
            item = QListWidgetItem("Nenhuma supervisão registrada.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_supervisoes.addItem(item)
            self.atualizar_acoes_supervisao()
            return

        for supervisao in supervisoes:
            item = QListWidgetItem(
                f"{supervisao.data.strftime('%d/%m/%Y')} — "
                f"{supervisao.responsavel}"
            )
            item.setData(Qt.UserRole, supervisao.id)

            detalhes = [supervisao.resumo]

            if supervisao.orientacoes:
                detalhes.append(f"Orientações: {supervisao.orientacoes}")

            if supervisao.proximos_passos:
                detalhes.append(
                    f"Próximos passos: {supervisao.proximos_passos}"
                )

            item.setToolTip("\n\n".join(detalhes))
            self.lista_supervisoes.addItem(item)

        self.atualizar_acoes_supervisao()

    def abrir_nova_supervisao(self):
        dialog = SupervisaoDialog(
            aprendiz_id=self.aprendiz.id,
            parent=self,
        )

        if dialog.exec():
            self.atualizar_supervisoes()

    def alternar_lista_supervisoes(self):
        mostrar_lista = not self.lista_supervisoes.isVisible()

        if mostrar_lista:
            self.atualizar_supervisoes()

        self.lista_supervisoes.setVisible(mostrar_lista)
        self.acoes_supervisao.setVisible(mostrar_lista)
        self.botao_ver_supervisoes.setText(
            "Ocultar Histórico"
            if mostrar_lista
            else "Ver Histórico"
        )

        self.atualizar_acoes_supervisao()

    def atualizar_acoes_supervisao(self):
        supervisao = self.lista_supervisoes.currentItem()
        habilitar_exclusao = (
            supervisao is not None
            and supervisao.data(Qt.UserRole) is not None
        )
        self.botao_excluir_supervisao.setEnabled(habilitar_exclusao)

    def excluir_supervisao_selecionada(self):
        supervisao = self.lista_supervisoes.currentItem()

        if supervisao is None:
            return

        supervisao_id = supervisao.data(Qt.UserRole)

        if supervisao_id is None:
            return

        resposta = QMessageBox.question(
            self,
            "Excluir supervisão",
            "Deseja realmente excluir o registro de supervisão selecionado?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        self.supervisao_service.excluir(supervisao_id)
        self.atualizar_supervisoes()

    def atualizar_avaliacoes(self):
        avaliacoes = self.avaliacao_service.listar_por_aprendiz(
            self.aprendiz.id
        )

        quantidade = len(avaliacoes)
        if quantidade == 1:
            self.contador_avaliacoes.setText("1 avaliação registrada")
        else:
            self.contador_avaliacoes.setText(
                f"{quantidade} avaliações registradas"
            )

        self.lista_avaliacoes.clear()

        if not avaliacoes:
            item = QListWidgetItem("Nenhuma avaliação registrada.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_avaliacoes.addItem(item)
            self.atualizar_acoes_avaliacao()
            return

        for avaliacao in avaliacoes:
            item = QListWidgetItem(
                f"{avaliacao.data.strftime('%d/%m/%Y')} — "
                f"{avaliacao.instrumento}"
            )
            item.setData(Qt.UserRole, avaliacao.id)

            detalhes = [
                f"Responsável: {avaliacao.responsavel}",
                avaliacao.sintese,
            ]

            if avaliacao.proximos_passos:
                detalhes.append(
                    f"Próximos passos: {avaliacao.proximos_passos}"
                )

            item.setToolTip("\n\n".join(detalhes))
            self.lista_avaliacoes.addItem(item)

        self.atualizar_acoes_avaliacao()

    def abrir_nova_avaliacao(self):
        dialog = AvaliacaoDialog(
            aprendiz_id=self.aprendiz.id,
            parent=self,
        )

        if dialog.exec():
            self.atualizar_avaliacoes()

    def alternar_lista_avaliacoes(self):
        mostrar_lista = not self.lista_avaliacoes.isVisible()

        if mostrar_lista:
            self.atualizar_avaliacoes()

        self.lista_avaliacoes.setVisible(mostrar_lista)
        self.acoes_avaliacao.setVisible(mostrar_lista)
        self.botao_ver_avaliacoes.setText(
            "Ocultar Histórico"
            if mostrar_lista
            else "Ver Histórico"
        )

        self.atualizar_acoes_avaliacao()

    def atualizar_acoes_avaliacao(self):
        avaliacao = self.lista_avaliacoes.currentItem()
        habilitar_exclusao = (
            avaliacao is not None
            and avaliacao.data(Qt.UserRole) is not None
        )
        self.botao_excluir_avaliacao.setEnabled(habilitar_exclusao)

    def excluir_avaliacao_selecionada(self):
        avaliacao = self.lista_avaliacoes.currentItem()

        if avaliacao is None:
            return

        avaliacao_id = avaliacao.data(Qt.UserRole)

        if avaliacao_id is None:
            return

        resposta = QMessageBox.question(
            self,
            "Excluir avaliação",
            "Deseja realmente excluir o registro de avaliação selecionado?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        self.avaliacao_service.excluir(avaliacao_id)
        self.atualizar_avaliacoes()

    def alternar_lista_pendencias(self):
        mostrar_lista = not self.lista_pendencias.isVisible()

        if mostrar_lista:
            self.atualizar_pendencias()

        self.lista_pendencias.setVisible(mostrar_lista)
        self.acoes_pendencia.setVisible(mostrar_lista)
        self.botao_ver_pendencias.setText(
            "Ocultar Pendências"
            if mostrar_lista
            else "Ver Pendências"
        )

        self.atualizar_acoes_pendencia()

    def atualizar_acoes_pendencia(self):
        pendencia_selecionada = self.lista_pendencias.currentItem()
        habilitar_acoes = (
            pendencia_selecionada is not None
            and pendencia_selecionada.data(Qt.UserRole) is not None
        )

        self.botao_concluir_pendencia.setEnabled(habilitar_acoes)
        self.botao_excluir_pendencia.setEnabled(habilitar_acoes)

    def concluir_pendencia_selecionada(self):
        pendencia = self.lista_pendencias.currentItem()

        if pendencia is None:
            return

        pendencia_id = pendencia.data(Qt.UserRole)

        if pendencia_id is None:
            return

        self.pendencia_service.concluir(pendencia_id)
        self.atualizar_pendencias()

    def excluir_pendencia_selecionada(self):
        pendencia = self.lista_pendencias.currentItem()

        if pendencia is None:
            return

        pendencia_id = pendencia.data(Qt.UserRole)

        if pendencia_id is None:
            return

        resposta = QMessageBox.question(
            self,
            "Excluir pendência",
            "Deseja realmente excluir a pendência selecionada?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        self.pendencia_service.excluir(pendencia_id)
        self.atualizar_pendencias()

    def editar_cadastro(self):
        dialog = AprendizDialog(self, aprendiz=self.aprendiz)

        if not dialog.exec():
            return

        aprendiz_atualizado = self.aprendiz_service.buscar(self.aprendiz.id)

        if aprendiz_atualizado is None:
            return

        self.aprendiz = aprendiz_atualizado
        self.atualizar_dados_aprendiz()
        self.aprendiz_atualizado.emit()

    def atualizar_dados_aprendiz(self):
        self.titulo_pagina.setText(self.aprendiz.nome)
        self.campos["Código"].setText(
            f"<b>Código</b><br>{self.aprendiz.codigo}"
        )
        self.campos["Nível de suporte"].setText(
            "<b>Nível de suporte</b><br>"
            f"{self.aprendiz.nivel_suporte}"
        )
        self.campos["Sala"].setText(
            f"<b>Sala</b><br>{self.aprendiz.sala or '-'}"
        )
        self.campos["Dias de atendimento"].setText(
            "<b>Dias de atendimento</b><br>"
            f"{self.aprendiz.dias_atendimento or '-'}"
        )
        self.campos["Horário"].setText(
            f"<b>Horário</b><br>{self.aprendiz.horario or '-'}"
        )
        self.campos["Carga ABA"].setText(
            f"<b>Carga ABA</b><br>"
            f"{self.aprendiz.carga_horaria_aba or '-'}"
        )
        self.observacoes.setPlainText(self.aprendiz.observacoes or "")
