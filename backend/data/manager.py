# data/manager.py
from abc import ABC, abstractmethod

class Manager(ABC):
    @abstractmethod
    def get_data(self, source: str):
        pass

    @abstractmethod
    def add_data(self, source: str, data: dict):
        pass
