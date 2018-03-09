import json

class ConfigManager:
    def __init__(self, strFileName):
        self.config = {}
        with open(strFileName, 'r') as f:
            self.config = json.load(f)

    def get(self, strKey):
        return self.config.get(strKey)