from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *


class EstadoTransformacao(Estado):

    #! indices pontos_selecao = [index_forma, index_ponto]

    def __init__(self) -> None:
        super().__init__()
        self.malha_pontos_selecao = []
        self.inicializa_malha()

    def inicializa_malha(canva):
        min_y = 0
        max_y = 0
        min_x = 0
        max_x = 0
        
        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]
        
        for forma in formas_selecionadas:
            pontos_x = [ponto[0] for ponto in forma]
            pontos_y = [ponto[1] for ponto in forma]

        min_x = min(pontos_x)
        max_x = max(pontos_x)

        min_y = min(pontos_y)
        max_y = max(pontos_y)

        

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)
        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]

    def OnMouseMotion(self, canva, evt): 
        if evt.Dragging() and evt.LeftIsDown():
            canva.Refresh(True)

        