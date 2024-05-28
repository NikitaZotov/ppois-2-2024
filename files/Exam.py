import random


class Exam:
    def __init__(self, subject: str, professor: str, classroom: str) -> None:
        self.subject = subject
        self.professor = professor
        self.classroom = classroom
        self.grade = None
        self.passed = False

    def take_exam(self, attendance: int, total_lectures: int) -> None:
        attendance_rate = attendance / total_lectures
        base_grade = attendance_rate * 10
        deviation = random.uniform(-1, 2)
        self.grade = max(0, min(10, int(base_grade + deviation)))
        if self.grade >= 4:
            self.passed = True
        else:
            self.passed = False

    def display_exam_info(self) -> None:
        print(f"Экзамен по предмету: {self.subject}")
        print(f"Преподаватель: {self.professor}")
        print(f"Аудитория: {self.classroom}")
        if self.grade is not None:
            if self.grade >= 4:
                print(f"Оценка: {self.grade:.2f}")
                print("Экзамен сдан.")
            else:
                print("Экзамен не сдан.")

