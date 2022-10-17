import json
class Request:
    def __init__(self):
        self._from = None
        self._to = None
        self.description = None
        self.action = None
        self.timestamp = None
        self.amount = None
    
    def fetch_pending_requests(self, path):
        with open(path, 'r') as file_in:
            data = json.load(file_in)
        return data

    def save_pending_transactions(self, data, path):
        with open(path, 'w') as file:
            file.write(json.dumps(data, indent=4))
    
    def append_file(self, entry, path):
        data = self.fetch_pending_requests(path)
        with open(path, 'w') as file:
            data.insert(0, entry)
            file.write(json.dumps(data, indent=4))  