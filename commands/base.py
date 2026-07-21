from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, params):
        pass
