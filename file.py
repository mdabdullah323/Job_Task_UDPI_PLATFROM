import json


class File:
    def __init__(self, path):
        self.data = []
        self.path = path

    def read(self):
        with open(self.path, "r") as file:
            data = file.read()
            if len(data) > 0 and data[0] == "[":
                self.data = json.loads(data)
        return self.data

    def save(self, data=None):
        if data is None:
            data = []
        with open(self.path, "w", ) as file:
            if len(data) > 0:
                self.data = data
                file.write(json.dumps(self.data))
        return self.data
