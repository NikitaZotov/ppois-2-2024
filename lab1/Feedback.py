class Feedback:
    def __init__(self, message):
        self.message = message

    def get_message(self) -> str:
        return self.message