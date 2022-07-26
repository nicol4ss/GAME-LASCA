from src.Peca import Peca
from src.Oficial import Oficial

class Soldado(Peca):
    
    def __init__(self, cor, dono):
        super().__init__(cor, dono)

        self.__cor = cor
        self.__dono = dono

    def promover(self):
        return Oficial(self.__cor, self.__dono)

    @property
    def dono(self):
        return self.__dono

    @property
    def cor(self):
        return self.__cor
    
    def padrao_movimento(self):
        return "soldado"