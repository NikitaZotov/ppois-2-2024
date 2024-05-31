from typing import Callable, Any


class Menu:
    @classmethod
    def print_menu(cls, context: str, actions: dict[str | tuple[int, str], Callable]) -> None:
        print(context)
        for i, point in enumerate(actions):
            match point:
                case str():
                    print(f'{i+1} - {point}')
                case int() as n, _ as p:
                    print(f'{n} - {p}')
        actions[cls.__get_menu_input(*actions.keys())]()

    @classmethod
    def __get_menu_input(cls, *points):
        dict_ = {}
        for i, point in enumerate(points):
            match point:
                case str():
                    dict_[str(i + 1)] = point
                case int() as n, _:
                    dict_[str(n)] = point

        def callback(p):
            input_ = cls.__validate_input(p, dict_)
            return dict_[input_]

        return cls.get_entry(callback)

    @staticmethod
    def __validate_input(input_, points):
        if input_ not in points:
            raise ValueError(f'{input_} is not a valid choice')
        return input_

    @staticmethod
    def get_entry(callback: Callable[[Any], Any], context: str = "") -> Any:
        while True:
            try:
                input_ = input(context).replace(" ", "")
                return callback(input_)
            except ValueError as e:
                print(e)
                continue

    @staticmethod
    def show_list(list_: list[Any], context: str = "") -> None:
        print(context)
        for entry in list_:
            print(entry)

    @staticmethod
    def show_error(error_msg: str) -> None:
        print(f"Error! {error_msg}")
