class TestException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def handle_exception(self):
        print("An exception occurred:", self.message)