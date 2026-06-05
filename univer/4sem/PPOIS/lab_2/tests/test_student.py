import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.student import Student


def make_student(**kwargs) -> Student:
    defaults = dict(name="Иванов И.И.", course=2, group="ПО-21",
                    total_works=10, done_works=7, language="Python")
    defaults.update(kwargs)
    return Student(**defaults)


class TestStudentProperty:
    def test_not_done_works_normal(self):
        s = make_student(total_works=10, done_works=7)
        assert s.not_done_works == 3

    def test_not_done_works_all_done(self):
        s = make_student(total_works=5, done_works=5)
        assert s.not_done_works == 0

    def test_not_done_works_none_done(self):
        s = make_student(total_works=8, done_works=0)
        assert s.not_done_works == 8


class TestStudentSerialization:
    def test_to_dict_contains_all_fields(self):
        s = make_student()
        d = s.to_dict()
        assert set(d.keys()) == {"name", "course", "group", "total_works", "done_works", "language"}

    def test_to_dict_values(self):
        s = make_student(name="Петров П.П.", course=3, group="ПО-31",
                         total_works=12, done_works=9, language="Java")
        d = s.to_dict()
        assert d["name"] == "Петров П.П."
        assert d["course"] == 3
        assert d["group"] == "ПО-31"
        assert d["total_works"] == 12
        assert d["done_works"] == 9
        assert d["language"] == "Java"

    def test_from_dict_roundtrip(self):
        s = make_student()
        restored = Student.from_dict(s.to_dict())
        assert restored == s

    def test_from_dict_creates_correct_student(self):
        data = {"name": "Сидоров С.С.", "course": 1, "group": "ПО-11",
                "total_works": 6, "done_works": 4, "language": "C++"}
        s = Student.from_dict(data)
        assert s.name == "Сидоров С.С."
        assert s.course == 1
        assert s.not_done_works == 2

    def test_not_done_not_in_dict(self):
        s = make_student(total_works=10, done_works=3)
        d = s.to_dict()
        assert "not_done_works" not in d
