class Student:

    def __init__(self, _name: str, _group: str, _exam_titles: list, _exam_grades: list):
        self.__name: str = _name
        self.__group: str = _group
        self.__exams: list = list(zip(_exam_titles, _exam_grades))
        self.__avg_grade: float = round(sum(_exam_grades) / len(_exam_grades), 2)

    def __str__(self):
        return f'{self.__name} - {self.__group} - {self.__exams} - {self.__avg_grade}'

    def get_name(self):
        return self.__name

    def get_group(self):
        return self.__group

    def get_exams(self):
        return self.__exams

    def get_avg_grade(self):
        return self.__avg_grade
