from typing import List, Dict
from files.Professor import Professor


class Curriculum:
    def __init__(
        self,
        name: str,
        subjects: List[str],
        professors: Dict[str, Professor],
        lectures_per_subject: int = 10,
    ) -> None:
        self.name: str = name
        self.subjects: List[str] = subjects
        self.professors: Dict[str, Professor] = professors
        self.lectures_per_subject: int = lectures_per_subject
        self.attendance_records: Dict[str, Dict[str, int]] = {}

    def display_curriculum_info(self) -> None:
        print(f"Название учебного плана: {self.name}")
        print("Список предметов и преподавателей:")
        for subject, professor in self.professors.items():
            print(f"- {subject}: {professor.first_name} {professor.last_name}")
        print(f"Количество лекций по каждому предмету: {self.lectures_per_subject}")
