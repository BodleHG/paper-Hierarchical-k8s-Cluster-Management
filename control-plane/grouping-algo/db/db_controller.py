from .mysql_strategy import MySQLStrategy
from .mongo_strategy import MongoStrategy

class DatabaseController:
    def __init__(self, kind):
        self.kind = kind.lower()
        if self.kind == "mysql":
            self.strategy = MySQLStrategy()
        elif self.kind == "mongo":
            self.strategy = MongoStrategy()
        else:
            raise ValueError(f"Unsupported kind: {kind}")

    def create(self, data):
        return self.strategy.create(data)

    def read(self, query):
        return self.strategy.read(query)

    def update(self, query, update):
        return self.strategy.update(query, update)

    def delete(self, query):
        return self.strategy.delete(query)
