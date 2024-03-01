import json

class Employee:
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department

    def display_details(self):
        return f"Name: {self.name}, ID: {self.emp_id}, Title: {self.title}, Department: {self.department}"

    def __str__(self):
        return f"{self.name} - {self.emp_id}"


class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            self.employees.append(employee)
        else:
            print("Error: Invalid employee object.")

    def remove_employee(self, emp_id):
        for employee in self.employees:
            if employee.emp_id == emp_id:
                self.employees.remove(employee)
                break
        else:
            print(f"Error: Employee with ID '{emp_id}' not found in department '{self.name}'.")

    def list_employees(self):
        return [str(employee) for employee in self.employees]


class EmployeeManagementSystem:
    def __init__(self):
        self.company = {}

    def add_department(self, department):
        if isinstance(department, Department):
            self.company[department.name] = department
        else:
            print("Error: Invalid department object.")

    def remove_department(self, department_name):
        if department_name in self.company:
            del self.company[department_name]
        else:
            print(f"Error: Department '{department_name}' not found.")

    def display_departments(self):
        return list(self.company.keys())
    
    def save_data(self, filename="company_data.json"):
        with open(filename, "w") as file:
            data = {
                "departments": {
                    department.name: [vars(employee) for employee in department.employees]
                    for department in self.company.values()
                }
            }
            json.dump(data, file)

    def load_data(self, filename="company_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for department_name, employees_data in data.get("departments", {}).items():
                    department = Department(department_name)
                    for employee_data in employees_data:
                        employee = Employee(**employee_data)
                        department.add_employee(employee)
                    self.add_department(department)
        except FileNotFoundError:
            print("No saved data found.")


def print_menu():
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. Display Departments")
    print("4. Exit")


def main():
    system = EmployeeManagementSystem()

    system.load_data()

    if not system.company:
        default_department = Department("Default")
        system.add_department(default_department)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter employee name: ")
            emp_id = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter employee department: ")

            employee = Employee(name, emp_id, title, department)

            department_object = system.company.get(department)
            if department_object:
                department_object.add_employee(employee)
            else:
                print(f"Error: Department '{department}' not found.")

        elif choice == "2":
            emp_id = input("Enter employee ID to remove: ")
            for department in system.company.values():
                department.remove_employee(emp_id)

        elif choice == "3":
            print("Departments:", system.display_departments())

        elif choice == "4":
            system.save_data()
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
