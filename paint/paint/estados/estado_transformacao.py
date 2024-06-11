from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
class EstadoTransformacao(Estado):

    #! indices pontos_selecao = [index_forma, index_ponto]

    def __init__(self) -> None:
        super().__init__()
        self.malha_inicializada = False
        self.formas = []
        self.ponto_selecionado = None
        self.posicao_inicial = None
    def inicializa_malha(self,canva):
        self.formas = []

        min_y = 0
        max_y = 0
        min_x = 0
        max_x = 0
        
        formas_selecionadas = [forma.pontos for forma in canva.layers[0].formas if forma.selecionado]
        print("formas_selecionadas = ", formas_selecionadas)
        for forma in formas_selecionadas:
            pontos_x = [ponto[0] for ponto in forma]
            pontos_y = [ponto[1] for ponto in forma]

            min_x = min(pontos_x)
            max_x = max(pontos_x)

            min_y = min(pontos_y)
            max_y = max(pontos_y)

            self.malha_pontos_selecao = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

            novo_poligono = Poligono(min_x, min_y)
            novo_poligono.pontos = self.malha_pontos_selecao
            # canva.layers[0].formas.append(novo_poligono)
            # canva.layers[0].formas[-1].draw()

            self.formas.append(novo_poligono)

        print("min_x = ", min_x, "max_x = ", max_x, "min_y = ", min_y, "max_y = ", max_y)
        canva.Refresh(True)

    def OnDraw(self, canva):
        for forma in self.formas:
            forma.draw()
        
        glColor3f(1.0, 1.0, 1.0) # definir a cor branca
        glBegin(GL_POINTS)
        for forma in self.formas:
            for i in forma.pontos:
                glVertex2f(i[0],i[1])
        glEnd()


    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)

        margem_erro = 5

        for i_forma in range(len(self.formas)):
            for i_ponto in range(len(self.formas[i_forma].pontos)):
                if (
                    self.formas[i_forma].pontos[i_ponto][0] >= (canva.x - margem_erro) and self.formas[i_forma].pontos[i_ponto][0] <= (canva.x + margem_erro)  
                    and 
                    self.formas[i_forma].pontos[i_ponto][1] >= (canva.y - margem_erro) and self.formas[i_forma].pontos[i_ponto][1] <= (canva.y + margem_erro) 
                    ):
                    print("ponto selecionado = ", self.formas[i_forma].pontos[i_ponto])
                    self.ponto_selecionado = [i_forma,i_ponto]
                    self.posicao_inicial = [canva.x, canva.y]
                    canva.Refresh(True)

    def OnMouseMotion(self, canva, evt): 
        if not self.malha_inicializada:
            self.inicializa_malha(canva)
            self.malha_inicializada = True
            
        if evt.Dragging() and evt.LeftIsDown():
            print("canva.x = ", canva.x, "canva.y = ", canva.y)
            print("ponto selecionado = ", self.ponto_selecionado)
            if self.ponto_selecionado == None:
                return
            print("posicao_inicial = ", self.posicao_inicial)

            i_forma, _ = self.ponto_selecionado
            forma =  [forma for forma in canva.layers[0].formas if forma.selecionado][i_forma]

            # largura = self.formas[i_forma].pontos[2][0] - self.formas[i_forma].pontos[0][0]
            # altura = self.formas[i_forma].pontos[2][1] - self.formas[i_forma].pontos[0][1]

            # Calculate centroid
            centroid = np.mean(forma.pontos, axis=0)

            largura = self.posicao_inicial[0] - centroid[0]
            altura = self.posicao_inicial[1] - centroid[1]

            dx = canva.x - self.posicao_inicial[0]
            dy = canva.y - self.posicao_inicial[1]


             
            escalar_largura = (largura+dx)/largura 
            escalar_altura = (altura+dy)/altura
            # Calculate the distance the mouse has moved
            dist_moved = np.sqrt(dx**2 + dy**2)
            
            # Determine the scale factor based on the distance moved
            if dist_moved == 0:
                return

            # Scale the polygon
            scaled_pontos = []
            for x, y in forma.pontos:
                
                new_x = centroid[0] + escalar_largura * (x - centroid[0])
                new_y = centroid[1] + escalar_altura * (y - centroid[1])
                scaled_pontos.append((new_x, new_y))
            print("scaled_pontos = ", scaled_pontos)
            forma.pontos = scaled_pontos
            self.posicao_inicial = [canva.x, canva.y]
            self.inicializa_malha(canva)
            canva.Refresh(True)

        