import xml.etree.ElementTree as ET

class Model:
    def __init__(self):
        self.data = []

    def load_from_file(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        self.data = [{
            'product_name': child.find('product_name').text,
            'manufacturer_name': child.find('manufacturer_name').text,
            'manufacturer_id': child.find('manufacturer_id').text,
            'quantity': child.find('quantity').text,
            'warehouse_address': child.find('warehouse_address').text
        } for child in root.findall('product')]

    def save_to_file(self, filename):
        root = ET.Element("products")
        for item in self.data:
            product = ET.SubElement(root, 'product')
            ET.SubElement(product, 'product_name').text = item['product_name']
            ET.SubElement(product, 'manufacturer_name').text = item['manufacturer_name']
            ET.SubElement(product, 'manufacturer_id').text = item['manufacturer_id']
            ET.SubElement(product, 'quantity').text = item['quantity']
            ET.SubElement(product, 'warehouse_address').text = item['warehouse_address']
        tree = ET.ElementTree(root)
        tree.write(filename)

    def add_product(self, product):
        self.data.append(product)

    def search_product(self, search_criteria):
        def match_criteria(item):
            for key, value in search_criteria.items():
                if item[key] != value:
                    return False
            return True

        return [item for item in self.data if match_criteria(item)]

    def delete_product(self, delete_criteria):
        def match_criteria(item):
            for key, value in delete_criteria.items():
                if item[key] != value:
                    return False
            return True

        self.data = [item for item in self.data if not match_criteria(item)]
