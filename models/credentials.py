import json


# I wish to  avoid O(N) iteration in a large user base
# user_id_mapping[1] should return "larry"
# username_mapping['larry'] should  return larry

class Credentials:
    def __init__(self, filename):
        self.users = []
        self.username_mapping = {}
        self.user_id_mapping = {}
        self.update_credentials(filename, None, 'get')

    def update_credentials(self, filename, new_user, mode):
        # TODO implement error handling
        # Edge case:  error if file is empty
        # Base case: file is empty and contains: []

        if mode == 'add':
            self.users.append(new_user)

            credentials_file = open(filename, 'w')
            json.dump(self.users, credentials_file, indent=4)
            credentials_file.close()

        elif mode == 'get':

            credentials_file = open(filename, 'r')
            self.users = json.load(credentials_file)
            credentials_file.close()

        elif mode == 'delete':

            self.users = [i for i in self.users if i['user_name'] != new_user['user_name']]

            db_file = open(filename, 'w')

            json.dump(self.users, db_file, indent=4)

            db_file.close()

        elif mode == 'update':

            self.users = [i for i in self.users if i['user_name'] != new_user['user_name']]

            self.update_credentials(filename, new_user, 'add')


        # set comprehension for mapping username to user object
        self.username_mapping = {user['user_name']: user for user in self.users}

        # set comprehension for mapping user_id to user object
        self.user_id_mapping = {user['user_id']: user for user in self.users}

        print(self.users)

    def find_by_username(self, user_name):
        # return the first match, else None
        return self.username_mapping.get(user_name, None)

    def find_by_userid(self, user_id):
        # return the first match, else None
        return self.user_id_mapping.get(user_id, None)
