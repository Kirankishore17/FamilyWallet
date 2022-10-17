import json
class Transaction:
    def __init__(self):
        self.user = None
        self.description = None
        self.amount = None
        self.timestamp = None
        self.current_balance = 0
        
    def read_file(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def append_file(self, entry, path):
        data = self.read_file(path)
        with open(path, 'w') as file:
            data.insert(0, entry)
            file.write(json.dumps(data, indent=4))

    def fetch_current_balance(self, path):
        data = self.read_file(path)
        self.current_balance = data[0].get('current_balance') if len(data) > 0 else 0
        return self.current_balance
    
    def update_transaction(self, username, amount, date, description, path):
        entry = {}
        entry['user'] = username.upper()
        entry['timestamp'] = str(date)
        entry['current_balance'] = self.fetch_current_balance(path) + amount
        entry['description'] = description
        entry['amount'] = amount
        self.append_file(entry, path)