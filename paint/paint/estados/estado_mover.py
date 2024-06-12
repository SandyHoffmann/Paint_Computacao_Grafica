from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *

# estado que move a figura inteira pelo seu centro
class EstadoMover(Estado):

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)

        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]
        # cada figura deve ter seu movimento padrão
        for forma in formas_selecionadas:
            forma.move((canva.x, canva.y))

        canva.Refresh(True)

    def OnMouseMotion(self, canva, evt): 
        pass

    def OnDraw(self, canva):
        pass