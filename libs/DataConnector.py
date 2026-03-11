import json
import os


import json
import os

from libs.FileFactory import JsonFileFactory


class DataConnector:

    def __init__(self, employee_file_path=None, manager_file_path=None):
        self.employee_file_path = employee_file_path or "../datasets/employees.json"
        self.manager_file_path = manager_file_path or "../datasets/managers.json"

    def _read_json_file(self, file_path):

        if not file_path or not os.path.exists(file_path):
            print(f"File '{file_path}' không tồn tại!")
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, dict) and "managers" in data:
                    return data["managers"]
                if isinstance(data, dict) and "employees" in data:
                    return data["employees"]
                if isinstance(data, list):
                    return data

                return []

        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc file JSON '{file_path}': {e}")
            return []

    def read_employees(self):
        employees = self._read_json_file(self.employee_file_path)

        for emp in employees:
            emp["EmployeeName"] = emp.get("EmployeeName", "").strip().lower()
            emp["Password"] = str(emp.get("Password", "")).strip()

        return employees

    def validate_employee_login(self, username, password):

        employees = self.read_employees()

        username = username.strip().lower()
        password = password.strip()

        for emp in employees:

            stored_username = emp.get("EmployeeName", "").strip().lower()
            stored_password = str(emp.get("Password", "")).strip()

            if stored_username == username and stored_password == password:
                return emp

        return None

    def read_managers(self):
        managers = self._read_json_file(self.manager_file_path)

        # Chuẩn hóa dữ liệu: Xóa khoảng trắng thừa và chuyển username về chữ thường
        for manager in managers:
            manager["ManagerUsername"] = manager.get("ManagerUsername", "").strip()
            manager["ManagerPassword"] = manager.get("ManagerPassword", "").strip()

        return managers

    def validate_manager_login(self, username, password):

        managers = self.read_managers()

        username = username.strip().lower()
        password = password.strip()

        for manager in managers:

            stored_username = manager.get("ManagerUsername", "").strip().lower()
            stored_password = manager.get("ManagerPassword", "").strip()

            if stored_username == username and stored_password == password:
                return manager

        return None
