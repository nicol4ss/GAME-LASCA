from tkinter import *
from tkinter.font import Font
from src.UserInterface.Page import WinBlue, WinRed, GamePage, StartPage


class GerenciadorDeTelas(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # tkinter window settings
        self.title("Lasca")
        self.geometry("1290x1000+300+0")
        self.resizable(False, False)
        self.BG_COLOR = "#212121"
        self.FG_COLOR = "white"
        self.AVISO_COLOR = "yellow"

        self.__font_style   = "Arial Black"
        self.__font_weight  = "bold"

        # fontes para as telas
        self.font_title     =  Font(font=(self.__font_style, 54, self.__font_weight))
        self.font_info      =  Font(font=(self.__font_style, 26, self.__font_weight))
        self.font_button    =  Font(font=(self.__font_style, 22, self.__font_weight))
        self.font_mim       =  Font(font=(self.__font_style, 24, self.__font_weight))
        self.font_medium    =  Font(font=(self.__font_style, 38, self.__font_weight))

        self.__container = Frame(self)
        self.__container.pack(side="top", fill="both", expand=True)
        self.__container.grid_rowconfigure(0, weight=1)
        self.__container.grid_columnconfigure(0, weight=1)
        
        self.__frames = {}
        
        for F in (StartPage, WinRed, WinBlue):
            page_name = F.__name__
            frame = F(controller=self, parent=self.__container)
            self.__frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("StartPage")

    def criar_game(self):
        frame = GamePage(controller=self, parent=self.__container)
        self.__frames["GamePage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.mostrar_frame("GamePage")
    
    # exibe a janela solicitada
    def mostrar_frame(self, page_name):
        frame = self.__frames[page_name]
        frame.tkraise()
