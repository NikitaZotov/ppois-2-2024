from Model import Model
from Student import Student

model = Model()
model.initialize("data.xml")
model.print_student()
new_student: Student = Student("AAAAAAAAAA", 223344, ["phisics", "PE", "math"], [1, 2, 3])
# model.add_student(new_student, "data.xml")
model.delete_student(new_student, "data.xml")
model.print_student()

