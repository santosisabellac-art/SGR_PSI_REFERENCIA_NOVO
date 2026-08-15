import sqlite3
from datetime import datetime
from pathlib import Path


class BackupService:

    def __init__(self, projeto_path=None):
        if projeto_path is None:
            projeto_path = Path(__file__).resolve().parents[2]

        self.projeto_path = Path(projeto_path)
        self.banco_path = self.projeto_path / "database" / "sgr_psicologa.db"
        self.backups_path = self.projeto_path / "backups"

    def criar_backup(self):
        if not self.banco_path.exists():
            raise FileNotFoundError("Banco de dados do SGR não encontrado.")

        self.backups_path.mkdir(parents=True, exist_ok=True)
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        destino = self.backups_path / f"sgr_backup_{data_hora}.db"

        with sqlite3.connect(self.banco_path) as origem:
            with sqlite3.connect(destino) as copia:
                origem.backup(copia)

        self.validar_backup(destino)
        return destino

    def listar_backups(self):
        if not self.backups_path.exists():
            return []

        return sorted(
            self.backups_path.glob("sgr_backup_*.db"),
            key=lambda arquivo: arquivo.stat().st_mtime,
            reverse=True,
        )

    def validar_backup(self, arquivo):
        arquivo = Path(arquivo)
        if not arquivo.exists() or arquivo.stat().st_size == 0:
            raise ValueError("O arquivo de backup está vazio ou não existe.")

        with sqlite3.connect(arquivo) as conexao:
            resultado = conexao.execute("PRAGMA integrity_check").fetchone()

        if not resultado or resultado[0] != "ok":
            raise ValueError("O backup não passou na verificação de integridade do SQLite.")

        return True
