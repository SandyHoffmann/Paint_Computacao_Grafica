from paint.estados.estado import *
from paint.formas.poligono import *
from lib.coordenadas.getWorldCoords import *


class EstadoIdle(Estado):

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)

        canva.layers[0].formas.append(Poligono(canva.x, canva.y, canva.cor_selecionada))
        canva.estado_atual = canva.estado_desenho

    def OnMouseMotion(self, canva, evt): 
        pass

    def OnDraw(self, canva):
        pass