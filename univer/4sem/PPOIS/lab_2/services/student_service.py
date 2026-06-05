import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xml.sax
import xml.sax.handler
from typing import List
from models.student import Student


class _StudentSAXHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.students: List[Student] = []
        self._current: dict = {}
        self._tag: str = ""
        self._text: str = ""

    def startElement(self, name, attrs):
        self._tag = name
        self._text = ""
        if name == "student":
            self._current = {}

    def characters(self, content):
        self._text += content

    def endElement(self, name):
        if name == "student":
            self.students.append(Student(
                name=self._current.get("name", ""),
                course=int(self._current.get("course", 1)),
                group=self._current.get("group", ""),
                total_works=int(self._current.get("total_works", 0)),
                done_works=int(self._current.get("done_works", 0)),
                language=self._current.get("language", ""),
            ))
        elif name in ("name", "course", "group", "total_works", "done_works", "language"):
            self._current[name] = self._text.strip()


class StudentService:
    def __init__(self):
        self._students: List[Student] = []
        self._filepath: str = ""

    # ── persistence ──────────────────────────────────────────────────────────

    def load(self, filepath: str):
        handler = _StudentSAXHandler()
        xml.sax.parse(filepath, handler)
        self._students = handler.students
        self._filepath = filepath

    def save(self, filepath: str = ""):
        path = filepath or self._filepath
        if not path:
            raise ValueError("Путь к файлу не задан.")
        dom = minidom.getDOMImplementation().createDocument(None, "students", None)
        root = dom.documentElement
        for s in self._students:
            node = dom.createElement("student")
            for tag, val in [
                ("name", s.name), ("course", str(s.course)),
                ("group", s.group), ("total_works", str(s.total_works)),
                ("done_works", str(s.done_works)), ("language", s.language),
            ]:
                el = dom.createElement(tag)
                el.appendChild(dom.createTextNode(val))
                node.appendChild(el)
            root.appendChild(node)
        xml_str = dom.toprettyxml(indent="  ", encoding="utf-8")
        with open(path, "wb") as f:
            f.write(xml_str)
        if filepath:
            self._filepath = filepath

    @property
    def filepath(self) -> str:
        return self._filepath

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def get_all(self) -> List[Student]:
        return list(self._students)

    def add(self, student: Student):
        self._students.append(student)

    def update(self, index: int, student: Student):
        self._students[index] = student

    def delete(self, index: int):
        del self._students[index]

    def delete_many(self, students: List[Student]):
        ids = set(id(s) for s in students)
        self._students = [s for s in self._students if id(s) not in ids]

    # ── search ────────────────────────────────────────────────────────────────

    def search(self, key: str, value) -> List[Student]:
        result = []
        for s in self._students:
            if key == "name":
                if str(value).lower() in s.name.lower():
                    result.append(s)
            elif key == "group":
                if str(value).lower() in s.group.lower():
                    result.append(s)
            elif key == "not_done":
                if s.not_done_works == value:
                    result.append(s)
            else:
                if getattr(s, key, None) == value:
                    result.append(s)
        return result

    def unique_values(self, key: str) -> List:
        if key == "not_done":
            return sorted(set(s.not_done_works for s in self._students))
        return sorted(set(getattr(s, key) for s in self._students))
