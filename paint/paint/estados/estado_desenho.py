from paint.estados.estado import *

import sys, os
from paint.canva import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
class EstadoDesenho(Estado):

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)
        print(f'MOUSEDOWN = x: {canva.x}, y:{canva.y}')
        # ! Verifica modo ativo.
        if (not canva.layers[0].formas):
            canva.layers[0].formas = [Poligono(canva.x,canva.y)]
        else:
            canva.layers[0].formas[-1].mouseClick(canva.x, canva.y)
        canva.Refresh(False)

    def OnMouseMotion(self, canva, evt):
           
        # if evt.Dragging() and evt.LeftIsDown():
        #     self.lastx, self.lasty = self.x, self.y
        #     self.x, self.y = evt.GetPosition()
            #mousePos(self.x, self.y)

        if evt.RightDown():
            canva.layers[0].formas[-1].setPontoTemporario()
            canva.layers[0].formas[-1].draw()
            canva.estado_atual = canva.estado_idle
            canva.Refresh(True)
            return 
        
        canva.lastx, canva.lasty = canva.x, canva.y
        canva.x, canva.y = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)

        if (canva.layers[0].formas):
            canva.layers[0].formas[-1].mouseMov(canva.x, canva.y)
            canva.Refresh(False)
