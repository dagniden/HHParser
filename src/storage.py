from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add