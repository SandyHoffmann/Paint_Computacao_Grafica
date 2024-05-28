from paint.forma import Forma
from OpenGL.GL import *
from OpenGL.GLUT import *

class Poligono(Forma):

    def __init__(self, x, y):
        super().__init__(x, y)  # Call the parent class constructor
        self.pontos = [(x, y)]
        self.pontoTemporario=False
        self.baricentro = False

    def mouseClick(self, x, y):
        self.pontos.append((x, y))

    def mouseMov(self, x, y):
        self.pontoTemporario = (x,y)
    
    def setPontoTemporario(self):
        self.pontoTemporario = False
        self.calculaBaricentro()

    def calculaBaricentro(self):
        qtdPontos = len(self.pontos)
        if (qtdPontos > 0):
            xb=0
            yb=0
            for ponto in self.pontos:
                xb += ponto[0]
                yb += ponto[1]

            self.baricentro = (xb/qtdPontos, yb/qtdPontos)

    def move(self, pMouse):
        # novosPontos = []
        # for ponto in self.pontos:
        #     dif = (ponto[0] + pMouse[0], ponto[1] + pMouse[1] )
        #     print(f'dif = {dif}')
        #     print(f'ponto = {ponto}')
        #     novosPontos.append((dif[0], dif[1]))
        # self.pontos = novosPontos
        novosPontos = []
        dif = (pMouse[0] - self.baricentro[0], pMouse[1] - self.baricentro[1] )
        for ponto in self.pontos:
            novosPontos.append((ponto[0] + dif[0] , ponto[1] + dif[1]))
        self.pontos = novosPontos
        self.baricentro = (pMouse[0], pMouse[1])
    def draw(self):
        
        glLineWidth(2)
        glColor3f(1.0, 0.0, 0.0) # definir a cor vermelha
        if self.pontoTemporario:
            glBegin(GL_LINE_STRIP) # tipo de primitiva que eu quero
        elif self.selecionado:
            glColor3f(0.0, 0.0, 1.0) # definir a cor azul
            glBegin(GL_LINE_LOOP) 

        else: 
            glBegin(GL_LINE_LOOP) 
        for i in self.pontos:
            glVertex2f(i[0],i[1])
        if self.pontoTemporario:
            glVertex2f(self.pontoTemporario[0],self.pontoTemporario[1])
        glEnd()

        if self.selecionado:
            glColor3f(1.0, 1.0, 1.0) # definir a cor branca
            glBegin(GL_POINTS)
            for i in self.pontos:
                glVertex2f(i[0],i[1])
            glEnd()


        if self.baricentro:
            glPointSize(5)
            glColor3f(0.0, 1.0, 0.0)
            glBegin(GL_POINTS)
            glVertex2d(self.baricentro[0], self.baricentro[1]) 
            glEnd()

        glFlush()
