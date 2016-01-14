from abc import abstractmethod, abstractproperty


class Field:
    @abstractmethod
    def set(self):
        raise NotImplementedError("should have implemented this")

    @abstractproperty
    def get(self):
        raise NotImplementedError("should have implemented this")

    def __str__(self):
        return str(self.get())