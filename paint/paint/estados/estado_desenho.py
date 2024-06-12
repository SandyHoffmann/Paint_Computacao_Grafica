from paint.estados.estado import *

import sys, os
from paint.canva import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
class EstadoDesenho(Estado):

    def __init__(self):
        super().__init__()
        self.cor_selecionada = (255, 0, 0)

    # com click do mouse inicia o desenho do poligono
    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
        if (not canva.layers[0].formas):
            canva.layers[0].formas = [Poligono(canva.x,canva.y, self.cor_selecionada)]
        else:
            canva.layers[0].formas[-1].mouseClick(canva.x, canva.y)
        canva.Refresh(False)

    def OnMouseMotion(self, canva, evt):
        # clicar com o botao direito para terminar o desenho
        if evt.RightDown():
            canva.layers[0].formas[-1].setPontoTemporario()
            canva.layers[0].formas[-1].draw()
            canva.estado_atual = canva.estado_idle
            canva.Refresh(True)
            return 
        # se nao continua o desenho
        canva.lastx, canva.lasty = canva.x, canva.y
        canva.x, canva.y = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)

        if (canva.layers[0].formas):
            canva.layers[0].formas[-1].mouseMov(canva.x, canva.y)
            canva.Refresh(False)
    

    def OnDraw(self, canva):
        pass