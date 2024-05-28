from singleton import singleton
from os import PathLike
import yaml


@singleton
class Config:
    def __init__(
            self,
            path: str | bytes | PathLike = "resource/config.yaml"
    ):
        self.path = path
        self.config = {}

        with open(self.path) as file:
            templates = yaml.safe_load(file)
            self.config.update(templates)

            # for string in file:
            #     if string == '\n':
            #         continue
            #     if string[0] == '#':
            #         continue
            #     name, value = string.split(maxsplit=1)
            #     name = name.strip()
            #     value = value.strip()
            #     if value.isdigit():
            #         value = int(value)
            #     elif value.isnumeric():
            #         value = float(value)
            #     elif value.startswith("0x"):
            #         value = value
            #     self.config[name] = value

    def __getitem__(self, item: str):
        return self.config[item]

    def __setitem__(self, key: str, value: str | int | float):
        if key not in self.config:
            raise KeyError()
        self.config[key] = value
        # TODO writing in the config file


config = Config()
