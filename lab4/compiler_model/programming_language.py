class ProgrammingLanguage:
    def __init__(self, name: str = "",file_extension: str = "",reserved_words: dict = None):
        self.name = name
        self.file_extension = file_extension
        self.__reserved_words = reserved_words or {}

    def __str__(self):
        return f"Language: {self.name}\nFile extension: .{self.file_extension}"

    def add_new_key_words(self, key_word_list: dict):
        self.__reserved_words.update(key_word_list)

    def add_new_key_word(self, key_word: str, definition: str):
        self.__reserved_words[key_word] = definition

    def clear_reserved_words(self):
        self.__reserved_words.clear()
    def get_key_word_list(self) -> dict:
        return self.__reserved_words

    def print_key_word(self):
        print(f"Ключевые слова: {self.__reserved_words}")