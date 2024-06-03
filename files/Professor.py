from files.Person import Person


class Professor(Person):
    def __init__(self, first_name: str, last_name: str, age: int) -> None:
        super().__init__(first_name, last_name, age)
