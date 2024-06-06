# This is a sample Python script.
import garden as gr
import garden_administration as ga

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#Модель огорода 39

#Предметная область: организация и управление садово-огородным участком.

#Важные сущности: огород, почва, растения, семена, инструменты, удобрения, полив.

#Операции: операция посева и посадки, операция ухода за растениями, операция полива и удобрения,
# операция сбора урожая, операция планирования и дизайна огорода.







# Press the green button in the gutter to run the script.
garden_adm = ga.GardenAdministration()
while True:
    print('1.Добавить грядку\n2.Вывести список грядок \n3.Купить семена \n4.Посадить грядку\n'
          '5.Полить грядку\n6.Удобрить грядку \n7.Позаботиться о грядке \n8.Cобрать урожай \n'
          '9.Добавить растение в инцеклопедию \n10.Пополнить список предпочитаемых почв для растения \n'
          '11.Вывести информацию о растении \n12.Вывести информации о количестве семян \n'
          '13.Закончить')
    a = input()
    match(a):
        case '1':
            print('Введите длину грядки')
            l = input()
            print('Введите ширину грядки')
            w = input()
            print('Введите тип почвы')
            soil = input()
            match(garden_adm.add_garden_bed(l,w, soil)):
                case -1: print('Длина или ширина не целое число')
                case 0: print('DONE')
        case '2':
            for bed in garden_adm.garden_plan:
                print(bed.garden_bed_width, ' ', bed.garden_bed_length, ' ', bed.soil_type, ' ', bed.get_plant())
        case '3':
            print('Введите название растения')
            name = input()
            print('Введите количество семян')
            num = input()
            match(garden_adm.buy_seeds(name,num)):
                case -1: print('Количество семян не целое число')
                case 0: print('DONE')
        case '4':
            print('Введите название растения, которое желаете посадить')
            name = input()
            print('Введите номер грядки')
            id_ = input()
            match(garden_adm.plant_garden(id_, name)):
                case 1: print('DONE. Информации о растении нет  в инцекопедии')
                case -1: print('Грядки с таким id не существует')
                case 0: print('DONE')
                case -3: print('Недостаточно семян')
                case 2: print('Данная почва не подходит')
        case '5':
            print('Введите id грядки')
            id_ = input()
            match(garden_adm.water_plants(id_)):
                case 0: print('DONE')
                case -1: print('Невозможно полить данную грядку')
        case '6':
            print('Введите id грядки')
            id_ = input()
            match (garden_adm.fertilizing_lant(id_)):
               case 0:print('DONE')
               case -1:print('Невозможно удобрить данную грядку')
        case '7':
            print('Введите id грядки')
            id_ = input()
            match (garden_adm.take_care_of_plant(id_)):
               case 0:print('DONE')
               case -1:print('Невозможно поухаживать за данной грядку')
        case '8':
            print('Введите id грядки')
            id_ = input()
            a,b = garden_adm.collect_garden_bed(id_)
            match a:
                case -1: print('Такой грядки не существует')
                case 0: print('Данная грядка не существует')
                case _: print('Имя растения:', b, ' урожай:', a)
        case '9':
            print('Введите название растения')
            name = input()
            print('Введите предпочитаемый тип почвы')
            soil = input()
            print('Введите время между поливками в днях')
            w = input()
            print('Введите время созревания урожая в неделях')
            c = input()
            print('Введите время между уходами за растениями в днях')
            care = input()
            print('Введите время между вносами удобрений в днях')
            f = input()
            match(garden_adm.ad_plant_to_enciclopedy(name, soil, w,c,care,f)):
                case -1: print('Данное растение уже существует')
                case 0: print('DONE')
        case '10':
            print('Введите название растения')
            name = input()
            print('Введити тип почвы')
            soil = input()
            match(garden_adm.ad_soil_type_to_enciclopedy(name, soil)):
                case -1: print('Нет такого растения в энциклопедии')
                case 0: print('DONE')
        case '11':
            print('Введите название растения')
            name = input()
            if(garden_adm.plant_enciclopedy.get(name) == None):
                print('Данного растения нет в энциклопедии')
            else:
                plant_info = garden_adm.plant_enciclopedy.get(name)
                for soil in plant_info.prefered_solid:
                    print(soil, end=' ')
                print('\nВремя между поливками:', plant_info.time_between_watering, '\nВремя между уходами за растением:',
                      plant_info.time_between_taking_care, '\nВремя между удобрениями:', plant_info.time_between_fertilizing,
                      '\nВремя созревания урожая:', plant_info.time_before_colecting)
        case '12':
            print('Введите название растения')
            name = input()
            a = garden_adm.seads_collection.get(name, 0)
            print(a)
        case '13': break
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
