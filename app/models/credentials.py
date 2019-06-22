import json

"""
 I wish to  avoid O(N) iteration in a large user base

 user_id_mapping[0] should return "larry". Time complexity -> O(1)
 
 username_mapping['larry'] should  return "larry". Time complexity -> O(1)
 
 2 different dictionaries because, separation of information

 my approach will improve time complexity at the cost of space complexity

 reference: https://wiki.python.org/moin/TimeComplexity"
 
"""


class Credentials:

    def __init__(self, filename):

        self.users = []

        self.username_mapping = {}

        self.user_id_mapping = {}

        self.update_credentials(filename=filename, user=None, mode='get')

    def update_credentials(self, filename, user, mode):

        # TODO implement error handling

        # Edge case:  error if file is empty

        # Base case: file is empty and contains: []

        if mode == 'add':

            # to write to disk: first write to memory, then dump to disk

            self.users.append(user)

            credentials_file = open(filename, 'w')

            json.dump(self.users, credentials_file, indent=4)

            credentials_file.close()

        elif mode == 'get':

            # to write to memory: first read from disk

            credentials_file = open(filename, 'r')

            self.users = json.load(credentials_file)

            credentials_file.close()

        elif mode == 'delete':

            # to delete on disk : first delete in memory, then dump to disk

            self.users = [i for i in self.users if i['user_name'] != user['user_name']]

            db_file = open(filename, 'w')

            json.dump(self.users, db_file, indent=4)

            db_file.close()

        elif mode == 'update':

            # to update on disk : first delete in memory, then dump to disk

            self.users = [i for i in self.users if i['user_name'] != user['user_name']]

            self.update_credentials(filename, user, 'add')

        # create a dict == {'unique_username_string': employee_object} using set comprehension

        self.username_mapping = {user['user_name']: user for user in self.users}

        # create a dict == {unique_id_integer: employee_object} using set comprehension

        self.user_id_mapping = {user['user_id']: user for user in self.users}

    def find_by_username(self, user_name):

        # return the first match, else None

        return self.username_mapping.get(user_name, None)

    def find_by_userid(self, user_id):

        # return the first match, else None

        return self.user_id_mapping.get(user_id, None)
