from abc import ABC, abstractmethod

class DatabaseStrategy(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, query):
        pass

    @abstractmethod
    def update(self, query, update):
        pass

    @abstractmethod
    def delete(self, query):
        pass
