from Test import Test
from Student import Student
from Teacher import Teacher
from TestException import TestException


def main():
    tests = []
    students = []

    test1 = Test("Programming on C++", [
        "What is C++?",
        "What is OOP?",
        "What is class?",
        "What is array?",
        "What is \"int\""
    ],
                 [
                     "Programming language",
                     "Object-oriented programming"
                     "Data Abstraction",
                     "Data structure",
                     "Data type"
                 ])
    test2 = Test("General Knowledge", [
        "What is the capital of France?",
        "What is the tallest mountain in the world?",
        "What is the capital of Belarus",
        "What is the capital of Russia",
        "what is the capital of the Ukraine"
    ],
                 [
                     "Paris",
                     "Mount Everest",
                     "Minsk",
                     "Moscow",
                     "Kiev"
                 ])

    student1 = Student("Ivanov")
    student2 = Student("Petrov")
    students.extend([student1, student2])
    teacher = Teacher()

    teacher.add_test(tests, test1)
    teacher.add_test(tests, test2)

    while True:
        print("""
                Input number of operation:
                0 - Exit
                1 - Students' info
                2 - Add test
                3 - Delete test
                4 - Complete test
                5 - Give a feedback
                6 - Add student
                7 - List tests
                8 - Analyze results
                """)

        try:
            i = int(input("Choose operation: "))
        except ValueError:
            TestException("Invalid input: please enter a number.").handle_exception()
            continue

        match i:
            case 0:
                print("Goodbye!")
                break
            case 1:
                for student in students:
                    student.get_info()
                    print("\n")
            case 2:
                test_name = str(input("Enter the name of the test: "))
                num_questions = 5
                questions = [input(f"Enter question {i + 1}: ") for i in range(num_questions)]
                correct_answers = [input(f"Enter correct answer for question {i + 1}: ") for i in range(num_questions)]

                new_test = Test(test_name, questions, correct_answers)
                tests.append(new_test)
            case 3:
                test_name = input("Enter the name of the test to delete: ")
                teacher.remove_test(tests, test_name)
            case 4:
                student_name = input("Input your name: ")
                if not student_name.isalpha():
                    TestException("Invalid input: please enter a valid name.").handle_exception()
                    continue
                for student in students:
                    if student.get_name() == student_name:
                        print("What test you'd like to complete? ")
                        for test in tests:
                            print(test.get_name())
                        test_name = str(input("\nInput test name: "))
                        for test in tests:
                            if test_name == test.get_name():
                                teacher.test_student(student, test)
            case 5:
                student_name = input("Input student's name: ")
                if not student_name.isalpha():
                    TestException("Invalid input: please enter a valid name.").handle_exception()
                    continue
                for student in students:
                    if student.get_name() == student_name:
                        student.create_feedback()
            case 6:
                student_name = input("Input NEW student's name: ")
                if not student_name.isalpha():
                    TestException("Invalid input: please enter a valid name.").handle_exception()
                    continue
                new_student = Student(student_name)
                students.append(new_student)
            case 7:
                for test in tests:
                    print(test.get_name())
            case 8:
                teacher.analyze_results(students, tests)
            case _:
                TestException("Invalid input: please choose a number between 0 and 8.").handle_exception()


if __name__ == "__main__":
    main()
