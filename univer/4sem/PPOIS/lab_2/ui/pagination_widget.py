from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QSpinBox, QComboBox
)
from PyQt5.QtCore import pyqtSignal, Qt
from typing import List


class PaginationWidget(QWidget):
    """Панель управления страницами. Сигнал page_changed(page, per_page)."""

    page_changed = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._total = 0
        self._page = 1
        self._per_page = 10

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)

        self._first_btn = QPushButton("|<")
        self._prev_btn  = QPushButton("<")
        self._next_btn  = QPushButton(">")
        self._last_btn  = QPushButton(">|")

        for btn in (self._first_btn, self._prev_btn, self._next_btn, self._last_btn):
            btn.setFixedWidth(32)

        self._first_btn.clicked.connect(self._go_first)
        self._prev_btn.clicked.connect(self._go_prev)
        self._next_btn.clicked.connect(self._go_next)
        self._last_btn.clicked.connect(self._go_last)

        self._page_label = QLabel()
        self._total_label = QLabel()

        layout.addWidget(self._first_btn)
        layout.addWidget(self._prev_btn)
        layout.addWidget(self._page_label)
        layout.addWidget(self._next_btn)
        layout.addWidget(self._last_btn)
        layout.addSpacing(16)
        layout.addWidget(QLabel("На странице:"))

        self._per_page_combo = QComboBox()
        self._per_page_combo.addItems(["5", "10", "20", "50"])
        self._per_page_combo.setCurrentText("10")
        self._per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        layout.addWidget(self._per_page_combo)

        layout.addSpacing(16)
        layout.addWidget(self._total_label)
        layout.addStretch()

        self._update_ui()

    # ── public ────────────────────────────────────────────────────────────────

    def set_total(self, total: int):
        self._total = total
        if self._page > self._total_pages():
            self._page = max(1, self._total_pages())
        self._update_ui()
        self.page_changed.emit(self._page, self._per_page)

    @property
    def page(self) -> int:
        return self._page

    @property
    def per_page(self) -> int:
        return self._per_page

    def slice_data(self, data: list) -> list:
        start = (self._page - 1) * self._per_page
        return data[start:start + self._per_page]

    # ── slots ─────────────────────────────────────────────────────────────────

    def _go_first(self):
        self._set_page(1)

    def _go_prev(self):
        self._set_page(self._page - 1)

    def _go_next(self):
        self._set_page(self._page + 1)

    def _go_last(self):
        self._set_page(self._total_pages())

    def _on_per_page_changed(self, text: str):
        if text:
            self._per_page = int(text)
            self._page = 1
            self._update_ui()
            self.page_changed.emit(self._page, self._per_page)

    # ── private ───────────────────────────────────────────────────────────────

    def _set_page(self, page: int):
        pages = self._total_pages()
        self._page = max(1, min(page, pages))
        self._update_ui()
        self.page_changed.emit(self._page, self._per_page)

    def _total_pages(self) -> int:
        if self._total == 0:
            return 1
        return (self._total + self._per_page - 1) // self._per_page

    def _update_ui(self):
        pages = self._total_pages()
        self._page_label.setText(f"Стр. {self._page} из {pages}")
        self._total_label.setText(f"Всего записей: {self._total}")
        self._first_btn.setEnabled(self._page > 1)
        self._prev_btn.setEnabled(self._page > 1)
        self._next_btn.setEnabled(self._page < pages)
        self._last_btn.setEnabled(self._page < pages)
