import unittest
from controllers.phone_controller import PhoneController
from models.phone import Phone


class TestPhoneController(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр контроллера и добавляем в него несколько телефонных записей для тестирования
        self.controller = PhoneController()
        self.controller.add_phone(Phone("Иванов Иван", "123456", "ул. Ленина, д. 1", "+79101234567", "+74951234567"))
        self.controller.add_phone(Phone("Петров Петр", "123457", "ул. Пушкина, д. 2", "+79101234568", "+74951234568"))

    def test_add_phone(self):
        # Проверяем, что телефонная запись успешно добавлена в контроллер
        new_phone = Phone("Сидоров Сидор", "123458", "ул. Садовая, д. 3", "+79101234569", "+74951234569")
        self.controller.add_phone(new_phone)
        self.assertIn(new_phone, self.controller.phone_list)

    def test_delete_phone(self):
        # Проверяем, что телефонная запись успешно удаляется из контроллера
        phone_to_delete = self.controller.phone_list[0]
        self.controller.delete_phone("ФИО клиента или номер телефона", "Иванов Иван")
        self.assertNotIn(phone_to_delete, self.controller.phone_list)

    def test_search_phone_by_name_or_number(self):
        # Проверяем, что метод поиска по имени или номеру возвращает правильный результат
        results = self.controller.search_phone("ФИО клиента или номер телефона", "Иванов Иван")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Иванов Иван")

    def test_search_phone_by_account_or_address(self):
        # Проверяем, что метод поиска по номеру счета или адресу возвращает правильный результат
        results = self.controller.search_phone("Номер счета или адрес", "ул. Пушкина, д. 2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].address, "ул. Пушкина, д. 2")

    def test_search_phone_by_name_and_digits_in_number(self):
        # Проверяем, что метод поиска по имени и цифрам в номере возвращает правильный результат
        results = self.controller.search_phone("ФИО клиента и цифры в номере", "Петр")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Петров Петр")

    def test_save_and_load_data(self):
        # Проверяем, что сохраненные данные могут быть успешно загружены обратно
        file_path = "test_data.xml"
        self.controller.save_data(file_path)

        # Создаем новый экземпляр контроллера и загружаем данные из файла
        new_controller = PhoneController()
        new_controller.load_data(file_path)

        # Проверяем, что количество телефонных записей после загрузки соответствует ожидаемому
        self.assertEqual(len(new_controller.phone_list), len(self.controller.phone_list))


if __name__ == "__main__":
    unittest.main()
