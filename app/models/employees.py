import json


class Employees:

    def __init__(self, filename):

        self.employees = []

        self.update_employees(filename=filename, employee=None, mode='get')

    def get_employees(self):

        # return a list of all employee information

        return self.employees

    def size(self):

        # returns the number of employees in the registry

        return len(self.employees)

    def update_employees(self, filename, employee, mode):

        # TODO implement error handling

        # Edge case:  error if file is empty

        # Base case: file is empty and contains: []

        if mode == 'add':

            # to write to disk: first write to memory, then dump to disk

            self.employees.append(employee)

            db_file = open(filename, 'w')

            json.dump(self.employees, db_file, indent=4)

            db_file.close()

        elif mode == 'get':

            # to write to memory: first read from disk

            db_file = open(filename, 'r')

            self.employees = json.load(db_file)

            db_file.close()

        elif mode == 'delete':

            # to delete on disk : first delete in memory, then dump to disk

            self.employees = [i for i in self.employees if i['user_name'] != employee['user_name']]

            db_file = open(filename, 'w')

            json.dump(self.employees, db_file, indent=4)

            db_file.close()

        elif mode == 'update':

            # to update on disk : first delete in memory, then dump to disk

            self.employees = [i for i in self.employees if i['user_name'] != employee['user_name']]

            self.update_employees(filename, employee, 'add')

    def find_by_username(self, user_name):

        # return the first match, else None

        return next(filter(lambda user: user['user_name'] == user_name, self.employees), None)
