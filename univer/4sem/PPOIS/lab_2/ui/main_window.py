from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel,
    QMessageBox, QHeaderView, QAbstractItemView, QDialog,
    QFileDialog, QAction, QToolBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.student import Student
from services.student_service import StudentService
from ui.student_dialog import StudentDialog
from ui.search_dialog import SearchDialog, DeleteByCriteriaDialog
from ui.pagination_widget import PaginationWidget

HEADERS = ["ФИО студента", "Курс", "Группа", "Общее число работ",
           "Выполнено работ", "Невыполнено работ", "Язык программирования"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учёт студенческих работ — Вариант 14")
        self.setMinimumSize(980, 600)
        self._service = StudentService()
        self._build_menu()
        self._build_toolbar()
        self._build_central()
        self._reload()

    # ── menu ──────────────────────────────────────────────────────────────────

    def _build_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")
        self._act_open   = self._action("Открыть...",       "Ctrl+O",       file_menu, self._on_open)
        self._act_save   = self._action("Сохранить",        "Ctrl+S",       file_menu, self._on_save)
        self._act_saveas = self._action("Сохранить как...", "Ctrl+Shift+S", file_menu, self._on_save_as)
        file_menu.addSeparator()
        self._action("Выход", "Alt+F4", file_menu, self.close)

        edit_menu = menubar.addMenu("Правка")
        self._act_add     = self._action("Добавить запись",      "Ctrl+N", edit_menu, self._on_add)
        self._act_edit    = self._action("Редактировать запись", "Ctrl+E", edit_menu, self._on_edit)
        self._act_delete  = self._action("Удалить запись",       "Delete", edit_menu, self._on_delete)
        edit_menu.addSeparator()
        self._act_search  = self._action("Поиск...",                  "Ctrl+F", edit_menu, self._on_search)
        self._act_delcrit = self._action("Удаление по критерию...",   "Ctrl+D", edit_menu, self._on_delete_by_criteria)

    @staticmethod
    def _action(title, shortcut, menu, slot) -> QAction:
        act = QAction(title)
        act.setShortcut(shortcut)
        act.triggered.connect(slot)
        menu.addAction(act)
        return act

    # ── toolbar ───────────────────────────────────────────────────────────────

    def _build_toolbar(self):
        tb = QToolBar("Основные действия")
        tb.setMovable(False)
        self.addToolBar(tb)
        for act in (self._act_open, self._act_save, self._act_saveas):
            tb.addAction(act)
        tb.addSeparator()
        for act in (self._act_add, self._act_edit, self._act_delete):
            tb.addAction(act)
        tb.addSeparator()
        for act in (self._act_search, self._act_delcrit):
            tb.addAction(act)

    # ── central widget ────────────────────────────────────────────────────────

    def _build_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 4)

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

    # ── helpers ───────────────────────────────────────────────────────────────

    def _reload(self):
        """Перезагружает пагинацию и таблицу из сервиса."""
        all_data = self._service.get_all()
        self._pagination.set_total(len(all_data))

    def _on_page_changed(self, page: int, per_page: int):
        all_data = self._service.get_all()
        page_data = self._pagination.slice_data(all_data)
        self._fill_table(page_data)

    def _fill_table(self, students: list):
        self._table.setRowCount(0)
        for row_idx, s in enumerate(students):
            self._table.insertRow(row_idx)
            values = [s.name, str(s.course), s.group,
                      str(s.total_works), str(s.done_works),
                      str(s.not_done_works), s.language]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self._table.setItem(row_idx, col, item)

    def _update_title(self):
        path = self._service.filepath
        name = path.replace("\\", "/").split("/")[-1] if path else "Без имени"
        self.setWindowTitle(f"Учёт студенческих работ — {name}")

    def _selected_global_row(self) -> int:
        """Возвращает глобальный индекс выбранной строки с учётом текущей страницы."""
        row = self._table.currentRow()
        if row < 0:
            return -1
        return (self._pagination.page - 1) * self._pagination.per_page + row

    # ── file actions ──────────────────────────────────────────────────────────

    def _on_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "XML файлы (*.xml)")
        if not path:
            return
        try:
            self._service.load(path)
            self._reload()
            self._update_title()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def _on_save(self):
        if not self._service.filepath:
            self._on_save_as()
            return
        try:
            self._service.save()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить:\n{e}")

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "XML файлы (*.xml)")
        if not path:
            return
        if not path.endswith(".xml"):
            path += ".xml"
        try:
            self._service.save(path)
            self._update_title()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить:\n{e}")

    # ── record actions ────────────────────────────────────────────────────────

    def _on_add(self):
        dlg = StudentDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._service.add(dlg.get_student())
            self._reload()

    def _on_edit(self):
        idx = self._selected_global_row()
        if idx < 0:
            QMessageBox.information(self, "Внимание", "Выберите строку для редактирования.")
            return
        dlg = StudentDialog(self, self._service.get_all()[idx])
        if dlg.exec_() == QDialog.Accepted:
            self._service.update(idx, dlg.get_student())
            self._reload()

    def _on_delete(self):
        idx = self._selected_global_row()
        if idx < 0:
            QMessageBox.information(self, "Внимание", "Выберите строку для удаления.")
            return
        name = self._service.get_all()[idx].name
        if QMessageBox.question(self, "Подтверждение", f"Удалить студента «{name}»?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self._service.delete(idx)
            self._reload()

    def _on_search(self):
        students = self._service.get_all()
        if not students:
            QMessageBox.information(self, "Поиск", "Список студентов пуст.")
            return
        dlg = SearchDialog(self, students, service=self._service)
        dlg.exec_()

    def _on_delete_by_criteria(self):
        students = self._service.get_all()
        if not students:
            QMessageBox.information(self, "Удаление", "Список студентов пуст.")
            return
        dlg = DeleteByCriteriaDialog(self, students)
        if dlg.exec_() == QDialog.Accepted:
            key, value = dlg.get_filter()
            found = self._service.search(key, value)
            if not found:
                QMessageBox.information(self, "Удаление", "Записей по заданному критерию не найдено.")
                return
            if QMessageBox.question(self, "Подтверждение",
                                    f"Удалить {len(found)} записей?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self._service.delete_many(found)
                self._reload()
                QMessageBox.information(self, "Удаление", f"Удалено записей: {len(found)}.")
