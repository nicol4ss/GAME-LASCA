from src.Soldado import Soldado
from src.Jogador import Jogador
from src.Modules.cor import iluminar_escurecer_cor
from src.Posicao import Posicao
from src.Torre import Torre
from src.Oficial import Oficial
from functools import partial


class Tabuleiro:
    def __init__(self, gerenciador_telas, game_page) -> None:
        self.__CORES = ["#212738", "#F0EDEE"]
        self.__TAMANHO_POSICAO = 120
        self.__DIMENSAO = 7

        self.__matriz = []
        self.__jogadores = []
        self.__turno = None

        self.__jogada_em_andamento = False
        self.__ultima_posicao_selecionada = None

        self.__gerenciador_telas = gerenciador_telas
        self.__game_page = game_page


    def turno(self):
        return self.__turno

    def troca_turno(self):
        self.__turno = self.__jogadores[0] if self.turno() == self.__jogadores[1] else self.__jogadores[1] 
        self.__game_page.notificar_troca_turno(self.__turno)

    def __switch_jogada_em_andamento(self):
        self.__jogada_em_andamento = not self.__jogada_em_andamento

    def jogada_em_andamento(self):
        return self.__jogada_em_andamento

    def get_posicao(self, i: int, j: int):
        return self.__matriz[i][j]


    def nova_partida(self):
        for cor in ["red", "blue"]:
            self.__jogadores.append(Jogador(cor))
        self.__gerar_posicoes()
        self.troca_turno()


    def __gerar_posicoes(self) -> None:
        torres_ja_postas = [0, 0]

        for i in range(self.__DIMENSAO):
            linha = []
            for j in range(self.__DIMENSAO):
                cor_posicao = self.__CORES[(j+i) % len(self.__CORES)]                      # alterna entre as cores
                x1, y1 = (self.__TAMANHO_POSICAO*j) + 2, (self.__TAMANHO_POSICAO*i) + 2    # calcula posicao inicial da posicao
                x2, y2 = x1 + self.__TAMANHO_POSICAO, y1 + self.__TAMANHO_POSICAO          # calcula posicao final da posicao

                # cria quadrado da posicao na ui (canvas)
                self.__game_page.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=cor_posicao,
                    activefill=iluminar_escurecer_cor(cor_posicao),
                    tags=[f"{i},{j}", 'posicao']                          # tag usada posteriormente para identificar retangulos da interface (canvas)
                )

                # mapeia seleção das posicoes para o selecionar_posicao
                self.__game_page.canvas.tag_bind(f"{i},{j}", '<Button-1>', partial(self.selecionar_posicao, (i, j)))
                pos = Posicao(cor_posicao, (i, j))

                if (i in [0, 2] and j % 2 == 0) or (i == 1 and j % 2 != 0):
                    pos.ocupar(self.__jogadores[0].torres()[torres_ja_postas[0]])
                    torres_ja_postas[0] += 1

                elif (i in [4, 6] and j % 2 == 0) or (i == 5 and j % 2 != 0):
                    pos.ocupar(self.__jogadores[1].torres()[torres_ja_postas[1]])
                    torres_ja_postas[1] += 1

                linha.append(pos)
            self.__matriz.append(linha)

        self.__game_page.atualizar_desenho(self.__matriz)


    def selecionar_posicao(self, coordenadas: tuple, *args):
        self.__game_page.limpar_avisos()
        self.__game_page.limpar_destaques(self.__matriz)
        posicao_selecionada = self.get_posicao(coordenadas[0], coordenadas[1])

        if self.jogada_em_andamento():
            self.__avaliar_jogada(posicao_selecionada)
        else:
            self.__iniciar_jogada(posicao_selecionada)


    def __iniciar_jogada(self, origem: Posicao):
        if origem.ocupada():
            torre = origem.ocupante()

            if self.turno() == torre.controlador():
                captura = self.pode_capturar(torre)
                posicoes = []

                if not captura:
                    for torre_no_controle in self.turno().torres():
                        if self.pode_capturar(torre_no_controle) and torre != torre_no_controle:
                            self.__game_page.notificar_erro("VOCE TEM UMA OU MAIS CAPTURAS PARA FAZER", origem)
                            return

                if captura:                     posicoes = self.capturas_possiveis(torre)[0]
                elif self.pode_mover(torre):    posicoes = self.movimentacoes_possiveis(torre)
                else:
                    # notificar torre sem movimentos 
                    self.__game_page.notificar_erro("TORRE SEM MOVIMENTOS", origem)
                    return
                
                # destacar posicoes
                self.__ultima_posicao_selecionada = origem
                self.__game_page.destacar_posicoes(posicoes, "yellow")
                self.__game_page.destacar_posicoes([origem], "green")
                self.__switch_jogada_em_andamento()

            else:
                # notificar torre do oponente
                self.__game_page.notificar_erro("TORRE DO OPONENTE", origem)
        else:
            # notificar posicao vazia e piscar ela
            self.__game_page.notificar_erro("POSIÇÃO VAZIA", origem)


    def __avaliar_jogada(self, destino: Posicao):
        self.__switch_jogada_em_andamento()
        torre_movendo = self.__ultima_posicao_selecionada.ocupante()
        capturas = self.capturas_possiveis(torre_movendo)
        
        if self.destino_valido(torre_movendo, destino):
            # salvando contexto antes de mover
            podia_capturar = self.pode_capturar(torre_movendo) 

            torre_movendo.mover(destino)

            if self.na_borda(torre_movendo):
                if not isinstance(torre_movendo.topo(), Oficial):
                    torre_movendo.promover_topo()

            if podia_capturar:
                torre_vitima = capturas[1][capturas[0].index(destino)].ocupante()
                torre_movendo.capturar(torre_vitima)

            self.troca_turno()
            self.__game_page.atualizar_desenho(self.__matriz)
            self.verificar_partida()

        else:
            # notificar destino invalido
            self.__game_page.notificar_erro("DESTINO INVALIDO", destino)


    def destino_valido(self, torre: Torre, destino: Posicao) -> bool:
        destinos_validos = self.capturas_possiveis(torre)[0] if self.pode_capturar(torre) else self.movimentacoes_possiveis(torre)
        return destino in destinos_validos


    def verificar_partida(self):
        for jogador in self.__jogadores:
            pode_jogar = False

            if jogador.ha_torres():
                for torre in jogador.torres():
                    if self.pode_mover(torre) or self.pode_capturar(torre):
                        pode_jogar = True
                        break

            if not pode_jogar:
                for possivel_ganhador in self.__jogadores:
                    if possivel_ganhador != jogador:
                        self.decretar_vencedor(jogador)
                        break

    
    def movimentacoes_possiveis(self, torre: Torre):
        movimentos = []
        sinal_linha = 0
        sinal_coluna = 0
        
        if torre.topo().cor == "red":
            sinal_linha = 2
        else:
            sinal_linha = 0

        padrao_movimento = torre.topo().padrao_movimento()

        linha = torre.posicao.coordenadas[0]
        coluna = torre.posicao.coordenadas[1]
        if padrao_movimento == "soldado":
            for i in range(2):

                # Primeiro passa i == 0 ele faz coluna + 1
                # Segundo passa i != 0 ele faz coluna - 1  
                if i != 0:
                    sinal_coluna = 2

                # Para colunas e linhas negativas descartar e maiores que 7
                if coluna + (1 - sinal_coluna) > -1 and (linha + sinal_linha) - 1 > -1 and coluna + (1 - sinal_coluna) < 7 and (linha + sinal_linha) - 1 < 7: 

                    pos_possivel = self.__matriz[linha - (1 - sinal_linha)][coluna + (1 - sinal_coluna)]
                    if not pos_possivel.ocupada():
                        movimentos.append(pos_possivel)

        else:
            #Oficial
            sinal_linha = 0
            for i in range(4):
                # Linha começa em - 1 apos 2 iterações muda para + 1
                if i == 2:
                    sinal_linha = 2

                # Alterna sinal da coluna entre - e +
                if sinal_coluna == 0:
                    sinal_coluna = 2
                else:
                    sinal_coluna = 0
                
                # Para colunas e linhas negativas e maiores que 6 descartar
                if coluna + (1 - sinal_coluna) > -1 and (linha + sinal_linha) - 1 > -1 and coluna + (1 - sinal_coluna) < 7 and (linha + sinal_linha) - 1 < 7:  
                    pos_possivel = self.__matriz[(linha + sinal_linha) - 1][coluna + (1 - sinal_coluna)]
                    #                               3 + 0  -  1 = 2
                    #                               3 + 2  -  1 = 4

                    if not pos_possivel.ocupada():
                        movimentos.append(pos_possivel)
        
        return movimentos


    def capturas_possiveis(self, torre):
        movimentos_captura = []
        posicoes_vitima = []
        sinal_linha = 0
        sinal_coluna = 0

        padrao_movimento = torre.topo().padrao_movimento()

        if torre.topo().cor == "red":
            sinal_linha = 2
        else:
            sinal_linha = 0

        linha = torre.posicao.coordenadas[0]
        coluna = torre.posicao.coordenadas[1]
        if padrao_movimento == "soldado":
            for i in range(2):

                # Primeiro passa i == 0 ele faz coluna + 1
                # Segundo passa i != 0 ele faz coluna - 1  
                if i != 0:
                    sinal_coluna = 2

                # Para colunas e linhas negativas descartar
                if coluna + (1 - sinal_coluna) > -1 and (linha + sinal_linha) - 1 > -1 and coluna + (1 - sinal_coluna) < 7 and (linha + sinal_linha) - 1 < 7:
                    pos_vitima = self.__matriz[linha - (1 - sinal_linha)][coluna + (1 - sinal_coluna)]
                    
                    # Pos ocupada e torre inimiga
                    if pos_vitima.ocupada() and pos_vitima.ocupante().controlador() != torre.controlador():

                        #Pos seguinte em diagonal 2 pos pra cima e para os lados
                        # Logica de pegar posicao acima da vitima em todos os casos
                        if (pos_vitima.coordenadas[0] + sinal_linha) - 1 > -1 and (pos_vitima.coordenadas[0] + sinal_linha) - 1 < 7 and pos_vitima.coordenadas[1] + (1 - sinal_coluna) > -1 and pos_vitima.coordenadas[1] + (1 - sinal_coluna) < 7:
                            pos_captura = self.__matriz[(pos_vitima.coordenadas[0] + sinal_linha) - 1][pos_vitima.coordenadas[1] + (1 - sinal_coluna)]
                        
                            if not pos_captura.ocupada():
                                movimentos_captura.append(pos_captura)
                                posicoes_vitima.append(pos_vitima)
        
        else:
            #Oficial
            sinal_linha = 0
            for i in range(4):
                # Linha começa em - 1 apos 2 iterações muda para + 1
                if i == 2:
                    sinal_linha = 2

                # Alterna sinal da coluna entre - e +
                if sinal_coluna == 0:
                    sinal_coluna = 2
                else:
                    sinal_coluna = 0
                
                # Para colunas e linhas negativas descartar
                if coluna + (1 - sinal_coluna) > -1 and (linha + sinal_linha) - 1 > -1 and coluna + (1 - sinal_coluna) < 7 and (linha + sinal_linha) - 1 < 7: 
                    # pega posicao nas diagonais
                    pos_vitima = self.__matriz[(linha + sinal_linha) - 1][coluna + (1 - sinal_coluna)]
                    # verifica se ta ocupada e se o controlador é diferente
                    if pos_vitima.ocupada() and pos_vitima.ocupante().controlador() != torre.controlador():
                        #pego a diagonal + 1 em todas as direcoes controladas pelo for
                        if (pos_vitima.coordenadas[0] + sinal_linha) - 1 > -1 and (pos_vitima.coordenadas[0] + sinal_linha) - 1 < 7 and pos_vitima.coordenadas[1] + (1 - sinal_coluna) > -1 and pos_vitima.coordenadas[1] + (1 - sinal_coluna) < 7:
                            pos_captura = self.__matriz[(pos_vitima.coordenadas[0] + sinal_linha) - 1][pos_vitima.coordenadas[1] + (1 - sinal_coluna)]
                            # vejo se n tem ninguem nela
                            if not pos_captura.ocupada():
                                # isso é caracterizado um movimento de captura
                                movimentos_captura.append(pos_captura)
                                posicoes_vitima.append(pos_vitima)
        
        return movimentos_captura, posicoes_vitima


    def pode_mover(self, torre: Torre):
        return len(self.movimentacoes_possiveis(torre)) > 0

    def pode_capturar(self, torre: Torre):
        return len(self.capturas_possiveis(torre)[0]) > 0

    def na_borda(self, torre: Torre):
        return ((self.turno() == self.__jogadores[1] and torre.posicao in self.__matriz[0]) or
                (self.turno() == self.__jogadores[0] and torre.posicao in self.__matriz[6]))
    
    def decretar_vencedor(self, jogador: Jogador):
        tela_a_mostrar = "WinRed" if jogador == self.__jogadores[1] else "WinBlue"
        self.__gerenciador_telas.mostrar_frame(tela_a_mostrar)
        self.encerrar_partida()

    def encerrar_partida(self):
        self.__game_page.canvas.delete("all")
        self.__game_page.limpar_avisos()

        self.__matriz = []
        for jogador in self.__jogadores:
            for torre in jogador.torres():
                jogador.descontrolar(torre)

        self.__jogadores = []
        self.__turno = None
        self.__jogada_em_andamento = False
        self.__ultima_posicao_selecionada = None
        self.nova_partida()

    # mudar logica (errada)
    def desistir(self):
        self.decretar_vencedor(self.turno())
