from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.ui_qt.theme.theme import Theme


class Header(QWidget):

    def __init__(self, titulo: str, subtitulo: str = ""):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(4)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        lbl_titulo.setStyleSheet(
            f"color: {Theme.TEXT};"
        )

        layout.addWidget(lbl_titulo)

        if subtitulo:

            lbl_subtitulo = QLabel(subtitulo)
            lbl_subtitulo.setStyleSheet(
                f"color: {Theme.TEXT_SECONDARY};"
            )

            layout.addWidget(lbl_subtitulo)