from abc import ABC, abstractmethod

class LoxCallable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call_(self, interpreter, arguments):
        pass

    @abstractmethod
    def __str__(self):
        pass