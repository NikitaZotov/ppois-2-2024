from Marks import Marks
from Feedback import Feedback


class Student:
    def __init__(self, name):
        self.name = name
        self.marks = {}
        self.feedbacks = []

    def take_test(self, test) -> int:
        print(f"Test: {test.get_name()}")
        score = 10
        questions = test.get_questions()
        correct_answers = test.get_answers()
        for i, question in enumerate(questions):
            print(f"Question {i + 1}: {question}")
            answer = input("Answer: ")
            if answer == correct_answers[i]:
                print("Correct!")
            else:
                print(f"Mistake, correct answer: {correct_answers[i]}")
                score -= 2
        print(f"Test completed. you've achieved {score} out of 10.\n")
        return score

    def get_name(self) -> str:
        return self.name

    def add_feedback(self, feedback) -> None:
        self.feedbacks.append(feedback)

    def create_feedback(self) -> None:
        message = input("Enter feedback message: ")
        feedback = Feedback(message)
        self.add_feedback(feedback)

    def get_feedbacks(self) -> list:
        return self.feedbacks

    def get_info(self) -> None:
        print("Student Name:", self.name)
        print("Feedbacks:")
        for feedback in self.feedbacks:
            print("-", feedback.get_message())
        print("Grades:")
        for test_name, marks in self.marks.items():
            print("- Test:", test_name, ", Grades:", marks.get_grades())
        print()

    def get_marks(self, test_name):
        if test_name in self.marks:
            return self.marks[test_name]
        else:
            return None

    def add_grade(self, test_name, grade) -> None:
        if test_name not in self.marks:
            self.marks[test_name] = Marks()
        self.marks[test_name].add_grade(grade)

