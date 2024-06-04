import pytest
from unittest.mock import patch
from io import StringIO
from classes import Zoo, Animal, Enclosure, Veterinarian

@pytest.fixture
def setup_zoo():
    animals = {
        1: Animal("Лев", Enclosure(1), True, True),
        2: Animal("Слон", Enclosure(2), False, False),
        3: Animal("Жираф", Enclosure(3), True, False),
    }
    zoo = Zoo(animals)
    return zoo

def test_animal_feeding():
    enclosure = Enclosure(1)
    animal = Animal("Лев", enclosure, True, True)
    animal.feed()
    assert not animal.is_hungry

def test_veterinarian_initialization():
    vet = Veterinarian("Айболит", "Свободен")
    assert vet.name == "Айболит"
    assert vet.status == "Свободен"

def test_show_animals_list(setup_zoo, capsys):
    setup_zoo._show_animals_list()
    captured = capsys.readouterr()
    assert "1. Лев" in captured.out
    assert "2. Слон" in captured.out
    assert "3. Жираф" in captured.out

def test_visit_animal(setup_zoo, capsys):
    with patch('builtins.input', side_effect=['1', '4']):
        setup_zoo.visit_animal(1)
        captured = capsys.readouterr()
        assert "Вы посещаете Лев в вольере 1." in captured.out
        assert "Здоров. Голоден." in captured.out

def test_show_animal_actions_feed(setup_zoo, capsys):
    with patch('builtins.input', side_effect=['1', '4']):
        setup_zoo._show_animal_actions(setup_zoo.animals[1])
        captured = capsys.readouterr()
        assert "Лев полакомился." in captured.out

def test_show_animal_actions_pet(setup_zoo, capsys):
    with patch('builtins.input', side_effect=['2', '4']):
        setup_zoo._show_animal_actions(setup_zoo.animals[1])
        captured = capsys.readouterr()
        assert "Лев приласкался к вам." in captured.out

def test_book_tour(setup_zoo, capsys):
    setup_zoo.book_tour()
    captured = capsys.readouterr()
    assert "Вы записались на ближайшую экскурсию." in captured.out

def test_exit_zoo(setup_zoo, capsys):
    setup_zoo.exit_zoo()
    captured = capsys.readouterr()
    assert "Вы вышли из зоопарка." in captured.out

def test_zoo_main_loop(setup_zoo):
    with patch('builtins.input', side_effect=['1', '1', '4', '3']):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            setup_zoo.visit_animal(1)
            setup_zoo.exit_zoo()
            assert "Вы посещаете Лев в вольере 1." in fake_out.getvalue()
            assert "Вы вышли из зоопарка." in fake_out.getvalue()

@pytest.fixture
def setup_vets():
    Veterinarian.VETS = [
        Veterinarian("Айболит", "Свободен"),
        Veterinarian("Герман", "Свободен"),
        Veterinarian("Саша", "Свободен"),
    ]
    return Veterinarian.VETS

def test_show_vet_list(setup_zoo, setup_vets, capsys):
    with patch('builtins.input', side_effect=['1']):
        setup_zoo.show_vet_list(setup_zoo.animals[2])
        captured = capsys.readouterr()
        assert "Выберите ветеринара:" in captured.out
        assert "Айболит (Свободен)" in captured.out
        assert setup_vets[0].status == "Занят"
        assert setup_zoo.animals[2].is_healthy

def test_zoo_main_loop(setup_zoo):
    with patch('builtins.input', side_effect=['1', '1', '4', '3']):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            setup_zoo.visit_animal(1)
            setup_zoo.exit_zoo()
            assert "Вы посещаете Лев в вольере 1." in fake_out.getvalue()
            assert "Вы вышли из зоопарка." in fake_out.getvalue()
