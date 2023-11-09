from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic
from DB import DBDict
import datetime


class MainWindow(QMainWindow):
    family_members = []

    def __init__(self):
        super().__init__()

        uic.loadUi("views/resources/main-window.ui", self)
        self.show()

        self.update_manager_list()
        self.update_service_list()
        self.update_project_list()

        self.insertManager.clicked.connect(self.insert_manager)
        self.insertProject.clicked.connect(self.insert_project)
        self.appendSibling.clicked.connect(self.append_sibling)

    def insert_manager(self):
        dpi     = self.dpi.text()
        name    = self.name.text()
        address = self.address.text()

        DBDict.insert_manager(name, address, dpi)

        self.dpi.clear()
        self.name.clear()
        self.address.clear()

        self.update_manager_list()

    def append_sibling(self):
        age  = self.age.text()
        name = self.sibling_name.text()

        self.family_members.append({
            'name': name,
            'age' : age,
        })

        self.update_member_list()

        self.age.clear()
        self.sibling_name.clear()

    def insert_project(self):
        try:
            name           = self.project_name.text()
            budget         = self.budget.text()
            address        = self.family_address.text()
            last_name      = self.last_name.text()
            start_date     = datetime.datetime.now()
            manager_name     = self.manager_id.itemText(self.manager_id.currentIndex())
            service_id     = self.service_id.itemText(self.service_id.currentIndex())
            family_members = self.family_members
            monthly_income = self.monthly_income.text()

            manager_id = DBDict.find_managers({"_id": 1}, {"name": manager_name})[0]["_id"]
            DBDict.insert_project(name, start_date, budget, manager_id, address, monthly_income, last_name, family_members, service_id, False)

            self.budget.clear()
            self.last_name.clear()
            self.family_members = []
            self.project_name.clear()
            self.family_address.clear()
            self.monthly_income.clear()
            self.manager_id.setCurrentIndex(0)
            self.service_id.setCurrentIndex(0)

            self.update_member_list()
            self.update_project_list()

        except Exception as e:
            print(e)

    def update_manager_list(self):
        try:
            cursor = DBDict.find_managers()

            strings = []
            for document in cursor:
                string = str(document)
                strings.append(string)

            joined_strings = '\n'.join(strings)
            lines = joined_strings.split('\n')

            self.manager_id.clear()
            self.manager_table.setRowCount(0)
            self.manager_id.addItem('--Seleccionar--')

            for line in lines:
                data = line.split(':')
                columns = []

                for dato in data:
                    columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.manager_table.insertRow(self.manager_table.rowCount())
                self.manager_table.setItem(self.manager_table.rowCount() - 1, 0, QTableWidgetItem(columns[2]))
                self.manager_table.setItem(self.manager_table.rowCount() - 1, 1, QTableWidgetItem(columns[3]))
                self.manager_table.setItem(self.manager_table.rowCount() - 1, 2, QTableWidgetItem(columns[4]))

                self.manager_id.addItem(columns[2].replace("'", ''))

            self.manager_logs.setText(joined_strings)

        except Exception as e:
            print(e)

    def update_service_list(self):
        cursor = DBDict.find_services()

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        self.service_id.clear()
        self.service_id.addItem('--Seleccionar--')

        for line in lines:
            data = line.split(':')
            columns = []

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

            self.service_id.addItem(columns[2].replace("'", ''))

    def update_member_list(self):
        model = QStandardItemModel()

        if self.family_members:

            for value in self.family_members:
                standard_item = QStandardItem(f"{value['name']}, {value['age']}")
                model.appendRow(standard_item)

        self.member_list.setModel(model)

    def update_project_list(self):
        try:
            cursor = DBDict.find_projects()

            strings = []
            for document in cursor:
                string = str(document)
                strings.append(string)

            joined_strings = '\n'.join(strings)
            lines = joined_strings.split('\n')

            self.project_table.hide()
            # self.project_table.setRowCount(0)
            #
            # for line in lines:
            #     data = line.split(':')
            #     columns = []
            #
            #     for dato in data:
            #         columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))
            #
            #     print(columns)
            #
            #     self.project_table.insertRow(self.project_table.rowCount())
            #     self.project_table.setItem(self.project_table.rowCount() - 1, 0, QTableWidgetItem(columns[2]))
            #     self.project_table.setItem(self.project_table.rowCount() - 1, 1, QTableWidgetItem(columns[5]))
            #     self.project_table.setItem(self.project_table.rowCount() - 1, 2, QTableWidgetItem(columns[6]))
            #     self.project_table.setItem(self.project_table.rowCount() - 1, 3, QTableWidgetItem(columns[8]))
            #     self.project_table.setItem(self.project_table.rowCount() - 1, 4, QTableWidgetItem(columns[9]))

            self.project_logs.setText(joined_strings)

        except Exception as e:
            print(e)
