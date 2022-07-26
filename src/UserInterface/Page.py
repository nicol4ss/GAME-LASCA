from tkinter import *
from src.Jogador import Jogador
from src.Posicao import Posicao
from src.Tabuleiro import Tabuleiro
from src.Modules.cor import iluminar_escurecer_cor
from src.Oficial import Oficial


class StartPage(Frame):

    def __init__(self, controller, parent):
        Frame.__init__(self, parent)

        self.__controller = controller
        self.configure(bg=self.__controller.BG_COLOR)
        
        Label(self,
                text="LASCA",
                bg=self.__controller.BG_COLOR,
                fg=self.__controller.FG_COLOR,
                font= self.__controller.font_title
            ).place(x=795, y=145)

        Label(self,
                text="Criadores:\n\n\nAnthon Gretter\n\nNicolas Elias\n\nRian Serena",
                bg=self.__controller.BG_COLOR, fg=self.__controller.FG_COLOR,
                font= self.__controller.font_info
            ).place(x=775, y=295)

        Button(self,
                width=18, height=2,
                text="JOGAR",
                command=lambda: self.__controller.criar_game(),
                bg=self.__controller.BG_COLOR, fg=self.__controller.FG_COLOR,
                font= self.__controller.font_button
            ).place(x=90, y=310)

        Button(self,
                width=18, height=2,
                text="SAIR",
                command=controller.destroy,
                bg=self.__controller.BG_COLOR,
                fg=self.__controller.FG_COLOR,
                font= self.__controller.font_button
            ).place(x=90, y=410)


