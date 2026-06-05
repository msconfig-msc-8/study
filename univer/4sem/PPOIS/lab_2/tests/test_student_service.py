import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.student import Student
from services.student_service import StudentService


def make_student(name="Иванов И.И.", course=2, group="ПО-21",
                 total_works=10, done_works=7, language="Python") -> Student:
    return Student(name=name, course=course, group=group,
                   total_works=total_works, done_works=done_works, language=language)


@pytest.fixture
def service():
    return StudentService()


@pytest.fixture
def populated_service():
    svc = StudentService()
    svc.add(make_student("Иванов И.И.", 2, "ПО-21", 10, 7, "Python"))
    svc.add(make_student("Петров П.П.", 3, "ПО-31", 12, 9, "Java"))
    svc.add(make_student("Сидоров С.С.", 2, "ПО-21", 8, 4, "Python"))
    svc.add(make_student("Козлов К.К.", 4, "ПО-41", 15, 15, "C++"))
    return svc


class TestCRUD:
    def test_initially_empty(self, service):
        assert service.get_all() == []

    def test_add_student(self, service):
        s = make_student()
        service.add(s)
        assert len(service.get_all()) == 1
        assert service.get_all()[0] == s

    def test_add_multiple(self, service):
        service.add(make_student("А"))
        service.add(make_student("Б"))
        assert len(service.get_all()) == 2

    def test_get_all_returns_copy(self, service):
        service.add(make_student())
        lst = service.get_all()
        lst.clear()
        assert len(service.get_all()) == 1

    def test_update_student(self, service):
        service.add(make_student(name="Старый"))
        service.update(0, make_student(name="Новый"))
        assert service.get_all()[0].name == "Новый"

    def test_delete_student(self, service):
        service.add(make_student("А"))
        service.add(make_student("Б"))
        service.delete(0)
        assert len(service.get_all()) == 1
        assert service.get_all()[0].name == "Б"

    def test_delete_last(self, service):
        service.add(make_student())
        service.delete(0)
        assert service.get_all() == []

    def test_delete_many(self, populated_service):
        all_s = populated_service.get_all()
        to_delete = [all_s[0], all_s[2]]
        populated_service.delete_many(to_delete)
        remaining = populated_service.get_all()
        assert len(remaining) == 2
        assert all(s.name in ("Петров П.П.", "Козлов К.К.") for s in remaining)

    def test_delete_many_empty_list(self, populated_service):
        count_before = len(populated_service.get_all())
        populated_service.delete_many([])
        assert len(populated_service.get_all()) == count_before


class TestXMLPersistence:
    def test_save_and_load_roundtrip(self, tmp_path):
        path = str(tmp_path / "students.xml")
        svc1 = StudentService()
        svc1.add(make_student("Иванов"))
        svc1.add(make_student("Петров", course=3))
        svc1.save(path)

        svc2 = StudentService()
        svc2.load(path)
        assert len(svc2.get_all()) == 2
        assert svc2.get_all()[0].name == "Иванов"
        assert svc2.get_all()[1].course == 3

    def test_save_remembers_filepath(self, tmp_path):
        path = str(tmp_path / "students.xml")
        svc = StudentService()
        svc.add(make_student())
        svc.save(path)
        assert svc.filepath == path

    def test_save_without_path_raises(self, service):
        service.add(make_student())
        with pytest.raises(ValueError):
            service.save()

    def test_xml_preserves_all_fields(self, tmp_path):
        path = str(tmp_path / "students.xml")
        original = make_student("Сидоров С.С.", 3, "ПО-31", 12, 8, "C++")
        svc = StudentService()
        svc.add(original)
        svc.save(path)

        svc2 = StudentService()
        svc2.load(path)
        restored = svc2.get_all()[0]
        assert restored == original

    def test_save_empty_list(self, tmp_path):
        path = str(tmp_path / "empty.xml")
        svc = StudentService()
        svc.save(path)
        svc2 = StudentService()
        svc2.load(path)
        assert svc2.get_all() == []

    def test_not_done_not_stored_directly(self, tmp_path):
        path = str(tmp_path / "students.xml")
        svc = StudentService()
        svc.add(make_student(total_works=10, done_works=3))
        svc.save(path)
        content = open(path, encoding="utf-8").read()
        assert "not_done" not in content

    def test_xml_valid_encoding(self, tmp_path):
        path = str(tmp_path / "students.xml")
        svc = StudentService()
        svc.add(make_student("Фёдоров Ф.Ф.", language="C#"))
        svc.save(path)
        content = open(path, "rb").read()
        assert b"utf-8" in content or b"UTF-8" in content


class TestSearch:
    def test_search_by_name_exact(self, populated_service):
        result = populated_service.search("name", "Иванов И.И.")
        assert len(result) == 1
        assert result[0].name == "Иванов И.И."

    def test_search_by_name_partial(self, populated_service):
        result = populated_service.search("name", "ов")
        names = [s.name for s in result]
        assert "Иванов И.И." in names
        assert "Петров П.П." in names
        assert "Сидоров С.С." in names

    def test_search_by_name_case_insensitive(self, populated_service):
        result = populated_service.search("name", "иванов")
        assert len(result) == 1

    def test_search_by_name_no_match(self, populated_service):
        assert populated_service.search("name", "Несуществующий") == []

    def test_search_by_group(self, populated_service):
        result = populated_service.search("group", "ПО-21")
        assert len(result) == 2
        assert all(s.group == "ПО-21" for s in result)

    def test_search_by_group_partial(self, populated_service):
        assert len(populated_service.search("group", "ПО-")) == 4

    def test_search_by_course(self, populated_service):
        result = populated_service.search("course", 2)
        assert len(result) == 2
        assert all(s.course == 2 for s in result)

    def test_search_by_course_no_match(self, populated_service):
        assert populated_service.search("course", 99) == []

    def test_search_by_language(self, populated_service):
        result = populated_service.search("language", "Python")
        assert len(result) == 2

    def test_search_by_done_works(self, populated_service):
        result = populated_service.search("done_works", 7)
        assert len(result) == 1
        assert result[0].name == "Иванов И.И."

    def test_search_by_total_works(self, populated_service):
        assert len(populated_service.search("total_works", 10)) == 1

    def test_search_by_not_done(self, populated_service):
        result = populated_service.search("not_done", 3)
        assert len(result) == 2

    def test_search_by_not_done_zero(self, populated_service):
        result = populated_service.search("not_done", 0)
        assert len(result) == 1
        assert result[0].name == "Козлов К.К."


class TestUniqueValues:
    def test_unique_courses(self, populated_service):
        assert populated_service.unique_values("course") == [2, 3, 4]

    def test_unique_languages(self, populated_service):
        assert populated_service.unique_values("language") == ["C++", "Java", "Python"]

    def test_unique_not_done(self, populated_service):
        vals = populated_service.unique_values("not_done")
        assert 0 in vals
        assert 3 in vals

    def test_unique_empty_service(self, service):
        assert service.unique_values("course") == []
