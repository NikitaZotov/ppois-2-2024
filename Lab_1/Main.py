from market import Market
from customer import Customer
from seller import Seller

def run_market():
    market = Market()

    while True:
        print("\nДобро пожаловать на рынок!")
        print("\nВыберите действие:")
        print("1. Добавить покупателя")
        print("2. Добавить продавца")
        print("3. Добавить товар продавцу")
        print("4. Покупатель добавляет товар в корзину")
        print("5. Покупатель совершает покупку")
        print("6. Вывести всех покупателей")
        print("7. Вывести всех продавцов")
        print("8. Вывести товары продавца")
        print("9. Проверить баланс счета продавца")
        print("10. Добавить акцию/скидку на товар")
        print("11. Выход")
       

        choice = input("Введите номер действия: ")

        if choice == "1":
            name = input("Введите имя покупателя: ")
            budget = float(input("Введите бюджет покупателя: "))
            customer = Customer(name, budget)
            market.add_customer(customer)

        elif choice == "2":
            name = input("Введите имя продавца: ")
            seller = Seller(name)
            market.add_seller(seller)

        elif choice == "3":
            seller_name = input("Введите имя продавца: ")
            seller = market.find_seller(seller_name)
            if seller:
                product_name = input("Введите название товара: ")

                price = float(input("Введите цену товара: "))
                expiration_date = input("Введите дату истечения срока годности (ГГГГ-ММ-ДД): ")
                seller.add_product(product_name, price, expiration_date)
            else:
                print(f"Продавец с именем '{seller_name}' не найден.")

        elif choice == "4":
            customer_name = input("Введите имя покупателя: ")
            customer = market.find_customer(customer_name)
            if customer:
                seller_name = input("Введите имя продавца: ")
                seller = market.find_seller(seller_name)
                if seller:
                    product_name = input("Введите название товара: ")
                    quantity = int(input("Введите количество: "))
                    customer.add_to_cart(seller, product_name, quantity)
                else:
                    print(f"Продавец с именем '{seller_name}' не найден.")
            else:
                print(f"Покупатель с именем '{customer_name}' не найден.")

        elif choice == "5":
            customer_name = input("Введите имя покупателя: ")
            customer = market.find_customer(customer_name)
            if customer:
                seller_name = input("Введите имя продавца: ")
                seller = market.find_seller(seller_name)
                if seller:
                    customer.purchase(seller)
                else:
                    print(f"Продавец с именем '{seller_name}' не найден.")
            else:
                print(f"Покупатель с именем '{customer_name}' не найден.")

        elif choice == "6":
            market.show_customers()

        elif choice == "7":
            market.show_sellers()

        elif choice == "8":
            seller_name = input("Введите имя продавца: ")
            seller = market.find_seller(seller_name)
            if seller:
                seller.show_products()
            else:
                print(f"Продавец с именем '{seller_name}' не найден.")
                
        elif choice == "9":
            seller_name = input("Введите имя продавца: ")
            seller = market.find_seller(seller_name)
            if seller:
                print(f"Баланс счета продавца {seller.name}: {seller.account:.2f}")
            else:
                print(f"Продавец с именем '{seller_name}' не найден.")

        elif choice == "10":
            seller_name = input("Введите имя продавца: ")
            seller = market.find_seller(seller_name)
            if seller:
                product_name = input("Введите название товара: ")
                discount_percent = float(input("Введите процент скидки: "))
                seller.add_promotion(product_name, discount_percent)
            else:
                print(f"Продавец с именем '{seller_name}' не найден.")

        elif choice == "11":
            print("Спасибо за использование рынка. До свидания!")
            break
        
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    run_market()