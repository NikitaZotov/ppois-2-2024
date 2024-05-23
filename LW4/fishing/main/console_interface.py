from main.source.fishery_production_instance import FisheryProductionInstance
from main.util.serialization_util import Util

fishery_production_instance = None


def console_interface():
    global fishery_production_instance  # Объявляем переменную как глобальную

    # Если переменная уже проинициализирована, не выполняем код инициализации
    if fishery_production_instance is None:
        util = Util()
        fishery_production_instance = FisheryProductionInstance.get_instance()

    while True:
        fishery_production_instance.fishery_operations()
        util.save_state("fishery_production.json", fishery_production_instance)
        choice = input("Хотите продолжить? (да/нет): ")
        if choice.lower() != "да":
            break


# if __name__ == "__main__":
#     console_interface()
