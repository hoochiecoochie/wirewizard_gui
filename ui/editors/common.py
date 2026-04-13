from __future__ import annotations

from PySide6.QtWidgets import QComboBox


def build_combo(values: list[str], editable: bool = True) -> QComboBox:
    combo = QComboBox()
    combo.addItems(values)
    combo.setEditable(editable)
    combo.setInsertPolicy(QComboBox.NoInsert)
    return combo


def set_combo_text(combo: QComboBox, value: str) -> None:
    idx = combo.findText(value)
    if idx >= 0:
        combo.setCurrentIndex(idx)
    else:
        combo.setEditText(value)
