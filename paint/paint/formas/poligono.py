from paint.forma import Forma
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
#estado de poligono (pode ser feito qualquer poligono, como quadrados, retangulos, triangulos etc)
class Poligono(Forma):

    def __init__(self, x, y, cor_selecionada = (255, 0.0, 0.0)):
        super().__init__(x, y)  
        self.pontos = [(x, y)]
        self.pontoTemporario=False
        self.baricentro = False
        self.cor_selecionada = cor_selecionada

    def mouseClick(self, x, y):
        self.pontos.append((x, y))

    def mouseMov(self, x, y):
        self.pontoTemporario = (x,y)
    
    # calcula o area do poligono e o perimetro
    def calcularArea(self):
        n = len(self.pontos)
        # minimo de 3 pontos
        if n < 3:
            return 0  
        
        area = 0
        perimetro = 0
        for i in range(n):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[(i + 1) % n]
            distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            perimetro += distancia

            area += x1 * y2 - y1 * x2
        area = abs(area) / 2.0
        print(f'area = {round(area, 2)}')
        print(f'perimetro = {round(perimetro, 2)}')
        return area


    def setPontoTemporario(self):
        self.pontoTemporario = False
        self.calculaBaricentro()
    # calculo para calcular baricentro do poligono
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
       
        novosPontos = []
        dif = (pMouse[0] - self.baricentro[0], pMouse[1] - self.baricentro[1] )
        for ponto in self.pontos:
            novosPontos.append((ponto[0] + dif[0] , ponto[1] + dif[1]))
        self.pontos = novosPontos
        self.baricentro = (pMouse[0], pMouse[1])

    # desenha o poligono, se completo fechado, se ainda em temporario ira ter uma corda que facilita ao usuario continuar o desenho
    def draw(self):
        
        glLineWidth(2)
        glColor3f(self.cor_selecionada[0]/255, self.cor_selecionada[1]/255, self.cor_selecionada[2]/255) # definir a cor vermelha
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
