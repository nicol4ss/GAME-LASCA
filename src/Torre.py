from src.Peca import Peca
from src.Soldado import Soldado
from src.Posicao import Posicao


class Torre:

    def __init__(self, cor, dono):
        self.__tamanho = 1
        self.__posicao = None
        self.__pilha = [Soldado(cor, dono)]

    @property
    def pilha(self):
        return self.__pilha

    @property
    def posicao(self):
        return self.__posicao

    @posicao.setter
    def posicao(self, posicao):
        self.__posicao = posicao


    def topo(self):
        return self.__pilha[-1]

    def promover_topo(self):
        a_promover = self.pilha.pop(-1)
        self.__pilha.append(a_promover.promover())

    def empilhar(self, peca: Peca):
        self.__tamanho += 1
        self.__pilha.append(peca)

    def desempilhar(self) -> Peca:
        self.__tamanho -= 1
        if self.__tamanho == 0:
            self.controlador().descontrolar(self)
            self.__posicao.desocupar()
            
        return self.__pilha.pop(-1)

    def vazia(self):
        return self.__tamanho == 0

    def controlador(self):
        return self.topo().dono

    def mover(self, posicao: Posicao):
        self.__posicao.desocupar()
        posicao.ocupar(self)

    def capturar(self, vitima):
        antigo_dono_vitima = vitima.controlador()

        topo_vitima = vitima.desempilhar()
        self.__pilha.insert(0, topo_vitima)
        self.__tamanho += 1

        if not vitima.vazia():
            novo_dono_vitima = vitima.controlador() 

            if novo_dono_vitima != antigo_dono_vitima:
                antigo_dono_vitima.descontrolar(vitima)
                novo_dono_vitima.controlar(vitima)
