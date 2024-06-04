class Teacher:
    def test_student(self, student, test) -> None:
        grade = student.take_test(test)
        student.add_grade(test.get_name(), grade)

    def add_test(self, tests, new_test) -> None:
        tests.append(new_test)

    def remove_test(self, tests, test_name) -> None:
        for test in tests:
            if test.get_name() == test_name:
                tests.remove(test)
                print(f"Test '{test_name}' has been removed.")
                return
        print(f"Test '{test_name}' not found.")

    def analyze_results(self, students, tests) -> None:
        print("Results Analysis:")
        for test in tests:
            print("Test:", test.get_name())
            for student in students:
                grade = student.get_marks(test.get_name())
                if grade is not None:
                    print("- Student:", student.get_name(), ", Grade:", grade.get_grades()[0])
            print()