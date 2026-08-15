from datetime import datetime
from pathlib import Path
import shutil

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
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
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)

        titulo_backup = QLabel("Backup do SGR")
        titulo_backup.setFont(QFont("Segoe UI", 14, QFont.Bold))

        descricao = QLabel(
            "Crie uma cópia local de segurança dos dados clínicos. "
            "Os backups ficam na pasta 'backups' dentro do projeto."
        )
        descricao.setWordWrap(True)

        botoes_backup = QHBoxLayout()

        self.botao_backup = QPushButton("Criar backup agora")
        self.botao_backup.clicked.connect(self.criar_backup)

        self.botao_exportar = QPushButton("Exportar backup selecionado")
        self.botao_exportar.clicked.connect(self.exportar_backup)
        self.botao_exportar.setEnabled(False)

        botoes_backup.addWidget(self.botao_backup)
        botoes_backup.addWidget(self.botao_exportar)
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
        self.tabela.setHorizontalHeaderLabels(
            ["Arquivo", "Criado em", "Tamanho"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
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
            QMessageBox.critical(
                self,
                "Backup não criado",
                f"Não foi possível criar o backup.\n\n{erro}",
            )
            return

        self.status_backup.setText(
            f"Backup criado com sucesso: {arquivo.name}"
        )
        self.carregar_backups()

        QMessageBox.information(
            self,
            "Backup criado",
            "A cópia de segurança foi criada com sucesso.",
        )

    def carregar_backups(self):
        backups = self.backup_service.listar_backups()
        self.tabela.setRowCount(len(backups))

        for linha, arquivo in enumerate(backups):
            criado_em = datetime.fromtimestamp(
                arquivo.stat().st_mtime
            ).strftime("%d/%m/%Y %H:%M")
            tamanho_kb = arquivo.stat().st_size / 1024

            valores = [
                arquivo.name,
                criado_em,
                f"{tamanho_kb:.1f} KB",
            ]

            for coluna, valor in enumerate(valores):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor),
                )

        self.atualizar_acoes()

    def atualizar_acoes(self):
        self.botao_exportar.setEnabled(
            self.tabela.currentRow() >= 0
        )

    def backup_selecionado(self):
        linha = self.tabela.currentRow()
        backups = self.backup_service.listar_backups()

        if linha < 0 or linha >= len(backups):
            return None

        return backups[linha]

    def exportar_backup(self):
        arquivo = self.backup_selecionado()

        if arquivo is None:
            QMessageBox.information(
                self,
                "Selecionar backup",
                "Selecione um backup na lista antes de exportar.",
            )
            return

        destino, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar backup",
            str(Path.home() / arquivo.name),
            "Banco SQLite (*.db)",
        )

        if not destino:
            return

        try:
            shutil.copy2(arquivo, destino)
        except Exception as erro:
            QMessageBox.critical(
                self,
                "Exportação não concluída",
                f"Não foi possível exportar o backup.\n\n{erro}",
            )
            return

        QMessageBox.information(
            self,
            "Backup exportado",
            f"Backup salvo em:\n{destino}",
        )
