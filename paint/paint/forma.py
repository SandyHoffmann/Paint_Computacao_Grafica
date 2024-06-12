from abc import ABC, abstractmethod

# Forma abstrata para ser implementada a cada forma
class Forma(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color_linha = (255, 255, 255)
        self.color_preenchimento = False
        self.pontos = []
        self.pontoTemporario = False
        self.selecionado = False
        self.baricentro = (0,0)

    def set_selecionado(self):
        self.selecionado = not self.selecionado

    def set_color_linha(self, color):
        self.color_linha = color

    def set_color_preenchimento(self, color):
        self.color_preenchimento = color

    def verifica_colisao(self, x, y):
        pass
    @abstractmethod
    def mouseClick(self, x, y):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def mouseMov(self, x, y):
        pass

    @abstractmethod
    def setPontoTemporario(self):
        pass

    @abstractmethod
    def calcularArea(self):
        pass