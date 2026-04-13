from __future__ import annotations

import tempfile
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QLabel, QStackedLayout, QVBoxLayout, QWidget


class SvgPreviewPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._temp_file: Path | None = None

        self.info_label = QLabel("SVG preview пока не построен.")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)

        self.svg_widget = QSvgWidget()

        self.stack = QStackedLayout()
        info_page = QWidget()
        info_layout = QVBoxLayout(info_page)
        info_layout.addWidget(self.info_label)

        svg_page = QWidget()
        svg_layout = QVBoxLayout(svg_page)
        svg_layout.addWidget(self.svg_widget)

        self.stack.addWidget(info_page)
        self.stack.addWidget(svg_page)
        self.setLayout(self.stack)

    def show_message(self, message: str) -> None:
        self.info_label.setText(message)
        self.stack.setCurrentIndex(0)

    def show_svg(self, svg_text: str) -> None:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
        temp.write(svg_text.encode("utf-8"))
        temp.close()
        self._temp_file = Path(temp.name)
        self.svg_widget.load(str(self._temp_file))
        self.stack.setCurrentIndex(1)
