from src.Modules.cor import *

class Posicao:
    def __init__(self, cor: str, coordenadas: tuple):
        self.__coordenadas = coordenadas
        self.__ocupante = None
        self.__cor = cor

    @property
    def cor(self):
        return self.__cor

    @property
    def coordenadas(self):
        return self.__coordenadas

    @cor.setter
    def cor(self, cor: str):
        self.__cor = cor

    def ocupar(self, torre):
        self.__ocupante = torre
        self.__ocupante.posicao = self

    def desocupar(self):
        self.__ocupante.posicao = None
        self.__ocupante = None

    def ocupada(self):
        return self.__ocupante != None
    
    def ocupante(self):
        return self.__ocupante
