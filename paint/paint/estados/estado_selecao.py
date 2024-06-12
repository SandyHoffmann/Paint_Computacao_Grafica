from paint.estados.estado import *
from paint.formas.poligono import *
from lib.coordenadas.getWorldCoords import *
import sys

"""
Estado para selecionar poligonos

Utilizando o Ray Casting Algorithm
Fonte: https://rosettacode.org/wiki/Ray-casting_algorithm
"""
class EstadoSelecao(Estado):

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
        
        c = 0
        d = 0

        # utilizando o algoritmo de Ray Casting, formas selecionadas sao indicadas e mandadas ao canva

        for i in range(len(canva.layers[0].formas)):
            forma_atual = canva.layers[0].formas[i]
            quant_pontos_dentro = 0
            for j in range(len(forma_atual.pontos)):
                ponto_atual = forma_atual.pontos[j]
                indice_j = j + 1
                if (indice_j >= len(forma_atual.pontos)):
                    indice_j = 0
                ponto_prox = forma_atual.pontos[indice_j]
                if (self.checkIntersection((canva.x, canva.y), [ponto_atual, ponto_prox])):
                    quant_pontos_dentro += 1
            if quant_pontos_dentro % 2 == 1:
                print("Ponto dentro")
                canva.layers[0].formas[i].set_selecionado()
                canva.Refresh(True)
            else:
                print("Ponto fora")
        
    def OnMouseMotion(self, canva, evt): 
        pass

    def checkIntersection(self, p, linhaForma):
        
        p1 = linhaForma[0]
        p2 = linhaForma[1]
        
        if p[1] > min(p1[1], p2[1]):
            if p[1] <= max(p1[1], p2[1]):
                if p[0] <= max(p1[0], p2[0]):
                    xinters = 0
                    if p1[1] - p[1] != 0:
                        xinters = (p[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                        if p1[0] == p2[0] or p[0] <= xinters:
                            return True
        return False

    def OnDraw(self, canva):
        pass