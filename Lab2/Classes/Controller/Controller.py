from PyQt5.QtWidgets import QFileDialog

from Classes.Model.scheduleOfTrains import ScheduleOfTrains
from Classes.Model.ReadInfoFromFile import ReadFromFile
from Classes.View.Ui_MainWindow import Ui_MainWindow
from Classes.View.UI_AddWindow import Ui_AddWindow
from Classes.View.Ui_FindWindow import Ui_FindWindow
from Classes.View.Ui_RemoveWindow import Ui_RemoveWindow
from Classes.View.Ui_SettingWindow import Ui_SettingWindow
from Classes.View.Ui_MessageWindow import MessageWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from datetime import datetime, timedelta, date
import sys
import xml.sax
from xml.dom.minidom import Document

class Controller:

    def __init__(self):
        self._schedule_of_trains = ScheduleOfTrains()
        self._ui = Ui_MainWindow()
        self._list_to_del = []

    def start(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.update_main_menu()
        sys.exit(self.app.exec_())

    def update_main_menu(self):
        self._ui.setupUi(self.MainWindow, self._schedule_of_trains.list_of_trains)
        self.MainWindow.show()
        self.all_functions_of_main_window()

    def resize_of_table(self, count_of_records_in_page):
        if count_of_records_in_page == 5:
            return (65,12, 0)
        elif count_of_records_in_page == 8:
            return (40,12, 1)
        elif count_of_records_in_page == 10:
            return (33,10, 2)
        elif count_of_records_in_page == 15:
            return (22,8, 3)

    def size_of_rows_of_last_table(self, count_of_records_in_page):
        count_of_records = self._schedule_of_trains.count_of_records()
        if count_of_records % count_of_records_in_page == 0:
            return count_of_records_in_page
        else:
            return count_of_records % count_of_records_in_page

    def size_of_tableWidget(self, count_of_records_in_page):
        count_of_records = self._schedule_of_trains.count_of_records()
        if count_of_records % count_of_records_in_page == 0:
            return count_of_records // count_of_records_in_page
        else:
            return count_of_records // count_of_records_in_page + 1

    def all_functions_of_main_window(self):
        self._ui.AddTrain.clicked.connect(lambda: self.add_window())
        self._ui.FindTrain.clicked.connect(lambda: self.find_window())
        self._ui.RemoveTrain.clicked.connect(lambda: self.remove_window())

        self._ui.Save.clicked.connect(lambda: self.save_window())

        self._ui.AddRecordMenu.triggered.connect(lambda: self.add_window())
        self._ui.RemoveRecordMenu.triggered.connect(lambda: self.remove_window())
        self._ui.FindRecordMenu.triggered.connect(lambda: self.find_window())
        self._ui.ClearMenu.triggered.connect(lambda: self.clear_list_of_trains())

        self._ui.SettingMenu.triggered.connect(lambda: self.setting_window())
        self._ui.OpenMenu.triggered.connect(lambda: self.open_window())
        self._ui.SaveMenu.triggered.connect(lambda: self.save_window())

    def open_window(self):
        res = QFileDialog.getOpenFileName(self.MainWindow, 'Открыть файл', r'D:\BSUIR\Sem 4\ППОИС\Lab2\ ' 'XML files ', '*.xml')
        file_path = res[0]
        if file_path:
            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            schedule = ScheduleOfTrains()
            handler = ReadFromFile(schedule)
            parser.setContentHandler(handler)

            parser.parse(file_path)
            trains = handler.get_trains()
            self._schedule_of_trains.copy_list_of_trains(trains)
            self._ui.count_of_pages = self.size_of_tableWidget(self._ui.count_of_records_in_page)
            self._ui.count_of_records_on_last_page = self.size_of_rows_of_last_table(self._ui.count_of_records_in_page)
            self.update_main_menu()
        else:
            MessageWindow.show_error_message("Не удалось открыть файл")


    def save_window(self):
        res = QFileDialog.getSaveFileName(self.MainWindow, 'Сохранить файл', r'D:\BSUIR\Sem 4\ППОИС\Lab2\ ' 'XML1 ', '*.xml')
        file_path = res[0]
        if file_path:
            doc = Document()

            root = doc.createElement('trains')
            doc.appendChild(root)

            for train in self._schedule_of_trains.list_of_trains:
                train_element = doc.createElement('train')

                number_element = doc.createElement('number')
                number_element.appendChild(doc.createTextNode(train._number_of_train))
                train_element.appendChild(number_element)

                first_station_element = doc.createElement('first_station')
                first_station_element.appendChild(doc.createTextNode(train._first_station))
                train_element.appendChild(first_station_element)

                last_station_element = doc.createElement('last_station')
                last_station_element.appendChild(doc.createTextNode(train._last_station))
                train_element.appendChild(last_station_element)

                departure_time_element = doc.createElement('departure_time')
                departure_time_element.appendChild(doc.createTextNode(train._departure_time.strftime("%d-%m-%Y %H:%M")))
                train_element.appendChild(departure_time_element)

                arrival_time_element = doc.createElement('arrival_time')
                arrival_time_element.appendChild(doc.createTextNode(train._arrival_time.strftime("%d-%m-%Y %H:%M")))
                train_element.appendChild(arrival_time_element)

                root.appendChild(train_element)

            xml_str = doc.toprettyxml(indent="  ")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(xml_str)
            MessageWindow.show_information_message("Данные успешно сохранены")
        else:
            MessageWindow.show_error_message("Не удалось открыть файл")

    def add_window(self):
        self.addWindow = QtWidgets.QMainWindow()
        self.ui_add_window = Ui_AddWindow()
        self.ui_add_window.setupUi(self.addWindow)
        self.addWindow.show()
        self.all_functions_of_add_window()

    def all_functions_of_add_window(self):
        self.ui_add_window.pushButtonToCancel.clicked.connect(lambda: self.close_add_window_and_show_message("Новый маршрут не был добавлен"))
        self.ui_add_window.pushButtonToAdd.clicked.connect(lambda: self.check_input_information())

    def close_add_window_and_show_message(self, informative_text):
        self.addWindow.close()
        MessageWindow.show_information_message(informative_text)

    def check_input_information(self):
        code = self.ui_add_window.inputCodeOfTrain.text()
        dupartureDateTime = datetime.combine(self.ui_add_window.departureDate.date().toPyDate(), self.ui_add_window.departureTime.time().toPyTime())
        arrivalDateTime = datetime.combine(self.ui_add_window.arrivalDate.date().toPyDate(), self.ui_add_window.arrivalTime.time().toPyTime())
        seven_days = timedelta(days=7)
        three_minutes = timedelta(minutes=3)
        newYear = datetime(2025,1,1,00,00)
        format_string = "%d-%m-%Y %H:%M"
        if code == "000":
            MessageWindow.show_error_message("Номер поезда должен быть отличен от 000")
        elif not code.isdigit():
            MessageWindow.show_error_message("Номер поезда должен состоять только из цифр")
        elif self.ui_add_window.departurePoint.currentIndex() == 0:
            MessageWindow.show_error_message("Не указан пункт отправления")
        elif self.ui_add_window.arrivalPoint.currentIndex() == 0:
            MessageWindow.show_error_message("Не указан пункт прибытия")
        elif self.ui_add_window.departurePoint.currentIndex() == self.ui_add_window.arrivalPoint.currentIndex():
            MessageWindow.show_error_message("Пункт отправления и пункт прибытия должны быть разными")
        elif dupartureDateTime >= newYear:
            MessageWindow.show_error_message("Слишком большая дата отправления")
        elif arrivalDateTime >= newYear:
            MessageWindow.show_error_message("Слишком большая дата прибытия")
        elif dupartureDateTime >= arrivalDateTime:
            MessageWindow.show_error_message("Дата и время прибытия не должны быть раньше даты и времени отправления или совпадать")
        elif arrivalDateTime - dupartureDateTime >= seven_days:
            MessageWindow.show_error_message("Время в пути не должно привышать 7 дней")
        elif arrivalDateTime - dupartureDateTime < three_minutes:
            MessageWindow.show_error_message("Время в пути должно привышать 3 минуты")
        else:
            self._schedule_of_trains.addNewTrain(code, self.ui_add_window.departurePoint.currentText(), self.ui_add_window.arrivalPoint.currentText(), dupartureDateTime.strftime(format_string), arrivalDateTime.strftime(format_string))
            self._ui.count_of_pages = self.size_of_tableWidget(self._ui.count_of_records_in_page)
            self._ui.count_of_records_on_last_page = self.size_of_rows_of_last_table(self._ui.count_of_records_in_page)
            self.update_main_menu()
            self.close_add_window_and_show_message("Новый маршрут успешно добавлен")

    def find_window(self):
        self.findWindow = QtWidgets.QMainWindow()
        self.ui_find_window = Ui_FindWindow()
        self.update_find_window([])

    def update_find_window(self, list_of_trains):
        self.ui_find_window.setupUi(self.findWindow, list_of_trains)
        self.findWindow.show()
        self.all_functions_of_find_window()

    def all_functions_of_find_window(self):
        self.ui_find_window.btnCancel.clicked.connect(lambda: self.close_find_window_and_show_message(""))
        self.ui_find_window.btnOk.clicked.connect(lambda: self.close_find_window_and_show_message(""))

        self.ui_find_window.btnFind.clicked.connect(lambda: self.search_info())

    def close_find_window_and_show_message(self, informative_text):
        self.findWindow.close()
        MessageWindow.show_information_message(informative_text)

    def search_info(self):
        new_list = []
        if self.ui_find_window.selectionOfSearchParameter.currentIndex() == 0:
            MessageWindow.show_error_message("Не выбран параметр поиска")
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 1:
            code = self.ui_find_window.inputCodeOfTrain.text()
            if code == "000":
                MessageWindow.show_error_message("Номер поезда должен быть отличен от 000")
            elif not code.isdigit():
                MessageWindow.show_error_message("Номер поезда должен состоять только из цифр")
            else:
                new_list = self._schedule_of_trains.search_by_code_train(code)
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 2:
            if self.ui_find_window.departurePoint.currentIndex() == 0:
                MessageWindow.show_error_message("Не указан пункт отправления")
            else:
                new_list = self._schedule_of_trains.search_by_departure_point(self.ui_find_window.departurePoint.currentText())
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 3:
            if self.ui_find_window.arrivalPoint.currentIndex() == 0:
                MessageWindow.show_error_message("Не указан пункт прибытия")
            else:
                new_list = self._schedule_of_trains.search_by_arrival_point(self.ui_find_window.arrivalPoint.currentText())
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 4:
            duparture_date_str = self.ui_find_window.departureDate.date().toPyDate().strftime("%d-%m-%Y")
            duparture_date = datetime.strptime(duparture_date_str, "%d-%m-%Y").date()
            newYear = date(2025,1,1)
            if duparture_date >= newYear:
                MessageWindow.show_error_message("Слишком большая дата отправления")
            else:
                new_list = self._schedule_of_trains.search_by_departure_date(duparture_date_str)
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 5:
            duparture_time_low_limit_str = self.ui_find_window.departureTimeLowLimit.time().toPyTime().strftime("%H:%M")
            duparture_time_high_limit_str = self.ui_find_window.departureTimeHighLimit.time().toPyTime().strftime("%H:%M")
            if duparture_time_low_limit_str > duparture_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                new_list = self._schedule_of_trains.search_by_departure_time(duparture_time_low_limit_str, duparture_time_high_limit_str)
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 6:
            arrival_time_low_limit_str = self.ui_find_window.arrivalTimeLowLimit.time().toPyTime().strftime("%H:%M")
            arrival_time_high_limit_str = self.ui_find_window.arrivalTimeHighLimit.time().toPyTime().strftime("%H:%M")
            if arrival_time_low_limit_str > arrival_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                new_list = self._schedule_of_trains.search_by_arrival_time(arrival_time_low_limit_str, arrival_time_high_limit_str)
        elif self.ui_find_window.selectionOfSearchParameter.currentIndex() == 7:
            travel_time_low_limit_str = self.ui_find_window.travelTimeLowLimit.time().toPyTime().strftime("%H:%M")
            travel_time_high_limit_str = self.ui_find_window.travelTimeHighLimit.time().toPyTime().strftime("%H:%M")
            count_of_days_low_limit = self.ui_find_window.countOfDaysLowLimit.currentText()
            count_of_days_high_limit = self.ui_find_window.countOfDaysHighLimit.currentText()
            if travel_time_low_limit_str > travel_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                new_list = self._schedule_of_trains.search_by_travel_time(travel_time_low_limit_str, travel_time_high_limit_str, count_of_days_low_limit, count_of_days_high_limit)
        self.update_find_window(new_list)

    def remove_window(self):
        self.removeWindow = QtWidgets.QMainWindow()
        self.ui_remove_window = Ui_RemoveWindow()
        self.update_remove_window([])

    def update_remove_window(self, list_of_trains):
        self.ui_remove_window.setupUi(self.removeWindow, list_of_trains)
        self.removeWindow.show()
        self.all_functions_of_remove_window()

    def all_functions_of_remove_window(self):
        self.ui_remove_window.btnCancel.clicked.connect(lambda: self.close_remove_window_and_show_message("Маршруты не были удалены"))
        self.ui_remove_window.btnDel.clicked.connect(lambda: self.remove_trains())
        self.ui_remove_window.btnFind.clicked.connect(lambda: self.search_info_to_del())

    def close_remove_window_and_show_message(self, informative_text):
        self.removeWindow.close()
        MessageWindow.show_information_message(informative_text)

    def search_info_to_del(self):
        self._list_to_del = []
        if self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 0:
            MessageWindow.show_error_message("Не выбран параметр поиска")
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 1:
            code = self.ui_remove_window.inputCodeOfTrain.text()
            if code == "000":
                MessageWindow.show_error_message("Номер поезда должен быть отличен от 000")
            elif not code.isdigit():
                MessageWindow.show_error_message("Номер поезда должен состоять только из цифр")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_code_train(code)
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 2:
            if self.ui_remove_window.departurePoint.currentIndex() == 0:
                MessageWindow.show_error_message("Не указан пункт отправления")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_departure_point(self.ui_remove_window.departurePoint.currentText())
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 3:
            if self.ui_remove_window.arrivalPoint.currentIndex() == 0:
                MessageWindow.show_error_message("Не указан пункт прибытия")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_arrival_point(self.ui_remove_window.arrivalPoint.currentText())
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 4:
            duparture_date_str = self.ui_remove_window.departureDate.date().toPyDate().strftime("%d-%m-%Y")
            duparture_date = datetime.strptime(duparture_date_str, "%d-%m-%Y").date()
            newYear = date(2025,1,1)
            if duparture_date >= newYear:
                MessageWindow.show_error_message("Слишком большая дата отправления")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_departure_date(duparture_date_str)
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 5:
            duparture_time_low_limit_str = self.ui_remove_window.departureTimeLowLimit.time().toPyTime().strftime("%H:%M")
            duparture_time_high_limit_str = self.ui_remove_window.departureTimeHighLimit.time().toPyTime().strftime("%H:%M")
            if duparture_time_low_limit_str > duparture_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_departure_time(duparture_time_low_limit_str, duparture_time_high_limit_str)
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 6:
            arrival_time_low_limit_str = self.ui_remove_window.arrivalTimeLowLimit.time().toPyTime().strftime("%H:%M")
            arrival_time_high_limit_str = self.ui_remove_window.arrivalTimeHighLimit.time().toPyTime().strftime("%H:%M")
            if arrival_time_low_limit_str > arrival_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_arrival_time(arrival_time_low_limit_str, arrival_time_high_limit_str)
        elif self.ui_remove_window.selectionOfSearchParameter.currentIndex() == 7:
            travel_time_low_limit_str = self.ui_remove_window.travelTimeLowLimit.time().toPyTime().strftime("%H:%M")
            travel_time_high_limit_str = self.ui_remove_window.travelTimeHighLimit.time().toPyTime().strftime("%H:%M")
            count_of_days_low_limit = self.ui_remove_window.countOfDaysLowLimit.currentText()
            count_of_days_high_limit = self.ui_remove_window.countOfDaysHighLimit.currentText()
            if travel_time_low_limit_str > travel_time_high_limit_str:
                MessageWindow.show_error_message("Нижний предел должен быть меньше верхнего")
            else:
                self._list_to_del = self._schedule_of_trains.search_by_travel_time(travel_time_low_limit_str, travel_time_high_limit_str, count_of_days_low_limit, count_of_days_high_limit)
        self.update_remove_window(self._list_to_del)

    def remove_trains(self):
        if not self._list_to_del:
            MessageWindow.show_error_message("Нет выбранных маршрутов")
        else:
            self._schedule_of_trains.removeTrain(self._list_to_del)
            self._list_to_del = []
            self.close_remove_window_and_show_message("Маршруты успешно удалены")
            if self._schedule_of_trains.list_of_trains == []:
                self._ui.count_of_pages = 1
                self._ui.count_of_records_on_last_page = 0
            else:
                self._ui.count_of_pages = self.size_of_tableWidget(self._ui.count_of_records_in_page)
                self._ui.count_of_records_on_last_page = self.size_of_rows_of_last_table(self._ui.count_of_records_in_page)
            self.update_main_menu()

    def clear_list_of_trains(self):
        if self._schedule_of_trains.list_of_trains:
            MessageWindow.show_information_message("Все маршруты успешно удалены")
            self._schedule_of_trains.clear_list()
            self._ui.count_of_pages = 1
            self._ui.count_of_records_on_last_page = 0
            self.update_main_menu()
        else:
            MessageWindow.show_error_message("Список маршрутов уже пуст")

    def setting_window(self):
        self.settingWindow = QtWidgets.QMainWindow()
        self.ui_setting_window = Ui_SettingWindow()
        index = self.resize_of_table(self._ui.count_of_records_in_page)[2]
        self.ui_setting_window.setupUi(self.settingWindow, index)
        self.settingWindow.show()
        self.all_functions_of_setting_window()

    def all_functions_of_setting_window(self):
        self.ui_setting_window.btnSave.clicked.connect(lambda: self.save_settings())

    def save_settings(self):
        size = int(self.ui_setting_window.comboBoxCountInPage.currentText())
        new_size = self.resize_of_table(size)
        self._ui.count_of_records_in_page = size
        self._ui.size_of_item = new_size[0]
        self._ui.size_of_font = new_size[1]
        self._ui.count_of_pages = self.size_of_tableWidget(self._ui.count_of_records_in_page)
        self._ui.count_of_records_on_last_page = self.size_of_rows_of_last_table(self._ui.count_of_records_in_page)
        self.update_main_menu()
        self.close_setting_window_and_show_message("Настройки были сохранены")

    def close_setting_window_and_show_message(self, informative_text):
        self.settingWindow.close()
        MessageWindow.show_information_message(informative_text)