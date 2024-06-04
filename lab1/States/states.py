import time
from statemachine import State
from statemachine import StateMachine

from SiteStructure.site import Site
from SiteStructure.clothes import Clothes, ClothingCategory
from SiteStructure.customer import Customer
from SiteStructure.seller import Seller
from SiteStructure.shoppingCart import ShoppingCart

from Save.file import File

from Exceptions.exceptions import File_Exception


class SiteStates(StateMachine):
    view_sites = State(initial=True)
    add_site = State()
    view_site = State()
    view_products = State()
    add_product = State()
    add_seller = State()
    view_seller = State()
    add_customer = State()
    view_customers = State()
    view_customer = State()
    view_cart = State()
    add_to_cart = State()
    remove_from_cart = State()
    add_to_wallet = State()
    check_wallet = State()
    search = State()
    payment = State()
    delivery_status = State()
    delivery_view = State()
    handle_return = State()
    exit_ = State(final=True)

    next_state = (
        exit_.from_(view_sites, cond="navigating_backwards")
        ######
        | view_sites.from_(view_site, cond="navigating_backwards")
        | view_sites.to(view_site, cond="navigating_by_index")

        | view_sites.from_(add_site)
        | view_sites.to(add_site, cond="navigating_add")
        ######
        | view_site.from_(add_product)
        | view_site.to(add_product, cond="navigating_add_product")

        | view_site.from_(add_seller)
        | view_site.to(add_seller, cond="navigating_add_seller")

        | view_site.from_(view_seller, cond="navigating_backwards")
        | view_site.to(view_seller, cond="navigating_view")

        | view_site.from_(add_customer)
        | view_site.to(add_customer, cond="navigating_add_customer")

        | view_site.from_(view_products, cond="navigating_backwards")
        | view_site.to(view_products, cond="navigating_view_products")

        | view_site.from_(view_customers, cond="navigating_backwards")
        | view_site.to(view_customers, cond="navigating_view_customers")
        #######
        | view_customers.from_(view_customer, cond="navigating_backwards")
        | view_customers.to(view_customer, cond="navigating_by_index")

        | view_customer.from_(view_cart, cond="navigating_backwards")
        | view_customer.to(view_cart, cond="navigating_view")

        | view_customer.from_(add_to_cart)
        | view_customer.to(add_to_cart, cond="navigating_add")

        | view_customer.from_(remove_from_cart)
        | view_customer.to(remove_from_cart, cond="navigating_remove")

        | view_customer.from_(add_to_wallet)
        | view_customer.to(add_to_wallet, cond="navigating_add_to_wallet")

        | view_customer.from_(check_wallet, cond="navigating_backwards")
        | view_customer.to(check_wallet, cond="navigating_view_wallet")

        | view_customer.from_(search, cond="navigating_backwards")
        | view_customer.to(search, cond="navigating_search")

        | view_customer.from_(payment, cond="navigating_backwards")
        | view_customer.to(payment, cond="navigating_payment")

        | payment.from_(delivery_status, cond="navigating_backwards")
        | payment.to(delivery_status, cond="navigating_view")

        | delivery_status.from_(delivery_view, cond="navigating_backwards")
        | delivery_status.to(delivery_view, cond="navigating_view")

        | delivery_status.from_(handle_return, cond="navigating_backwards")
        | delivery_status.to(handle_return, cond="navigating_remove")

    )

    def __init__(self, file: File):
        self.file: File = file
        self.selected_index: int
        self.selected_site: Site
        self.selected_customer: Customer

        try:
            print("Loading state...")
            self.sites: list[Site] = file.load()

        except File_Exception:

            self.sites: list[Site] = []

        super().__init__()  # call the constructor of the parent class (StateMachine)

    def navigating_backwards(self, input_: str) -> bool:
        return input_ == 'q'

    def navigating_yes(self, input_: str) -> bool:
        return input_ == 'y'

    def navigating_no(self, input_: str) -> bool:
        return input_ == 'n'

    def navigating_add(self, input_: str) -> bool:
        return input_ == 'a'

    def navigating_add_seller(self, input_: str) -> bool:
        return input_ == 'as'

    def navigating_add_customer(self, input_: str) -> bool:
        return input_ == 'ac'

    def navigating_add_product(self, input_: str) -> bool:
        return input_ == 'ap'

    def navigating_by_index(self, input_: str) -> bool:
        if input_.isnumeric():
            self.selected_index = int(input_)
            return True
        else:
            return False

    def navigating_view_products(self, input_: str) -> bool:
        return input_ == 'p'

    def navigating_view_customers(self, input_: str) -> bool:
        return input_ == 'c'

    def navigating_remove(self, input_: str) -> bool:
        return input_ == 'r'

    def navigating_view(self, input_: str) -> bool:
        return input_ == 'v'

    def navigating_add_to_wallet(self, input_: str) -> bool:
        return input_ == 'tw'

    def navigating_view_wallet(self, input_: str) -> bool:
        return input_ == 'vw'

    def navigating_search(self, input_: str) -> bool:
        return input_ == 's'

    def navigating_payment(self, input_: str) -> bool:
        return input_ == 'p'


    def on_enter_view_sites(self):
        self.selected_site = None
        print("\nList of sites:")
        for i in range(len(self.sites)):
            print(f"{i} - {self.sites[i].get_name()}")
        print("a - add")
        if self.sites:
            print("enter index to view site")

    def on_enter_view_site(self):
        if len(self.sites) <= self.selected_index:
            print("Wrong index\nTry again")
            self.next_state('q')
            return
        if self.selected_site is None:
            self.selected_site = self.sites[self.selected_index]
        print(f"\nSite {self.selected_site.get_name()}")
        print("ap - add product")
        print("as - add seller")
        print("ac - add customer")
        print("v - view sellers")
        print("p - view products")
        print("c - view customers")

    def on_enter_add_site(self):
        site = Site(input(f"Input site name: "))
        self.sites.append(site)
        print(f"Site {site.get_name()} added")
        self.next_state()


    def on_enter_add_product(self):
        sellers: list[Seller] = self.selected_site.get_sellers()
        if not sellers:
            print("Add seller")
            self.next_state('q')
            return
        print("Enter clothes:")
        name: str = input(f"Name: ")
        price: int = int(input(f"Price: "))
        print("Choose category index:")
        category = ClothingCategory()
        for i in range(len(category.get_category_list())):
            print(f"{i+1} - {category.get_category_list()[i+1]}")
        category.set_category(int(input()))

        print(f"Sellers: ")
        for i in range(len(sellers)):
            print(f"{i} - {sellers[i].get_name()}")
        number: int = int(input(f"Chose seller: "))
        product = Clothes(name, price, category.get_category(), sellers[number])
        self.selected_site.add_product(product)
        self.next_state()

    def on_enter_add_seller(self):
        print("Enter seller:")
        name: str = input(f"Name: ")
        wallet: int = int(input(f"Money: "))
        seller = Seller(name, wallet)
        self.selected_site.add_seller(seller)
        self.next_state()

    def on_enter_view_seller(self):
        sellers = self.selected_site.get_sellers()
        if not sellers:
            print("Add seller")
            self.next_state('q')
            return
        for i in range(len(sellers)):
            print(f"{i} - name: {sellers[i].get_name()} wallet: {sellers[i].get_wallet()}")
        self.next_state('q')

    def on_enter_add_customer(self):
        print("Enter customer:")
        name: str = input(f"Name: ")
        wallet: int = int(input(f"Money: "))
        customer = Customer(name, wallet)
        self.selected_site.add_customer(customer)
        self.next_state()

    def on_enter_view_products(self):
        products = self.selected_site.get_products()
        if not products:
            print("Nothing to view")
            self.next_state('q')
            return
        for i in range(len(products)):
            print(f"{i} - {products[i].get_name()} {products[i].get_price()} "
                  f"{products[i].get_category()} {products[i].get_seller().get_name()}")
        self.next_state('q')

    def on_enter_view_customers(self):
        self.selected_customer = None
        customers = self.selected_site.get_customers()
        if not customers:
            print("Add customer to site")
            self.next_state('q')
            return
        print("\nList of customers:")
        for i in range(len(customers)):
            print(f"{i} - {customers[i].get_name()}")

    def on_enter_view_customer(self):
        customers = self.selected_site.get_customers()
        if len(customers) <= self.selected_index:
            print("Wrong index\nTry again")
            self.next_state('q')
            return
        if self.selected_customer is None:
            self.selected_customer = customers[self.selected_index]
        print(f"\nCustomer {self.selected_customer.get_name()}")
        print("tw - top up wallet")
        print("vw - view wallet")
        print("a - add to cart")
        print("r - remove from cart")
        print("v - view cart")
        print("s - search by category")
        print("p - payment")

    def on_enter_view_cart(self):
        cart = self.selected_customer.get_cart()
        if not cart.get_cart_list():
            print("Cart is empty")
            self.next_state('q')
            return
        for i in range(len(cart.get_cart_list())):
            print(f"{i} - {cart.get_cart_list()[i].get_name()} {cart.get_cart_list()[i].get_price()}")
        print(f"Total price: {cart.get_total_price()}")
        self.next_state('q')

    def on_enter_add_to_cart(self):
        products = self.selected_site.get_products()
        if not products:
            print("Add product to site")
            self.next_state('q')
            return
        print("Products:")
        for i in range(len(products)):
            print(f"{i} - name: {products[i].get_name()} price: {products[i].get_price()}")
        print(f"Choose product: ")
        choose = int(input())
        if choose >= len(products):
            print("Wrong index\nTry again")
            self.next_state('q')
            return
        cart: ShoppingCart = self.selected_customer.get_cart()
        cart.add_to_cart(products[choose])
        self.next_state()

    def on_enter_remove_from_cart(self):
        cart = self.selected_customer.get_cart()
        if not cart:
            print("Nothing to remove")
            self.next_state('q')
            return
        print("Chose product index:")
        for i in range(len(cart.get_cart_list())):
            print(f"{i} - {cart.get_cart_list()[i].get_name()} {cart.get_cart_list()[i].get_price()}")
        choose = int(input())
        cart.remove_from_cart(cart.get_cart_list()[choose])
        self.next_state()


    def on_enter_add_to_wallet(self):
        transfer = int(input(f"Enter amount of money: "))
        self.selected_customer.change_wallet(transfer)
        self.next_state()

    def on_enter_check_wallet(self):
        print(f"Wallet: {self.selected_customer.get_wallet()}")
        self.next_state('q')

    def on_enter_search(self):
        print(f"Category:")
        category = ClothingCategory()
        for i in range(len(category.get_category_list())):
            print(f"{i + 1} - {category.get_category_list()[i + 1]}")
        category.set_category(int(input("Choose category: ")))
        finded = self.selected_site.search_clothes(category.get_category())
        if not finded:
            print("Nothing find")
            self.next_state('q')
            return
        print("Findings: ")
        for i in range(len(finded)):
            print(f"{i} - {finded[i].get_name()}")
        self.next_state('q')

    def on_enter_payment(self):
        self.check = True
        if self.selected_customer.get_cart().get_total_price() == 0:
            print("Add something to cart")
            self.next_state('q')
            return
        if self.selected_customer.get_wallet() < self.selected_customer.get_cart().get_total_price():
            print("Not enough money")
            self.next_state('q')
            return
        self.selected_customer.change_wallet(-self.selected_customer.get_cart().get_total_price())
        products = self.selected_customer.get_cart().get_cart_list()
        for i in range(len(products)):
            products[i].get_seller().change_wallet(products[i].get_price())
        print("Payment successfully")
        for i in range(len(products)):
            self.selected_customer.get_delivery().add_to_delivery(products[i])
        products.clear()
        print("v - view delivery status")

    def on_enter_delivery_status(self):
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while (elapsed_time < 1 and self.check):
            elapsed_time = time.time() - start_time
            print(f"{elapsed_time:.1f} seconds")
            time.sleep(1)
        if self.check: print("Delivery successfully")
        print("v - view delivery")
        print("r - return delivery")

    def on_enter_delivery_view(self):
        self.check = False
        delivery = self.selected_customer.get_delivery().get_delivery()
        if not delivery:
            print("Empty")
            self.next_state('q')
            return
        for i, v in enumerate(delivery):
            print(f"{i} - {v.get_name()}")
        self.next_state('q')

    def on_enter_handle_return(self):
        self.check = False
        delivery = self.selected_customer.get_delivery()
        if not delivery.get_delivery():
            print("Nothing to return")
            self.next_state('q')
            return
        print("Choose return product:")
        for i, v in enumerate(delivery.get_delivery()):
            print(f"{i} - {v.get_name()}")
        choose = int(input())
        transfer = delivery.get_delivery()[choose].get_price()
        delivery.get_delivery()[choose].get_seller().change_wallet(-transfer)
        self.selected_customer.change_wallet(transfer)
        delivery.remove_delivery(delivery.get_delivery()[choose])
        print(f"Return {transfer} money")
        self.next_state('q')

    def on_enter_exit_(self):
        print("Saving state...")
        self.file.save(self.sites)
        exit()
