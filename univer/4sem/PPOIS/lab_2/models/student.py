from dataclasses import dataclass, asdict


@dataclass
class Student:
    name: str
    course: int
    group: str
    total_works: int
    done_works: int
    language: str

    @property
    def not_done_works(self) -> int:
        return self.total_works - self.done_works

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            name=data["name"],
            course=data["course"],
            group=data["group"],
            total_works=data["total_works"],
            done_works=data["done_works"],
            language=data["language"],
        )
