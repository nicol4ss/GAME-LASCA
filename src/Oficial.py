from src.Peca import Peca

class Oficial(Peca):

    def __init__(self, cor, dono):
        super().__init__(cor, dono)

        self.__cor = cor
        self.__dono = dono

    @property
    def dono(self):
        return self.__dono

    @property
    def cor(self):
        return self.__cor

    def padrao_movimento(self):
        return "oficial"