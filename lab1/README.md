# Документация программной системы

## Введение

Эта программная система представляет собой систему солнечной системы, включающая в себя различные классы представляющие объекты этой системы.

## Классы и методы

### Класс SpaceObject

Базовый класс для представления естественных объектов в системе.

#### Методы

- `__init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 atmosphere: list[float] = None)`: Инициализация объекта класса SpaceObject.
- `get_name(self)`: Возвращает имя объекта.
- `get_speed(self)`: Возвращает cкорость.
- `get_mass(self)`:Возвращает массу объекта .
- `get_x(self)`:Возвращает координату x объекта .
- `get_y(self)`:Возвращает координату y объекта .
- `get_z(self)`:Возвращает координату z объекта .
- `get_gravity(self)`:Возвращает постоянную ускоренния объекта .
- `get_radius(self)`:Возвращает радиус объекта .
- `get_atmosphere(self)`:Возвращает список элементов атмосферы объекта.
- `get_info(self)`:Возвращает словарь с аттрибутами объекта .
### Класс Spacectaft

Класс для представления космического аппарата.

#### Методы

- `__init__(self, name: str, planet: SpaceObject)`: Инициализация объекта класса Spacecraft.
- `speed_exploration(self, planet: SpaceObject)`: Возвращает скорость планеты.
- `analysis_planet(self, planet: SpaceObject)`: Возвращает атмосферу планеты.
- `analysis_space_object(self, space_object: SpaceObject)`: Выводит информацию о космическом объекте.
- `get_name(self)`: Возвращает имя космического аппарата.

### Класс Star(SpaceObject)

Класс для представления космического аппарата.

#### Методы

- `__init__(self, name: str, type_star: str, speed: float, mass: float, x: float, y: float, z: float, radius: float)`: Инициализация объекта класса Star.
- `get_type(self)`: Возвращает тип звезды.


### Класс Planet(SpaceObject)

Класс для представления планет.

#### Методы

- `__init__(self,  name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 star: Star = None)`: Инициализация объекта класса Planet.
- `generate_atmosphere(self)`: Создает атмосферу планеты.
- `launch_spacecraft(self, name: str)`: Создает объект класса Spacecraft.

### Класс Asteroid(SpaceObject)

Класс для представления астероидов.

#### Методы

- `__init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float)`: Инициализация объекта класса Asteroid.


### Класс Cometa(Asteroid)

Класс для представления комет.

#### Методы

- `__init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 star: Star = None)`: Инициализация объекта класса Cometta.
- `get_star_orbit(self)`:Возращает звезду вокруг которой находится.
### Класс Satellite(Planet)

Класс для представления спутников.

#### Методы

- `__init__(self,  name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float, planet: Planet)`: Инициализация объекта класса Satellite.
- `get_planet(self)`: Возвращает планету вокруг которой вращается.

### Класс StarSystem

Базовый класс для представления звёздной системы,то есть, самой системы.

#### Методы

- `__init__(self,  star: Star = None, planets: list[Planet] = [], satellite: list[Satellite] = [],
                 asteroid: list[Asteroid] = [], cometa: list[Cometa] = [], 
spacecraft: list[Spacecraft] = [])`: Инициализация объекта класса StarSystem.
- `add_planet(self, planet: Planet)`: Добавляет планету .
- `add_satellite(self, satellite: Satellite)`: Добавляет спутник .
- `add_asteroid(self, asteroid: Asteroid)`:Добавляет астероид  .
- `add_cometa(self, cometa: Cometa)`:Добавляет комету  .
- `add_spacecraft(self, spacecraft: Spacecraft)`:Добавляет космический аппарат .
- `search_planet(self, name: str)`:Ищет планету в системе.
- `search_space_object(self, name: str)`:Ищет объект системы .
- `search_spacecraft(self, name: str)`:Ищет спутник в системе .
- `get_star(self)`:Возвращает звезду системы.
- `get_info(self)`:Выводит информацию о системе.
- `save(self)`: Сохраняет систему в файл.