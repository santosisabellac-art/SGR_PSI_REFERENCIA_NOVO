from datetime import datetime
from pathlib import Path
import shutil

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QHeaderView, QLabel, QMessageBox,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from app.services.backup_service import BackupService


class ConfiguracoesPage(QWidget):

    def __init__(self):
        super().__init__()
        self.backup_service = BackupService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        titulo = QLabel("Configurações")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(titulo)

        card = QFrame()
        card.setStyleSheet("QFrame { background: white; border: 1px solid #DDDDDD; border-radius: 12px; }")
        card_layout = QVBoxLayout(card)

        titulo_backup = QLabel("Backup do SGR")
        titulo_backup.setFont(QFont("Segoe UI", 14, QFont.Bold))
        descricao = QLabel("Crie, exporte e restaure cópias locais de segurança dos dados clínicos. A restauração substitui o banco atual.")
        descricao.setWordWrap(True)

        botoes_backup = QHBoxLayout()
        self.botao_backup = QPushButton("Criar backup agora")
        self.botao_backup.clicked.connect(self.criar_backup)
        self.botao_exportar = QPushButton("Exportar backup selecionado")
        self.botao_exportar.clicked.connect(self.exportar_backup)
        self.botao_restaurar = QPushButton("Restaurar backup selecionado")
        self.botao_restaurar.clicked.connect(self.restaurar_backup)
        self.botao_exportar.setEnabled(False)
        self.botao_restaurar.setEnabled(False)
        botoes_backup.addWidget(self.botao_backup)
        botoes_backup.addWidget(self.botao_exportar)
        botoes_backup.addWidget(self.botao_restaurar)
        botoes_backup.addStretch()

        self.status_backup = QLabel()
        self.status_backup.setStyleSheet("color: #374151;")
        card_layout.addWidget(titulo_backup)
        card_layout.addWidget(descricao)
        card_layout.addLayout(botoes_backup)
        card_layout.addWidget(self.status_backup)
        layout.addWidget(card)

        cabecalho_lista = QHBoxLayout()
        titulo_lista = QLabel("Backups disponíveis")
        titulo_lista.setFont(QFont("Segoe UI", 14, QFont.Bold))
        botao_atualizar = QPushButton("Atualizar lista")
        botao_atualizar.clicked.connect(self.carregar_backups)
        cabecalho_lista.addWidget(titulo_lista)
        cabecalho_lista.addStretch()
        cabecalho_lista.addWidget(botao_atualizar)
        layout.addLayout(cabecalho_lista)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(["Arquivo", "Criado em", "Tamanho"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.itemSelectionChanged.connect(self.atualizar_acoes)
        layout.addWidget(self.tabela)
        self.carregar_backups()

    def criar_backup(self):
        try:
            arquivo = self.backup_service.criar_backup()
        except Exception as erro:
            QMessageBox.critical(self, "Backup não criado", f"Não foi possível criar o backup.\n\n{erro}")
            return
        self.status_backup.setText(f"Backup criado e validado: {arquivo.name}")
        self.carregar_backups()
        QMessageBox.information(self, "Backup criado", "A cópia de segurança foi criada e validada com sucesso.")

    def carregar_backups(self):
        backups = self.backup_service.listar_backups()
        self.tabela.setRowCount(len(backups))
        for linha, arquivo in enumerate(backups):
            criado_em = datetime.fromtimestamp(arquivo.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
            tamanho_kb = arquivo.stat().st_size / 1024
            for coluna, valor in enumerate([arquivo.name, criado_em, f"{tamanho_kb:.1f} KB"]):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(valor))
        self.atualizar_acoes()

    def atualizar_acoes(self):
        selecionado = self.tabela.currentRow() >= 0
        self.botao_exportar.setEnabled(selecionado)
        self.botao_restaurar.setEnabled(selecionado)

    def backup_selecionado(self):
        linha = self.tabela.currentRow()
        backups = self.backup_service.listar_backups()
        if linha < 0 or linha >= len(backups):
            return None
        return backups[linha]

    def exportar_backup(self):
        arquivo = self.backup_selecionado()
        if arquivo is None:
            return
        destino, _ = QFileDialog.getSaveFileName(self, "Exportar backup", str(Path.home() / arquivo.name), "Banco SQLite (*.db)")
        if not destino:
            return
        try:
            self.backup_service.validar_backup(arquivo)
            shutil.copy2(arquivo, destino)
        except Exception as erro:
            QMessageBox.critical(self, "Exportação não concluída", f"Não foi possível exportar o backup.\n\n{erro}")
            return
        QMessageBox.information(self, "Backup exportado", f"Backup salvo em:\n{destino}")

    def restaurar_backup(self):
        arquivo = self.backup_selecionado()
        if arquivo is None:
            return

        try:
            self.backup_service.validar_backup(arquivo)
        except Exception as erro:
            QMessageBox.critical(self, "Backup inválido", f"O backup não pode ser restaurado.\n\n{erro}")
            return

        confirmacao = QMessageBox.warning(
            self,
            "Confirmar restauração",
            "ATENÇÃO: a restauração substituirá todos os dados atuais pelo conteúdo deste backup.\n\nEssa ação não pode ser desfeita. Deseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirmacao != QMessageBox.Yes:
            return

        try:
            backup_atual = self.backup_service.criar_backup()
            self.backup_service.restaurar_backup(arquivo)
        except Exception as erro:
            QMessageBox.critical(self, "Restauração não concluída", f"O banco não foi restaurado.\n\n{erro}")
            return

        self.status_backup.setText(f"Banco restaurado a partir de: {arquivo.name}")
        QMessageBox.information(
            self,
            "Restauração concluída",
            "O banco foi restaurado com sucesso.\n\nUm backup do estado anterior foi criado antes da restauração.\n\nFeche e abra o SGR novamente para carregar todos os dados restaurados.",
        )
