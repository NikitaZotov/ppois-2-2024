#index-файл для главной страницы(телевизор выключен)
#index2-файл для включённого телевизора
#index3-файл для развлекательного канала
#index4-файл для спортивного канала
#index5-файл для кулинарного канала
#index6-файл для детского канала
#index7-отображение текущего состояния модели
#index8-отображение текущего состояния пульта управления
#index9-отображение технических характеристик
#index10-отображение графических настроек(яркость, контрастность, насыщенность)
#index11-обновление графических настроек(ярксоть, контрастность, насыщенность)
#index12-отображение уровня звука
#index13-обновление уровня звука
import os
print("\n1. Run in Web\n2. Run in CLI")
choice = input("Enter your choice:")
if choice == '1':
    os.system('python web.py')
elif choice == '2':
    os.system('python ../lab1scripts/main.py')
