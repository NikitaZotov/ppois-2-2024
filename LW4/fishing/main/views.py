# Create your views here.
import threading

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from main.source.fishery_production_instance import FisheryProductionInstance

from main.source.fishery_production import FisheryProduction

from main.source.fisherman import Experience

from main.source.fisherman import Fisherman

from main.source.ship import Ship

from main.source.net import Net

from main.util.serialization_util import Util


def index(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()
    data = {
        'tittle': 'Главная страница!!',
    }
    return render(request, 'main/index.html', data)


def about(request):
    return render(request, 'main/about.html')


def organize_fishing(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()

    if request.method == 'POST':
        ship_index = request.POST.get('ship')
        fisherman_indices = request.POST.getlist('fishermen')
        net_indices = request.POST.getlist('nets')
        print(fisherman_indices)
        if ship_index and fisherman_indices:
            ship = fishery_production.choose_ship(ship_index)
            fishermen = fishery_production.choose_fishermen(fisherman_indices)
            fishery_production.choose_nets(ship, net_indices)

            ship.add_fishermen(fishermen)
            thread = threading.Thread(target=ship.start_fishing)
            thread.start()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'main/organize_fishing.html', {'error_message': 'Invalid selection'})

    context = {
        'ships': fishery_production.ships,
        'fishermen': fishery_production.fishermen,
        'nets': fishery_production.free_nets,
    }
    return render(request, 'main/organize_fishing.html', context)


def finish_fishing(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()

    if request.method == 'POST':
        fishery_production.end_fishing_and_store_fish()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'main/finish_fishing.html', {'error_message': 'Invalid selection'})


def process_fish(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()

    if request.method == 'POST':
        processed_fish = fishery_production.cold_storage.process_fish()
        return render(request, 'main/process_fish.html', {'processed_fish': processed_fish})

    return render(request, 'main/process_fish.html')


def freeze_fish(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()

    if request.method == 'POST':
        try:
            target_weight = int(request.POST.get('weight'))
            frozen_fish = fishery_production.cold_storage.freeze_fish(target_weight)
            return render(request, 'main/freeze_fish.html', {
                'frozen_fish': frozen_fish,
                'message': f'{sum(fish.weight for fish in frozen_fish)} кг рыбы было заморожено.'
            })
        except ValueError:
            return render(request, 'fishery_app/freeze_fish.html', {
                'error_message': 'Введите корректное число килограммов.'
            })

    return render(request, 'main/freeze_fish.html')


def transfer_to_market(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()
    total_weight = fishery_production.cold_storage.calculate_weight(is_for_selling=True)
    if request.method == 'POST':
        try:
            limit = int(request.POST.get('weight_limit'))
            fish_to_market = fishery_production.cold_storage.sell_fish_to_market(limit)
            fishery_production.market.receive_fish_from_storage(fishery_production.cold_storage, fish_to_market)
            total_weight = fishery_production.cold_storage.calculate_weight(is_for_selling=True)
            return render(request, 'main/transfer_to_market.html',
                          {'fish_to_market': fish_to_market, 'total_weight': total_weight})
        except ValueError as e:
            return render(request, 'main/transfer_to_market.html', {'error_message': 'Введите корректное число'})
    return render(request, 'main/transfer_to_market.html', {'total_weight': total_weight})


def add_ship(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()
    if request.method == 'POST':
        name = request.POST.get('name')
        ship = Ship(name)
        fishery_production.ships.append(ship)
        return HttpResponseRedirect('/')

    return render(request, 'main/add_ship.html')


def add_fisherman(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()
    if request.method == 'POST':
        name = request.POST.get('name')
        experience = request.POST.get('experience')

        experience_map = {
            "новичок": Experience.BEGINNER,
            "средний": Experience.INTERMEDIATE,
            "продвинутый": Experience.ADVANCED,
            "эксперт": Experience.EXPERT
        }

        try:
            experience_enum = experience_map[experience.lower()]
        except KeyError:
            return render(request, 'fishery_app/add_fisherman.html',
                          {'error_message': 'Выберите корректный уровень опыта'})

        fisherman = Fisherman(name, experience)
        fishery_production.fishermen.append(fisherman)
        print(fishery_production.fishermen)

        return HttpResponseRedirect('/')
    else:
        return render(request, 'main/add_fisherman.html')


def add_net(request):
    fishery_production: FisheryProduction = FisheryProductionInstance.get_instance()

    if request.method == 'POST':
        try:
            square = int(request.POST.get('square'))
            net = Net(square)
            fishery_production.free_nets.append(net)
            return HttpResponseRedirect('/')
        except ValueError:
            return render(request, 'main/add_net.html', {'error_message': 'Введите корректное число'})

    return render(request, 'main/add_net.html')


def logout(request):
    fishery_production = FisheryProductionInstance.get_instance()
    while fishery_production.borrowed_ships:
        fishery_production.end_fishing_and_store_fish()
    util = Util()
    util.save_state("fishery_production.json", fishery_production)
    return render(request, 'main/save_state.html')
