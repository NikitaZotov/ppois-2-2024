from classes import Zoo, Animal, Enclosure, Veterinarian

Veterinarian.VETS = [
    Veterinarian("Айболит", "Свободен"),
    Veterinarian("Герман", "Свободен"),
    Veterinarian("Саша", "Свободен"),
]


animals = {
    1: Animal("Лев", Enclosure(1), True, True),
    2: Animal("Слон", Enclosure(2), False, False),
    3: Animal("Жираф", Enclosure(3), True, False),
}

zoo = Zoo(animals)

while True:
    action = input("Выберите действие (1 - посетить животное, 2 - запись на экскурсию, 3 - выйти из зоопарка): ")
    if action not in ("1", "2", "3"):
        continue

    if action == "1":
        zoo._show_animals_list()
        animal_id = int(input("Введите номер животного: "))
        zoo.visit_animal(animal_id)
    elif action == "2":
        zoo.book_tour()
    else:
        zoo.exit_zoo()
        break
