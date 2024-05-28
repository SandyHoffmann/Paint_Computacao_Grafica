from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *


class EstadoMover(Estado):

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        print(AREA)
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)

        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]

        for forma in formas_selecionadas:
            forma.move((canva.x, canva.y))

        canva.Refresh(True)

    def OnMouseMotion(self, canva, evt): 
        pass