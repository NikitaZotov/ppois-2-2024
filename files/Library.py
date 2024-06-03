class Library:
    def __init__(self):
        self.books = {}
        self.borrowers = {}

    def add_book(self, book_title, quantity):
        self.books[book_title] = self.books.get(book_title, 0) + quantity

    def display_available_books(self):
        available_books = []
        print("Доступные книги:")
        for book_title, quantity in self.books.items():
            print(f"{book_title}: {quantity} экземпляр(ов)")
            available_books.append(book_title)
        return available_books

    def lend_book(self, book_title, borrower_name, borrower_last_name):
        if book_title in self.books:
            if self.books[book_title] > 0:
                self.books[book_title] -= 1
                borrower_key = (borrower_name, borrower_last_name)
                self.borrowers.setdefault(borrower_key, []).append(book_title)
                print(
                    f"Книга '{book_title}' успешно выдана студенту {borrower_name} {borrower_last_name}."
                )
                return True
            else:
                print(f"Книга '{book_title}' недоступна для выдачи.")
                return False
        else:
            print("Выбранной книги нет в библиотеке.")
            return False

    def return_book(self, book_title, borrower_name, borrower_last_name):
        borrower_key = (borrower_name, borrower_last_name)
        if (
            borrower_key in self.borrowers
            and book_title in self.borrowers[borrower_key]
        ):
            self.books[book_title] += 1
            self.borrowers[borrower_key].remove(book_title)
            print(f"Книга '{book_title}' успешно возвращена.")
        else:
            print(
                f"Студент {borrower_name} {borrower_last_name} не взял книгу '{book_title}'."
            )