class GamePage(Frame):

    def __init__(self, controller, parent):
        Frame.__init__(self, parent)
        
        self.__controller = controller
        self.configure(bg=self.__controller.BG_COLOR)

        # canvas (desenho do tabuleiro e inteface tabuleiro)
        self.__canvas = Canvas(self, width=841, height=841, bg="#000000")
        self.__canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self,
                text="LASCA",
                bg=self.__controller.BG_COLOR,
                fg=self.__controller.FG_COLOR,
                font= self.__controller.font_medium
            ).place(x=18, y=465) 
        
        Button(self,
                width=8, height=2,
                text="DESISTIR",
                command=lambda: self.__tab.desistir(),
                bg=self.__controller.BG_COLOR,
                fg=self.__controller.FG_COLOR,
                font= self.__controller.font_mim
            ).place(x=1075, y=455)

        # Label de notificações de avisos
        self.__notificar_avisos_label = Label(
                                                self,
                                                text="",
                                                bg=self.__controller.BG_COLOR,
                                                fg=self.__controller.AVISO_COLOR,
                                                font= self.__controller.font_info
                                            )
        # Label de troca de turno
        self.__notificar_troca_turno_label = Label(
                                                    self,
                                                    text="",
                                                    bg=self.__controller.BG_COLOR,
                                                    fg=self.__controller.BG_COLOR,
                                                    font= self.__controller.font_info
                                                )

        self.__notificar_avisos_label.pack(side="bottom", pady=15)
        self.__notificar_troca_turno_label.pack(pady=15)

        self.__tab = Tabuleiro(controller, self)
        self.__tab.nova_partida()

    @property
    def canvas(self):
        return self.__canvas

    def notificar_erro(self, mensagem, posicao_errada):
        self.__notificar_avisos_label['text'] = mensagem
        self.piscar_posicao(posicao_errada)

    def notificar_troca_turno(self, jogador: Jogador):
        text = ("TURNO TROCADO, VEZ DO " + jogador.cor_pecas.upper())
        self.__notificar_troca_turno_label['text'] = text
        self.__notificar_troca_turno_label['fg'] = jogador.cor_pecas


    def piscar_posicao(self, posicao: Posicao):

        def piscar(contador_peridodo=4, trocar_cor=True):
            if not contador_peridodo:
                self.__canvas.itemconfig(
                    f"{posicao.coordenadas[0]}x{posicao.coordenadas[1]}",
                    fill=posicao.cor, activefill=iluminar_escurecer_cor(posicao.cor))
                return
            else:
                cor = posicao.cor
                if trocar_cor: cor = 'red'
                
                self.__canvas.itemconfig(f"{posicao.coordenadas[0]},{posicao.coordenadas[1]}", fill=cor, activefill=cor)
                self.__canvas.after(250, piscar, contador_peridodo-1, not trocar_cor)

        piscar()
    

    def atualizar_desenho(self, matriz: list):
        self.__canvas.delete("torre")

        for i in range(len(matriz)):
            for j in range(len(matriz)):
                pos = matriz[i][j]

                if pos.ocupada():
                    torre = pos.ocupante()
                    pos_coords = self.__canvas.coords(self.__canvas.find_withtag(f"{pos.coordenadas[0]},{pos.coordenadas[1]}"))

                    offset_pilha = 10
                    for peca in torre.pilha:
                        self.__canvas.create_oval(
                            pos_coords[0]+15, pos_coords[1]-offset_pilha+70,
                            pos_coords[2]-10, pos_coords[3]-offset_pilha,
                            fill=peca.cor, width=2, tags="torre"
                        )
                        offset_pilha += 10
                        if peca == torre.topo():
                            self.__canvas.create_oval(
                                pos_coords[0]+15, pos_coords[1]-offset_pilha+70,
                                pos_coords[2]-10, pos_coords[3]-offset_pilha,
                                fill=peca.cor, width=2, tags="torre"
                            )
                            offset_pilha += 10
                        if isinstance(peca, Oficial):
                            self.__canvas.create_rectangle(
                                pos_coords[0]+35, pos_coords[1]-offset_pilha+100,
                                pos_coords[2]-30, pos_coords[3]-offset_pilha-10,
                                fill='black', width=2, tags="torre"
                            )


    def destacar_posicoes(self, posicoes: list, cor: str):
        for posicao in posicoes:
            self.__canvas.itemconfig(f"{posicao.coordenadas[0]},{posicao.coordenadas[1]}", fill=cor, activefill=cor)


    def limpar_avisos(self):
        self.__notificar_avisos_label['text'] = ""


    def limpar_destaques(self, matriz: list):
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                posicao = matriz[i][j]

                self.__canvas.itemconfig(
                    f"{posicao.coordenadas[0]},{posicao.coordenadas[1]}",
                    fill=posicao.cor, activefill=iluminar_escurecer_cor(posicao.cor)
                )
        

class WinPage(Frame):
    
    def __init__(self, controller, parent):
        Frame.__init__(self, parent)
        
        self.__controller = controller
        self.configure(bg=self.__controller.BG_COLOR)
        
        Label(
            self, text="FIM DE JOGO!\nVENCEDOR:",
            bg=self.__controller.BG_COLOR, fg=self.__controller.FG_COLOR,
            font= self.__controller.font_title
        ).place(x=380, y=185)

        Button(
            self, width=45, height=2,
            text="CLIQUE AQUI PARA CONTINUAR",
            command=lambda: self.__controller.mostrar_frame("StartPage"),
            bg=self.__controller.BG_COLOR, fg=self.__controller.FG_COLOR,
            font= self.__controller.font_info
        ).place(x=95, y=745)


class WinRed(WinPage):

    def __init__(self, controller, parent):
        super().__init__(controller, parent)

        self.__controller = controller

        Label(
            self, text="VERMELHO",
            bg=self.__controller.BG_COLOR,
            fg="red", font= self.__controller.font_title
        ).place(x=435, y=420)


class WinBlue(WinPage):

     def __init__(self, controller, parent):
        super().__init__(controller, parent)

        self.__controller = controller

        Label(
            self, text="AZUL",
            bg=self.__controller.BG_COLOR,
            fg="blue", font= self.__controller.font_title
        ).place(x=555, y=420)
