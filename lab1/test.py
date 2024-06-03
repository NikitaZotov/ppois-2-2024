#  coverage report -m
#  coverage run -m unittest discover
from unittest.mock import MagicMock
import unittest

from SiteStructure.site import Site
from SiteStructure.clothes import Clothes, ClothingCategory
from SiteStructure.customer import Customer
from SiteStructure.seller import Seller
from SiteStructure.shoppingCart import ShoppingCart
from SiteStructure.delivery import Delivery


class TestClothes(unittest.TestCase):

    def setUp(self):
        self.category = ClothingCategory()
        self.category.set_category(1)
        self.seller = MagicMock(spec=Seller)
        self.clothes = Clothes("shirt", 25, self.category.get_category(), self.seller)

    def test_category(self):
        self.assertEqual("shirts", self.category.get_category())

    def test_clothes(self):
        self.assertEqual("shirt", self.clothes.get_name())
        self.assertEqual(25, self.clothes.get_price())
        self.assertEqual("shirts", self.clothes.get_category())
        self.assertEqual(self.seller, self.clothes.get_seller())


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.product = MagicMock(spec=Clothes)
        self.cart = MagicMock(spec=ShoppingCart)
        self.customer = Customer("Bob", 200)

    def test_customer(self):
        self.customer.get_delivery().add_to_delivery(self.product)
        self.customer.get_cart().add_to_cart(self.product)
        self.assertEqual("Bob", self.customer.get_name())
        self.assertEqual(200, self.customer.get_wallet())
        self.assertIn(self.product, self.customer.get_cart().get_cart_list())
        self.assertIn(self.product, self.customer.get_delivery().get_delivery())
        self.customer.change_wallet(200)
        self.assertEqual(400, self.customer.get_wallet())
        self.customer.get_delivery().remove_delivery(self.product)
        self.assertNotIn(self.product, self.customer.get_delivery().get_delivery())
        self.customer.get_cart().remove_from_cart(self.product)
        self.assertNotIn(self.product, self.customer.get_cart().get_cart_list())


class TestSeller(unittest.TestCase):

    def setUp(self):
        self.seller = Seller("Nike", 400)

    def test_seller(self):
        self.assertEqual("Nike", self.seller.get_name())
        self.assertEqual(400, self.seller.get_wallet())
        self.seller.change_wallet(-200)
        self.assertEqual(200, self.seller.get_wallet())


class TestSite(unittest.TestCase):

    def setUp(self):
        self.product = MagicMock(spec=Clothes)
        self.seller = MagicMock(spec=Seller)
        self.customer = MagicMock(spec=Customer)
        self.site = Site("123.ru")

    def test_site(self):
        self.site.add_product(self.product)
        self.site.add_seller(self.seller)
        self.site.add_customer(self.customer)
        self.assertEqual("123.ru", self.site.get_name())
        self.assertIn(self.product, self.site.get_products())
        self.assertIn(self.seller, self.site.get_sellers())
        self.assertIn(self.customer, self.site.get_customers())


if __name__ == '__main__':
    unittest.main()
