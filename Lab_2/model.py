import xml.etree.ElementTree as ET

class Product:
    def __init__(self, name, manufacturer_name, unp, quantity, warehouse_address):
        self.name = name
        self.manufacturer_name = manufacturer_name
        self.unp = unp
        self.quantity = quantity
        self.warehouse_address = warehouse_address

    def to_xml_element(self):
        product_elem = ET.Element('product')
        ET.SubElement(product_elem, 'name').text = self.name
        ET.SubElement(product_elem, 'manufacturer_name').text = self.manufacturer_name
        ET.SubElement(product_elem, 'unp').text = self.unp
        ET.SubElement(product_elem, 'quantity').text = str(self.quantity)
        ET.SubElement(product_elem, 'warehouse_address').text = self.warehouse_address
        return product_elem

    @classmethod
    def from_xml_element(cls, element):
        name = element.find('name').text
        manufacturer_name = element.find('manufacturer_name').text
        unp = element.find('unp').text
        quantity = int(element.find('quantity').text)
        warehouse_address = element.find('warehouse_address').text
        return cls(name, manufacturer_name, unp, quantity, warehouse_address)

class ProductModel:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product_by_criteria(self, criteria, value):
        removed_products = []
        for product in self.products:
            product_value = getattr(product, criteria)
            if isinstance(product_value, int):
                if product_value == int(value):
                    removed_products.append(product)
            else:
                if product_value.lower() == value.lower():
                    removed_products.append(product)

        for product in removed_products:
            self.products.remove(product)

        return removed_products

    def find_products_by_name_or_quantity(self, search_value):
        matching_products = []
        for product in self.products:
            if product.name.lower() == search_value.lower() or str(product.quantity) == search_value:
                matching_products.append(product)
        return matching_products

    def find_products_by_manufacturer_or_unp(self, search_value):
        matching_products = []
        for product in self.products:
            if product.manufacturer_name.lower() == search_value.lower() or product.unp == search_value:
                matching_products.append(product)
        return matching_products

    def find_products_by_storage_address(self, search_value):
        matching_products = []
        for product in self.products:
            if product.warehouse_address.lower() == search_value.lower():
                matching_products.append(product)
        return matching_products

    def load_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        self.products = [Product.from_xml_element(elem) for elem in root.findall('product')]

    def save_to_xml(self, file_path):
        root = ET.Element('products')
        for product in self.products:
            root.append(product.to_xml_element())
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)

    def get_products(self):
        return self.products