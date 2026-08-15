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

        principal = QVBoxLayout(self)
        principal.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        conteudo = QWidget()
        scroll.setWidget(conteudo)
        principal.addWidget(scroll)

        layout = QVBoxLayout(conteudo)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        self.titulo_pagina = QLabel(self.aprendiz.nome)
        self.titulo_pagina.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(self.titulo_pagina)
        subtitulo = QLabel("Painel 360º do Aprendiz")
        subtitulo.setStyleSheet("color:#6B7280;")
        layout.addWidget(subtitulo)

        self._criar_pendencias(layout)
        self._criar_documentos(layout)
        self._criar_supervisoes(layout)
        self._criar_avaliacoes(layout)
        self._criar_dados(layout)

        self.atualizar_pendencias()
        self.atualizar_documentos()
        self.atualizar_supervisoes()
        self.atualizar_avaliacoes()

    def _criar_card(self, titulo, layout):
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background:white; border:1px solid #DDDDDD; border-radius:12px; }"
        )
        interno = QVBoxLayout(card)
        interno.setContentsMargins(18, 16, 18, 16)
        interno.setSpacing(10)
        cabecalho = QHBoxLayout()
        label = QLabel(titulo)
        label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        contador = QLabel()
        contador.setStyleSheet("color:#6B7280; font-weight:600;")
        cabecalho.addWidget(label)
        cabecalho.addStretch()
        cabecalho.addWidget(contador)
        interno.addLayout(cabecalho)
        layout.addWidget(card)
        return card, interno, contador

    def _criar_lista_acoes(self, interno, lista, botoes):
        for botao in botoes:
            pass
        lista.setMaximumHeight(180)
        lista.setVisible(False)
        lista.setStyleSheet(
            "QListWidget { border:1px solid #E5E7EB; border-radius:8px; padding:4px; }"
            "QListWidget::item { padding:7px; }"
        )
        interno.addWidget(lista)

    def _criar_pendencias(self, layout):
        self.card_pendencias, interno, self.contador_pendencias = self._criar_card("Pendências", layout)
        botoes = QHBoxLayout()
        self.botao_nova_pendencia = QPushButton("+ Nova Pendência")
        self.botao_ver_pendencias = QPushButton("Ver Pendências")
        self.botao_nova_pendencia.clicked.connect(self.abrir_nova_pendencia)
        self.botao_ver_pendencias.clicked.connect(self.alternar_lista_pendencias)
        botoes.addWidget(self.botao_nova_pendencia)
        botoes.addWidget(self.botao_ver_pendencias)
        botoes.addStretch()
        interno.addLayout(botoes)
        self.lista_pendencias = QListWidget()
        self.lista_pendencias.itemSelectionChanged.connect(self.atualizar_acoes_pendencia)
        self._criar_lista_acoes(interno, self.lista_pendencias, [])
        self.acoes_pendencia = QWidget()
        acoes = QHBoxLayout(self.acoes_pendencia)
        acoes.setContentsMargins(0, 0, 0, 0)
        self.botao_editar_pendencia = QPushButton("✏ Editar selecionada")
        self.botao_concluir_pendencia = QPushButton("Concluir selecionada")
        self.botao_excluir_pendencia = QPushButton("Excluir selecionada")
        self.botao_editar_pendencia.clicked.connect(self.editar_pendencia_selecionada)
        self.botao_concluir_pendencia.clicked.connect(self.concluir_pendencia_selecionada)
        self.botao_excluir_pendencia.clicked.connect(self.excluir_pendencia_selecionada)
        acoes.addWidget(self.botao_editar_pendencia)
        acoes.addWidget(self.botao_concluir_pendencia)
        acoes.addWidget(self.botao_excluir_pendencia)
        acoes.addStretch()
        self.acoes_pendencia.setVisible(False)
        interno.addWidget(self.acoes_pendencia)

    def _criar_documentos(self, layout):
        self.card_documentos, interno, self.contador_documentos = self._criar_card("Documentos", layout)
        botoes = QHBoxLayout()
        self.botao_novo_documento = QPushButton("+ Novo Documento")
        self.botao_ver_documentos = QPushButton("Ver Documentos")
        self.botao_novo_documento.clicked.connect(self.abrir_novo_documento)
        self.botao_ver_documentos.clicked.connect(self.alternar_lista_documentos)
        botoes.addWidget(self.botao_novo_documento)
        botoes.addWidget(self.botao_ver_documentos)
        botoes.addStretch()
        interno.addLayout(botoes)
        self.lista_documentos = QListWidget()
        self._criar_lista_acoes(interno, self.lista_documentos, [])

    def _criar_supervisoes(self, layout):
        self.card_supervisoes, interno, self.contador_supervisoes = self._criar_card("Supervisões", layout)
        botoes = QHBoxLayout()
        self.botao_nova_supervisao = QPushButton("+ Nova Supervisão")
        self.botao_ver_supervisoes = QPushButton("Ver Histórico")
        self.botao_nova_supervisao.clicked.connect(self.abrir_nova_supervisao)
        self.botao_ver_supervisoes.clicked.connect(self.alternar_lista_supervisoes)
        botoes.addWidget(self.botao_nova_supervisao)
        botoes.addWidget(self.botao_ver_supervisoes)
        botoes.addStretch()
        interno.addLayout(botoes)
        self.lista_supervisoes = QListWidget()
        self.lista_supervisoes.itemSelectionChanged.connect(self.atualizar_acoes_supervisao)
        self._criar_lista_acoes(interno, self.lista_supervisoes, [])
        self.acoes_supervisao = QWidget()
        acoes = QHBoxLayout(self.acoes_supervisao)
        acoes.setContentsMargins(0, 0, 0, 0)
        self.botao_excluir_supervisao = QPushButton("Excluir registro selecionado")
        self.botao_excluir_supervisao.clicked.connect(self.excluir_supervisao_selecionada)
        acoes.addWidget(self.botao_excluir_supervisao)
        acoes.addStretch()
        self.acoes_supervisao.setVisible(False)
        interno.addWidget(self.acoes_supervisao)

    def _criar_avaliacoes(self, layout):
        self.card_avaliacoes, interno, self.contador_avaliacoes = self._criar_card("Avaliações", layout)
        botoes = QHBoxLayout()
        self.botao_nova_avaliacao = QPushButton("+ Nova Avaliação")
        self.botao_ver_avaliacoes = QPushButton("Ver Histórico")
        self.botao_nova_avaliacao.clicked.connect(self.abrir_nova_avaliacao)
        self.botao_ver_avaliacoes.clicked.connect(self.alternar_lista_avaliacoes)
        botoes.addWidget(self.botao_nova_avaliacao)
        botoes.addWidget(self.botao_ver_avaliacoes)
        botoes.addStretch()
        interno.addLayout(botoes)
        self.lista_avaliacoes = QListWidget()
        self.lista_avaliacoes.itemSelectionChanged.connect(self.atualizar_acoes_avaliacao)
        self._criar_lista_acoes(interno, self.lista_avaliacoes, [])
        self.acoes_avaliacao = QWidget()
        acoes = QHBoxLayout(self.acoes_avaliacao)
        acoes.setContentsMargins(0, 0, 0, 0)
        self.botao_excluir_avaliacao = QPushButton("Excluir registro selecionado")
        self.botao_excluir_avaliacao.clicked.connect(self.excluir_avaliacao_selecionada)
        acoes.addWidget(self.botao_excluir_avaliacao)
        acoes.addStretch()
        self.acoes_avaliacao.setVisible(False)
        interno.addWidget(self.acoes_avaliacao)

    def _criar_dados(self, layout):
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background:white; border:1px solid #DDDDDD; border-radius:12px; }"
        )
        interno = QVBoxLayout(card)
        self.campos = {}
        for titulo, valor in [
            ("Código", self.aprendiz.codigo),
            ("Nível de suporte", self.aprendiz.nivel_suporte),
            ("Sala", self.aprendiz.sala or "-"),
            ("Dias de atendimento", self.aprendiz.dias_atendimento or "-"),
            ("Horário", self.aprendiz.horario or "-"),
            ("Carga ABA", self.aprendiz.carga_horaria_aba or "-"),
        ]:
            campo = QLabel(f"<b>{titulo}</b><br>{valor}")
            campo.setTextFormat(Qt.RichText)
            interno.addWidget(campo)
            self.campos[titulo] = campo
        interno.addWidget(QLabel("Observações"))
        self.observacoes = QTextEdit()
        self.observacoes.setReadOnly(True)
        self.observacoes.setMinimumHeight(160)
        self.observacoes.setPlainText(self.aprendiz.observacoes or "")
        interno.addWidget(self.observacoes)
        self.botao_editar = QPushButton("✏ Editar Cadastro")
        self.botao_editar.clicked.connect(self.editar_cadastro)
        interno.addWidget(self.botao_editar)
        layout.addWidget(card)

    def atualizar_pendencias(self):
        pendencias = [p for p in self.pendencia_service.listar_por_aprendiz(self.aprendiz.id) if not p.concluida]
        self.contador_pendencias.setText("1 pendência aberta" if len(pendencias) == 1 else f"{len(pendencias)} pendências abertas")
        self.lista_pendencias.clear()
        if not pendencias:
            item = QListWidgetItem("Nenhuma pendência aberta.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_pendencias.addItem(item)
        else:
            for pendencia in pendencias:
                item = QListWidgetItem(pendencia.titulo)
                item.setData(Qt.UserRole, pendencia.id)
                item.setToolTip(pendencia.descricao or "")
                self.lista_pendencias.addItem(item)
        self.atualizar_acoes_pendencia()

    def abrir_nova_pendencia(self):
        dialog = PendenciaDialog(self.aprendiz.id, parent=self)
        if dialog.exec():
            self.atualizar_pendencias()

    def editar_pendencia_selecionada(self):
        item = self.lista_pendencias.currentItem()
        if item is None or item.data(Qt.UserRole) is None:
            return
        pendencia_id = item.data(Qt.UserRole)
        pendencia = next((p for p in self.pendencia_service.listar_por_aprendiz(self.aprendiz.id) if p.id == pendencia_id), None)
        if pendencia is None:
            return
        dialog = PendenciaDialog(self.aprendiz.id, parent=self, pendencia=pendencia)
        if dialog.exec():
            self.atualizar_pendencias()

    def alternar_lista_pendencias(self):
        mostrar = not self.lista_pendencias.isVisible()
        if mostrar:
            self.atualizar_pendencias()
        self.lista_pendencias.setVisible(mostrar)
        self.acoes_pendencia.setVisible(mostrar)
        self.botao_ver_pendencias.setText("Ocultar Pendências" if mostrar else "Ver Pendências")
        self.atualizar_acoes_pendencia()

    def atualizar_acoes_pendencia(self):
        habilitar = self.lista_pendencias.currentItem() is not None and self.lista_pendencias.currentItem().data(Qt.UserRole) is not None
        self.botao_editar_pendencia.setEnabled(habilitar)
        self.botao_concluir_pendencia.setEnabled(habilitar)
        self.botao_excluir_pendencia.setEnabled(habilitar)

    def concluir_pendencia_selecionada(self):
        item = self.lista_pendencias.currentItem()
        if item is not None and item.data(Qt.UserRole) is not None:
            self.pendencia_service.concluir(item.data(Qt.UserRole))
            self.atualizar_pendencias()

    def excluir_pendencia_selecionada(self):
        item = self.lista_pendencias.currentItem()
        if item is None or item.data(Qt.UserRole) is None:
            return
        if QMessageBox.question(self, "Excluir pendência", "Deseja realmente excluir a pendência selecionada?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.pendencia_service.excluir(item.data(Qt.UserRole))
        self.atualizar_pendencias()

    def atualizar_documentos(self):
        documentos = [d for d in self.documento_service.listar() if d.aprendiz_id == self.aprendiz.id and self.documento_service.situacao(d) != "Entregue"]
        self.contador_documentos.setText("1 documento pendente" if len(documentos) == 1 else f"{len(documentos)} documentos pendentes")
        self.lista_documentos.clear()
        if not documentos:
            item = QListWidgetItem("Nenhum documento pendente.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_documentos.addItem(item)
            return
        for documento in documentos:
            situacao = self.documento_service.situacao(documento)
            prazo = documento.prazo.strftime("%d/%m/%Y") if documento.prazo else "sem prazo"
            item = QListWidgetItem(f"{documento.tipo} — {situacao} ({prazo})")
            item.setToolTip(documento.observacoes or "")
            self.lista_documentos.addItem(item)

    def abrir_novo_documento(self):
        dialog = DocumentoDialog(parent=self, aprendiz_id=self.aprendiz.id)
        if dialog.exec():
            self.atualizar_documentos()

    def alternar_lista_documentos(self):
        mostrar = not self.lista_documentos.isVisible()
        if mostrar:
            self.atualizar_documentos()
        self.lista_documentos.setVisible(mostrar)
        self.botao_ver_documentos.setText("Ocultar Documentos" if mostrar else "Ver Documentos")

    def atualizar_supervisoes(self):
        supervisoes = self.supervisao_service.listar_por_aprendiz(self.aprendiz.id)
        self.contador_supervisoes.setText("1 supervisão registrada" if len(supervisoes) == 1 else f"{len(supervisoes)} supervisões registradas")
        self.lista_supervisoes.clear()
        if not supervisoes:
            item = QListWidgetItem("Nenhuma supervisão registrada.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_supervisoes.addItem(item)
        else:
            for supervisao in supervisoes:
                item = QListWidgetItem(f"{supervisao.data.strftime('%d/%m/%Y')} — {supervisao.responsavel}")
                item.setData(Qt.UserRole, supervisao.id)
                detalhes = [supervisao.resumo]
                if supervisao.orientacoes:
                    detalhes.append(f"Orientações: {supervisao.orientacoes}")
                if supervisao.proximos_passos:
                    detalhes.append(f"Próximos passos: {supervisao.proximos_passos}")
                item.setToolTip("\n\n".join(detalhes))
                self.lista_supervisoes.addItem(item)
        self.atualizar_acoes_supervisao()

    def abrir_nova_supervisao(self):
        dialog = SupervisaoDialog(self.aprendiz.id, parent=self)
        if dialog.exec():
            self.atualizar_supervisoes()

    def alternar_lista_supervisoes(self):
        mostrar = not self.lista_supervisoes.isVisible()
        if mostrar:
            self.atualizar_supervisoes()
        self.lista_supervisoes.setVisible(mostrar)
        self.acoes_supervisao.setVisible(mostrar)
        self.botao_ver_supervisoes.setText("Ocultar Histórico" if mostrar else "Ver Histórico")
        self.atualizar_acoes_supervisao()

    def atualizar_acoes_supervisao(self):
        self.botao_excluir_supervisao.setEnabled(self.lista_supervisoes.currentItem() is not None and self.lista_supervisoes.currentItem().data(Qt.UserRole) is not None)

    def excluir_supervisao_selecionada(self):
        item = self.lista_supervisoes.currentItem()
        if item is None or item.data(Qt.UserRole) is None:
            return
        if QMessageBox.question(self, "Excluir supervisão", "Deseja realmente excluir o registro selecionado?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.supervisao_service.excluir(item.data(Qt.UserRole))
        self.atualizar_supervisoes()

    def atualizar_avaliacoes(self):
        avaliacoes = self.avaliacao_service.listar_por_aprendiz(self.aprendiz.id)
        self.contador_avaliacoes.setText("1 avaliação registrada" if len(avaliacoes) == 1 else f"{len(avaliacoes)} avaliações registradas")
        self.lista_avaliacoes.clear()
        if not avaliacoes:
            item = QListWidgetItem("Nenhuma avaliação registrada.")
            item.setFlags(Qt.NoItemFlags)
            self.lista_avaliacoes.addItem(item)
        else:
            for avaliacao in avaliacoes:
                item = QListWidgetItem(f"{avaliacao.data.strftime('%d/%m/%Y')} — {avaliacao.instrumento}")
                item.setData(Qt.UserRole, avaliacao.id)
                detalhes = [f"Responsável: {avaliacao.responsavel}", avaliacao.sintese]
                if avaliacao.proximos_passos:
                    detalhes.append(f"Próximos passos: {avaliacao.proximos_passos}")
                item.setToolTip("\n\n".join(detalhes))
                self.lista_avaliacoes.addItem(item)
        self.atualizar_acoes_avaliacao()

    def abrir_nova_avaliacao(self):
        dialog = AvaliacaoDialog(self.aprendiz.id, parent=self)
        if dialog.exec():
            self.atualizar_avaliacoes()

    def alternar_lista_avaliacoes(self):
        mostrar = not self.lista_avaliacoes.isVisible()
        if mostrar:
            self.atualizar_avaliacoes()
        self.lista_avaliacoes.setVisible(mostrar)
        self.acoes_avaliacao.setVisible(mostrar)
        self.botao_ver_avaliacoes.setText("Ocultar Histórico" if mostrar else "Ver Histórico")
        self.atualizar_acoes_avaliacao()

    def atualizar_acoes_avaliacao(self):
        self.botao_excluir_avaliacao.setEnabled(self.lista_avaliacoes.currentItem() is not None and self.lista_avaliacoes.currentItem().data(Qt.UserRole) is not None)

    def excluir_avaliacao_selecionada(self):
        item = self.lista_avaliacoes.currentItem()
        if item is None or item.data(Qt.UserRole) is None:
            return
        if QMessageBox.question(self, "Excluir avaliação", "Deseja realmente excluir o registro selecionado?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.avaliacao_service.excluir(item.data(Qt.UserRole))
        self.atualizar_avaliacoes()

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
        self.campos["Código"].setText(f"<b>Código</b><br>{self.aprendiz.codigo}")
        self.campos["Nível de suporte"].setText(f"<b>Nível de suporte</b><br>{self.aprendiz.nivel_suporte}")
        self.campos["Sala"].setText(f"<b>Sala</b><br>{self.aprendiz.sala or '-'}")
        self.campos["Dias de atendimento"].setText(f"<b>Dias de atendimento</b><br>{self.aprendiz.dias_atendimento or '-'}")
        self.campos["Horário"].setText(f"<b>Horário</b><br>{self.aprendiz.horario or '-'}")
        self.campos["Carga ABA"].setText(f"<b>Carga ABA</b><br>{self.aprendiz.carga_horaria_aba or '-'}")
        self.observacoes.setPlainText(self.aprendiz.observacoes or "")
