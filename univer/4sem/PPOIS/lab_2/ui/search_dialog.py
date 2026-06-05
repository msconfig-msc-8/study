from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QGroupBox, QRadioButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
    QAbstractItemView
)
from PyQt5.QtCore import Qt
from typing import List, Tuple, Any
from models.student import Student
from ui.pagination_widget import PaginationWidget

HEADERS = ["ФИО студента", "Курс", "Группа", "Общее число работ",
           "Выполнено работ", "Невыполнено работ", "Язык программирования"]


class _CriteriaWidget(QGroupBox):
    """Панель с критериями поиска — переиспользуется в обоих диалогах."""

    def __init__(self, students: List[Student], parent=None):
        super().__init__("Критерий поиска", parent)
        layout = QVBoxLayout(self)

        def make_row(rb_text, widget):
            rb = QRadioButton(rb_text)
            row = QHBoxLayout()
            row.addWidget(rb)
            row.addWidget(widget)
            layout.addLayout(row)
            return rb

        self.name_edit = QLineEdit()
        self.rb_name = make_row("По ФИО студента:", self.name_edit)

        self.group_edit = QLineEdit()
        self.rb_group = make_row("По группе:", self.group_edit)

        self.course_combo = _combo([str(v) for v in sorted(set(s.course for s in students))])
        self.rb_course = make_row("По курсу:", self.course_combo)

        self.lang_combo = _combo(sorted(set(s.language for s in students if s.language)))
        self.rb_lang = make_row("По языку программирования:", self.lang_combo)

        self.done_combo = _combo([str(v) for v in sorted(set(s.done_works for s in students))])
        self.rb_done = make_row("По кол-ву выполненных работ:", self.done_combo)

        self.total_combo = _combo([str(v) for v in sorted(set(s.total_works for s in students))])
        self.rb_total = make_row("По общему числу работ:", self.total_combo)

        self.notdone_combo = _combo([str(v) for v in sorted(set(s.not_done_works for s in students))])
        self.rb_notdone = make_row("По кол-ву НЕвыполненных работ:", self.notdone_combo)

        self.rb_name.setChecked(True)

    def get_filter(self) -> Tuple[str, Any]:
        if self.rb_name.isChecked():
            return "name", self.name_edit.text().strip()
        if self.rb_group.isChecked():
            return "group", self.group_edit.text().strip()
        if self.rb_course.isChecked():
            text = self.course_combo.currentText()
            return "course", int(text) if text else 0
        if self.rb_lang.isChecked():
            return "language", self.lang_combo.currentText()
        if self.rb_done.isChecked():
            text = self.done_combo.currentText()
            return "done_works", int(text) if text else 0
        if self.rb_total.isChecked():
            text = self.total_combo.currentText()
            return "total_works", int(text) if text else 0
        if self.rb_notdone.isChecked():
            text = self.notdone_combo.currentText()
            return "not_done", int(text) if text else 0
        return "name", ""


def _combo(items: list) -> QComboBox:
    c = QComboBox()
    c.addItems(items)
    return c


class SearchDialog(QDialog):
    """Диалог поиска — показывает результаты внутри в таблице с пагинацией."""

    def __init__(self, parent=None, students: List[Student] = None, service=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск записей")
        self.setMinimumSize(860, 580)
        self._students = students or []
        self._service = service
        self._found: List[Student] = []

        layout = QVBoxLayout(self)

        self._criteria = _CriteriaWidget(self._students)
        layout.addWidget(self._criteria)

        find_btn = QPushButton("Найти")
        find_btn.clicked.connect(self._do_search)
        layout.addWidget(find_btn)

        self._result_label = QLabel("Результаты поиска:")
        layout.addWidget(self._result_label)

        self._table = QTableWidget()
        self._table.setColumnCount(len(HEADERS))
        self._table.setHorizontalHeaderLabels(HEADERS)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, len(HEADERS)):
            self._table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        layout.addWidget(self._table)

        self._pagination = PaginationWidget()
        self._pagination.page_changed.connect(self._on_page_changed)
        layout.addWidget(self._pagination)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)

    def _do_search(self):
        if not self._service:
            return
        key, value = self._criteria.get_filter()
        self._found = self._service.search(key, value)
        self._pagination.set_total(len(self._found))
        self._result_label.setText(
            f"Результаты поиска: найдено {len(self._found)} записей"
            if self._found else "Результаты поиска: ничего не найдено"
        )

    def _on_page_changed(self, page: int, per_page: int):
        page_data = self._pagination.slice_data(self._found)
        self._table.setRowCount(0)
        for row_idx, s in enumerate(page_data):
            self._table.insertRow(row_idx)
            values = [s.name, str(s.course), s.group,
                      str(s.total_works), str(s.done_works),
                      str(s.not_done_works), s.language]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self._table.setItem(row_idx, col, item)

    def get_filter(self) -> Tuple[str, Any]:
        return self._criteria.get_filter()


class DeleteByCriteriaDialog(QDialog):
    """Отдельный диалог удаления по критерию."""

    def __init__(self, parent=None, students: List[Student] = None):
        super().__init__(parent)
        self.setWindowTitle("Удаление по критерию")
        self.setMinimumWidth(460)
        students = students or []

        layout = QVBoxLayout(self)
        self._criteria = _CriteriaWidget(students)
        layout.addWidget(self._criteria)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Удалить")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_filter(self) -> Tuple[str, Any]:
        return self._criteria.get_filter()
