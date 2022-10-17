import json

class User:
    def __init__(self):
        self.profile = None
        self.username = None
        self.status = "ACTIVE"
        self.password = None
        self.last_spent = None
        self.allow_multi_spend = "false"
        self.credit_limit = "50"
        self.allow_overspend = "false"
        self.account_number = ""
    
    def check_credentials(self, username, password, file_path):
        with open(file_path, 'r') as file_in:
            list = json.load(file_in)
            for user in list:
                if user['username'] is not None and user['username'].lower() == username.lower() and user['password'] is not None and user['password'] == password:
                    print("Authorized")
                    return user
            return None

    def read_file(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def append_file(self, entry, path):
        data = self.read_file(path)
        with open(path, 'w') as file:
            data.insert(0, entry)
            file.write(json.dumps(data, indent=4))

    def update_profiles(self, list, path):
        with open(path, 'w') as file:
            file.write(json.dumps(list, indent=4))  
         