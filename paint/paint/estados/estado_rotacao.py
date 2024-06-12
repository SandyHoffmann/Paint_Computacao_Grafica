from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

#estado responsavel por rotacionar objeto
class EstadoRotacao(Estado):

    def __init__(self) -> None:
        super().__init__()
        # necessita do ponto inicial e uma copia de sua forma original
        self.ponto_inicial = None
        self.drag = True
        self.forma_original = False

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)       

    def OnMouseMotion(self, canva, evt): 

        forma = [forma for forma in canva.layers[0].formas if forma.selecionado][0]
        # primeito define a copia da forma
        if not self.forma_original:
            forma = [forma for forma in canva.layers[0].formas if forma.selecionado][0]
            self.forma_original = forma.pontos
        # com o botao direito é coletado o ponto inicial
        if evt.RightDown():
            canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
            canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
            self.ponto_inicial = [canva.x, canva.y]
            self.drag = False
            
            canva.Refresh(True)

        if evt.LeftIsDown() and self.drag == False:       
            
            #comparando as distâncias com o centro do polígono
            dist_inicial = [self.ponto_inicial[0]-forma.baricentro[0],self.ponto_inicial[1]-forma.baricentro[1]]
            dist_final = [canva.x - forma.baricentro[0] , canva.y - forma.baricentro[1]]
            
            #seno e cosseno são feitos a partir das propriedades de produto escalar e produto vetorial
            seno = ( np.dot(dist_inicial , dist_final) ) / ( np.linalg.norm(dist_inicial)*np.linalg.norm(dist_final) )
            cosseno = ( np.linalg.norm(np.cross(dist_inicial , dist_final)) ) / ( np.linalg.norm(dist_inicial)*np.linalg.norm(dist_final) )
            #definindo matriz de rotacao para recalcular pontos
            matriz_rotacao =  np.array([[cosseno, -seno],[seno, cosseno]])
            
            rotacao_pontos = []

            #tranformar os pontos do polígono 
            for ponto in self.forma_original:
                ponto_dif = [ponto[0] - forma.baricentro[0], ponto[1] - forma.baricentro[1]]
                ponto_resultante = np.dot(matriz_rotacao, np.array([ponto_dif[0], ponto_dif[1]]))
                ponto_resultante = [ponto_resultante[0]+forma.baricentro[0] , ponto_resultante[1]+forma.baricentro[1]]
                rotacao_pontos.append(ponto_resultante)

            forma.pontos = rotacao_pontos

            canva.Refresh(True)
        




    # desenhando ponto
    def OnDraw(self, canva):
        if self.ponto_inicial:
            glColor3f(1.0, 1.0, 1.0) # definir a cor branca
            glBegin(GL_POINTS)
            glVertex2f(self.ponto_inicial[0],self.ponto_inicial[1])
            glEnd()

        