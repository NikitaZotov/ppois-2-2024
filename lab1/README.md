# Лабораторная работа 1
## Вариант 21: Модель кадастрового агентства

Предметная область: учет и регистрация недвижимости.

Важные сущности: кадастровое агентство, кадастровый номер, земельный участок, здание, владелец, документы.

Операции: операция регистрации собственности, 
операция выдачи кадастровых номеров, операция обновления документации, 
операция предоставления информации о недвижимости.

## Классы
### Building
#### Свойства
- `name: str`
- `land_plot: LandPlot`
- `date_of_building: struct_time`
- `area_in_square_meters: float`
- `floors: int`
### LandPlot
#### Свойства
- `cadastral_number: CadastralNumber`
- `coordinates: float`
- `area_in_hectares: float`
- `functional_purpose: str`
### CadastralNumber
#### Свойства
- `terr_unit_region: Region`
- `terr_unit_code: str`
- `cadastral_block_number: str`
- `land_plot_number: str`
#### Методы
- `verify_land_plot_number(number: int) -> str`

  Проверяет номер земельного участка
### Region

Enum, хранит регионы DEFAULT, GRODNO, MINSK, MINSK_RG,
GOMEL, VITEBSK, MOGILEV, BREST с их номерами территориальной единицы и кол-вом блоков
### Owner
#### Свойства
- `passport_id: str`
- `first_name: str`
- `last_name: str`
### RegistrationDocument
#### Свойства
- `owner: Owner`
- `registration_date: date`
#### Методы
- ` |abstract| short_desc() -> str`

  Показывает краткое описание документа
- `update() -> None`

  Обновляет дату регистрации документа на сегодняшнюю
### CadastralAgency

Singleton
#### Свойства
- `serializer: ShelveSerializer`
- `documents: list[RegistrationDocument]`
- `registered_owners: list[Owner]`
- `registered_buildings: list[Building]`
- `registered_land_plots: list[LandPlot]`
- `unregistered_land_plots: list[LandPlot]`
#### Методы
- `register_land_plot(land_plot: LandPLot, owner: Owner)`

  Регистрирует земельный участок
- `unregister_land_plot(document: RegistrationDocument)`

  Снимает регистрацию с земельного участка
- `register_building(building: Building, owner: Owner)`

  Регистрирует здания
- `unregister_building(document: RegistrationDocument)`

  Снимает регистрацию здания
- `register_owner(owner: Owner)`

  Регистрирует владельца
- `get_land_plot_left_area(land_plot: LandPlot) -> float`

  Предоставляет информацию об оставшейся площади земельного участка
- `get_owner_documents(owner: Owner) -> list[RegistrationDocument]`

  Предоставляет все документы владельца
### Menu
#### Методы
- `print_menu(context: str, actions: dicr[str | tuple[int, str], Callable])`

  Выводит меню с введённым контекстом по словарю, где ключом является пункт меню,
  а значением -- метод-обработчик
- `get_entry(callback: Callable[[Any], Any], context: str)`

  Выводит контекст и предоставляет для него поле ввода
- `show_list(list_: list[Any], context: str)`

  Выводмт списко предоставленных сущностей и контекст
- `show_error(error_msg: str)`
  
  Показывает ошибку с указанным сообщением
### BuildingController, CadastralAgencyController, DocumentController, LandController, OwnerController

  Контроллеры, отвечающие за связь CadastralAgency с различными пунктами меню
  
