import json
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, vacancy):
        pass

    @abstractmethod
    def delete(self, vacancy):
        pass

    @abstractmethod
    def load(self):
        pass


class JSONStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def add(self, vacancy):
        pass

    def delete(self, vacancy):
        pass
