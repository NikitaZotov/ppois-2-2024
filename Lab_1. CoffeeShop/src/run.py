import os
from typing import List

import colors
import equipment
# import simulation
from coffee_shop import CoffeeShop
from menu import Menu
from people import Visitor
from shop import Shop


def hello():
    coffee_shop_name = input("Type coffee shop name ")
    coffee_shop: CoffeeShop = CoffeeShop(coffee_shop_name)
    choice: str = input("Do you want to use standard menu? (y/n) ")
    if choice.lower() == "y" or choice.lower() == "yes":
        menu: Menu = Menu()
        menu.default_menu()
        coffee_shop.menu = menu
        coffee_shop.menu.default_menu()
    show_menu(coffee_shop)


def show_menu(coffee_shop: CoffeeShop):
    while True:
        print("_" * 20)
        print("i - coffee shop info\n"
              "w - wait for visitors\n"
              "m - manage coffee shop\n"
              "1 - take order\n"
              "2 - make order\n"
              "3 - show order list\n"
              "q - quit"
              )
        choice: str = input("Enter your choice: ")
        if choice == "i" or choice == "info":
            show_info(coffee_shop)
        elif choice == "w" or choice == "wait":
            simulate_visitor(coffee_shop)
        elif choice == "m" or choice == "manage":
            management(coffee_shop)
        elif choice == "1":
            coffee_shop.take_order()
        elif choice == "2":
            coffee_shop.make_order()
        elif choice == "3":
            print(coffee_shop.order_list)
        elif choice == "q" or choice == "quit":
            break
        else:
            print("Invalid choice")


def show_info(coffee_shop: CoffeeShop):
    print("_" * 20)
    print(colors.CBEIGE + colors.CITALIC + "~~~ " + coffee_shop.name + " ~~~" + colors.CEND)
    print(" account: \t\t\t\t", colors.CBOLD, coffee_shop.account)
    print(" atmosphere:\t\t\t", colors.CBOLD, coffee_shop.atmosphere,
          colors.CGREEN + " ♫ on" if coffee_shop.music else colors.CRED + " ♫ off", colors.CEND)
    visitors_waiting: int = 0
    for visitor in coffee_shop.visitor_list:
        if visitor.waiting:
            visitors_waiting += 1
    print(" visitors waiting:", colors.CBOLD, visitors_waiting, colors.CEND)
    tables_taken: int = 0
    for table in coffee_shop.tables:
        if table.is_taken:
            tables_taken += 1
    print(" tables taken:", colors.CBOLD, tables_taken, colors.CEND)
    print(" active orders:", colors.CBOLD, len(coffee_shop.order_list), colors.CEND)
    # for item in coffee_shop.order_list: # prints active orders
    #     print(item)


def simulate_visitor(coffee_shop: CoffeeShop):
    visitor: Visitor = Visitor()
    coffee_shop.visitor_enter(visitor)


def management(coffee_shop: CoffeeShop):
    while True:
        print("_" * 20)
        print(coffee_shop.name, "balance:", colors.CBOLD, coffee_shop.account, colors.CEND)
        print(coffee_shop.show_history())
        print("+ - add money\n"
              "- - remove money\n"
              "s - shop\n"
              "switch music\n"
              "b - back")
        choice: str = input("Enter your choice: ")
        if choice == "+" or choice == "add":
            coffee_shop.income(float(input("Enter amount: ")))
        elif choice == "-" or choice == "remove":
            coffee_shop.expense(float(input("Enter amount: ")))
        elif choice == "s" or choice == "shop":
            shop(coffee_shop)
        elif choice == "switch music" or choice == "music":
            coffee_shop.switch_music()
        elif choice == "b" or choice == "back":
            break
        else:
            print("Invalid choice")


def shop(coffee_shop: CoffeeShop):
    shop: Shop = Shop()
    while True:
        print("_" * 20)
        print(colors.CBOLD, colors.CSELECTED, "You have: ", colors.CEND)
        if len(coffee_shop.inventory.coffee_equipment) == 0:
            print("\tNo coffee equipment")
        for item in coffee_shop.inventory.coffee_equipment:
            print(type(item).__name__)
        print(colors.CBOLD, colors.CSELECTED, " Atmosphere equipment:", colors.CEND)
        if len(coffee_shop.inventory.atmosphere_equipment) == 0:
            print("\tNo atmosphere equipment")
        for item in coffee_shop.inventory.atmosphere_equipment:
            print(type(item).__name__)
        print(colors.CBOLD, colors.CSELECTED, " In storage:", colors.CEND)
        for key, value in coffee_shop.inventory.storage.items():
            print(f"\t{key}: {value}")

        print(colors.CSELECTED, "Shop:", colors.CEND)
        print("Available coffee equipment:")
        if shop.coffeeMachine not in coffee_shop.inventory.coffee_equipment:
            print("\tCoffee machine - ", shop.coffeeMachine.price)
        if shop.coffeeGrinder not in coffee_shop.inventory.coffee_equipment:
            print("\tCoffee grinder - ", shop.coffeeGrinder.price)
        print("Available storage items:")
        print("\t", shop.milk.name, shop.milk.amount, "l -", shop.milk.price)
        print("\t", shop.coffeeBeans.name, shop.coffeeBeans.amount, "kg -", shop.coffeeBeans.price)

        choice: str = input("Enter what you want to buy (b - back): ")
        if choice.lower() == "coffee machine" or choice == "cm" or choice == "machine":
            if shop.coffeeMachine in coffee_shop.inventory.coffee_equipment:
                print("Wrong option")
            else:
                coffee_shop.buy_coffee_equipment(shop.coffeeMachine)
        elif choice.lower() == "coffee grinder" or choice == "cg" or choice == "grinder":
            if shop.coffeeGrinder in coffee_shop.inventory.coffee_equipment:
                print("Wrong option")
            else:
                coffee_shop.buy_coffee_equipment(shop.coffeeGrinder)
        elif choice.lower() == "milk" or choice == "m":
            coffee_shop.buy_storage_item(shop.milk)
        elif choice.lower() == "coffee beans" or choice == "cb" or choice == "beans":
            coffee_shop.buy_storage_item(shop.coffeeBeans)
        elif choice == "b" or choice == "back":
            break
        else:
            print("Wrong option")


hello()
