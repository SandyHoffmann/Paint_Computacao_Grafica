from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono


class EstadoTransformacao(Estado):

    #! indices pontos_selecao = [index_forma, index_ponto]

    def __init__(self) -> None:
        super().__init__()
        self.malha_inicializada = False
        self.formas = []

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

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , AREA, -AREA, AREA, -AREA)
        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]

    def OnMouseMotion(self, canva, evt): 
        if not self.malha_inicializada:
            self.inicializa_malha(canva)
            self.malha_inicializada = True
            
        if evt.Dragging() and evt.LeftIsDown():
            canva.Refresh(True)

        