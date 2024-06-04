from typing import Dict, List

class Enclosure:
    def __init__(self, number: int):
        self.number = number

class Veterinarian:
    VETS: List["Veterinarian"] = []

    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status
        Veterinarian.VETS.append(self)


class Animal:
    def __init__(self, name: str, enclosure: "Enclosure", is_healthy: bool, is_hungry: bool):
        self.name = name
        self.enclosure = enclosure
        self.is_healthy = is_healthy
        self.is_hungry = is_hungry

    def feed(self) -> None:
        self.is_hungry = False

class Zoo:
    def __init__(self, animals: Dict[int, "Animal"]):
        self.animals = animals

    def visit_animal(self, animal_id: int) -> None:
        animal = self.animals[animal_id]
        print(f"Вы посещаете {animal.name} в вольере {animal.enclosure.number}.")
        print(f"{'Здоров' if animal.is_healthy else 'Болен'}. {'Голоден' if animal.is_hungry else 'Сыт'}.")
        self._show_animal_actions(animal)

    def _show_animals_list(self) -> None:
        for i, animal in self.animals.items():
            print(f"{i}. {animal.name}")

    def _show_animal_actions(self, animal: "Animal") -> None:
        while True:
            action = input("Выберите действие (1 - покормить, 2 - погладить, 3 - вызвать ветеринара, 4 - уйти): ")
            if action not in ("1", "2", "3", "4"):
                continue

            if action == "1":
                if animal.is_hungry:
                    animal.feed()
                    print(f"{animal.name} полакомился.")
                else:
                    print(f"{animal.name} сыт.")
            elif action == "2":
                print(f"{animal.name} приласкался к вам.")
            elif action == "3":
                if animal.is_healthy:
                    print(f"{animal.name} здоров.")
                else:
                    self.show_vet_list(animal)
            else:
                break

    def show_vet_list(self, animal: "Animal") -> None:
        available_vets = [vet for vet in Veterinarian.VETS if vet.status == "Свободен"]

        if not available_vets:
            print("Нет доступных ветеринаров.")
            return

        print("Выберите ветеринара:")
        for i, vet in enumerate(available_vets, start=1):
            print(f"{i}. {vet.name} ({vet.status})")

        vet_id = int(input()) - 1
        vet = available_vets[vet_id]
        vet.status = "Занят"
        animal.is_healthy = True
        print(f"Ветеринар {vet.name} вызван и вылечил {animal.name}.")

    def book_tour(self) -> None:
        print("Вы записались на ближайшую экскурсию.")

    def exit_zoo(self) -> None:
        print("Вы вышли из зоопарка.")





