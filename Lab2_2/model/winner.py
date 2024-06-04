class Winner:

    def __init__(self, name: str, surname: str, middlename: str):
        self.name = name.capitalize()
        self.surname = surname.capitalize()
        self.middlename = middlename.capitalize()

    def dict(self):

        return {"Name": self.name, "Surname": self.surname, 
                "Middlename": self.middlename}
    
    def str(self): return f"{self.name} {self.surname} {self.middlename}"
