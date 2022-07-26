from src.Torre import Torre


class Jogador:

    def __init__(self, cor_pecas: str):
        self.__cor_pecas = cor_pecas
        self.__torres_controlando = []

        for i in range(11):
            self.__torres_controlando.append(Torre(cor_pecas, self))

    def __eq__(self, other) :
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            # quando other é nonetype
            return False

    @property
    def cor_pecas(self):
        return self.__cor_pecas

    def torres(self): # return list de torres
        return self.__torres_controlando

    def controlar(self, torre: Torre):
        self.__torres_controlando.append(torre)

    def descontrolar(self, torre: Torre):
        self.__torres_controlando.remove(torre)

    def ha_torres(self):
        return (len(self.__torres_controlando) > 0)
