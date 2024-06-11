from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
class EstadoRotacao(Estado):

    #! indices pontos_selecao = [index_forma, index_ponto]

    def __init__(self) -> None:
        super().__init__()
        self.ponto_inicial = None
        self.drag = True
    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)


    def OnMouseMotion(self, canva, evt): 
        if self.drag == True and evt.LeftIsDown():
            self.ponto_inicial = [canva.x, canva.y]
            self.drag = False
        elif self.drag == False and self.ponto_inicial[0] != canva.x and self.ponto_inicial[1] != canva.y and not evt.LeftIsDown():
            self.drag = True
            print("canva.x = ", canva.x, "canva.y = ", canva.y)

            forma = [forma for forma in canva.layers[0].formas if forma.selecionado][0]

            # angulo = np.arctan2(canva.y - forma.baricentro[1], canva.x - forma.baricentro[0])
            print("Ponto inicial: ", self.ponto_inicial)
            # matriz_rotacao = np.array([[np.cos(angulo), -np.sin(angulo)], [np.sin(angulo), np.cos(angulo)]])
            raio = ((canva.y - self.ponto_inicial[1])**2 + (canva.x - self.ponto_inicial[0])**2)**(0.5)
            print(f'Raio: {raio}')
            if raio == 0:
                seno, cosseno = 0,1
            seno = (canva.y - self.ponto_inicial[1])/raio
            cosseno = (canva.x - self.ponto_inicial[0])/raio
            matriz_rotacao =  np.array([[cosseno, -seno],[seno, cosseno]])
            
            rotacao_pontos = []

            for ponto in forma.pontos:
                ponto_dif = [ponto[0] - forma.baricentro[0], ponto[1] - forma.baricentro[1]]
                ponto_resultante = np.dot(matriz_rotacao, np.array([ponto_dif[0], ponto_dif[1]]))
                ponto_resultante = [ponto_resultante[0]+forma.baricentro[0] , ponto_resultante[1]+forma.baricentro[1]]
                print(ponto_resultante)
                rotacao_pontos.append(ponto_resultante)

            # for ponto in forma.pontos:
            #     ponto_resultante = np.dot(matriz_rotacao, np.array([ponto[0], ponto[1]]))
            #     print(ponto_resultante)
            #     rotacao_pontos.append(ponto_resultante)

            forma.pontos = rotacao_pontos

            canva.Refresh(True)
    def OnDraw(self, canva):
        pass

        