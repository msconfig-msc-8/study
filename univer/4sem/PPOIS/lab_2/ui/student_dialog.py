from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QHBoxLayout, QPushButton, QMessageBox
)
from models.student import Student


class StudentDialog(QDialog):
    def __init__(self, parent=None, student: Student = None):
        super().__init__(parent)
        self.setWindowTitle("Добавить студента" if student is None else "Редактировать студента")
        self.setMinimumWidth(400)
        self._student = student

        layout = QFormLayout(self)

        self.name_edit = QLineEdit(student.name if student else "")
        layout.addRow("ФИО студента:", self.name_edit)

        self.course_spin = QSpinBox()
        self.course_spin.setRange(1, 6)
        self.course_spin.setValue(student.course if student else 1)
        layout.addRow("Курс:", self.course_spin)

        self.group_edit = QLineEdit(student.group if student else "")
        layout.addRow("Группа:", self.group_edit)

        self.total_spin = QSpinBox()
        self.total_spin.setRange(0, 999)
        self.total_spin.setValue(student.total_works if student else 0)
        layout.addRow("Общее число работ:", self.total_spin)

        self.done_spin = QSpinBox()
        self.done_spin.setRange(0, 999)
        self.done_spin.setValue(student.done_works if student else 0)
        layout.addRow("Кол-во выполненных работ:", self.done_spin)

        self.lang_edit = QLineEdit(student.language if student else "")
        layout.addRow("Язык программирования:", self.lang_edit)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self._on_accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        self._result: Student = None

    def _on_accept(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "ФИО студента не может быть пустым.")
            return
        done = self.done_spin.value()
        total = self.total_spin.value()
        if done > total:
            QMessageBox.warning(self, "Ошибка",
                                "Кол-во выполненных работ не может превышать общее число работ.")
            return
        self._result = Student(
            name=name,
            course=self.course_spin.value(),
            group=self.group_edit.text().strip(),
            total_works=total,
            done_works=done,
            language=self.lang_edit.text().strip(),
        )
        self.accept()

    def get_student(self) -> Student:
        return self._result
