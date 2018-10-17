import json


class Employees:
    def __init__(self, filename):
        self.employees = []
        self.update_employees(filename, None, 'get')

    def get_employees(self):
        return self.employees

    def size(self):
        return len(self.employees)

    def update_employees(self, filename, employee, mode):
        # TODO implement error handling
        # Edge case:  error if file is empty
        # Base case: file is empty and contains: []

        if mode == 'add':
            self.employees.append(employee)

            db_file = open(filename, 'w')
            json.dump(self.employees, db_file, indent=4)
            db_file.close()

        elif mode == 'get':

            db_file = open(filename, 'r')
            self.employees = json.load(db_file)
            db_file.close()

        elif mode == 'delete':
            self.employees = [i for i in self.employees if i['user_name'] != employee['user_name']]

            db_file = open(filename, 'w')
            json.dump(self.employees, db_file, indent=4)
            db_file.close()

        elif mode == 'update':
            self.employees = [i for i in self.employees if i['user_name'] != employee['user_name']]
            self.update_employees(filename, employee, 'add')


        # print(self.employees)

    def find_by_username(self, user_name):
        # return the first match, else None
        return next(filter(lambda user: user['user_name'] == user_name, self.employees), None)
