class Test:
    def __init__(self, name, questions, correct_answers):
        self.test_name = name
        self.questions = questions
        self.correct_answers = correct_answers

    def get_name(self) -> str:
        return self.test_name

    def get_questions(self) -> str:
        return self.questions

    def get_answers(self) -> str:
        return self.correct_answers

