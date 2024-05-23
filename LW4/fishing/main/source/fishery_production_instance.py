from main.source.cold_storage import ColdStorage
from main.source.fishery_production import FisheryProduction
from main.source.market import Market
from main.util.serialization_util import Util
from json.decoder import JSONDecodeError


class FisheryProductionInstance:
    _instance: FisheryProduction = None

    @staticmethod
    def get_instance():
        if FisheryProductionInstance._instance is None:
            util = Util()
            try:
                data1 = util.load_state("fishery_production.json")
                FisheryProductionInstance._instance = FisheryProduction.create_object(data1)
                FisheryProductionInstance._instance.open_market()
            except JSONDecodeError:
                print("Файл не найден. Создается новый объект FisheryProduction.")
                market = Market("Рынок", [])
                cold_storage = ColdStorage("Хранилище", [], [], [])
                FisheryProductionInstance._instance = FisheryProduction(cold_storage, market)
                FisheryProductionInstance._instance.open_market()
        return FisheryProductionInstance._instance
