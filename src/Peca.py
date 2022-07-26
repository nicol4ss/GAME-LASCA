from abc import *

class Peca(ABC):

    def __init__(self, cor: str, dono):
        self.__cor = cor
        self.__dono = dono

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

    @property
    def dono(self):
        return self.__dono

    @property
    def cor(self):
        return self.__cor

    @abstractmethod
    def padrao_movimento(self):
        pass
