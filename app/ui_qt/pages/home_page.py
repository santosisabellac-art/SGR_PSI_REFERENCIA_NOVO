from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel("Bem-vinda, Isabella 👋")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))

        subtitulo = QLabel(
            "Sistema de Gestão da Psicóloga de Referência"
        )
        subtitulo.setStyleSheet("color: #6B7280;")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        layout.addSpacing(30)

        aviso = QLabel(
            "Primeiro módulo em desenvolvimento:\n\n👤 Aprendizes"
        )
        aviso.setAlignment(Qt.AlignCenter)
        aviso.setStyleSheet("""
            font-size:18px;
            border:1px solid #DDDDDD;
            border-radius:10px;
            padding:30px;
            background:#FFFFFF;
        """)

        layout.addWidget(aviso)

        layout.addStretch()