from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *


class EstadoMoverPonto(Estado):

    #! indices pontos_selecao = [index_forma, index_ponto]

    def __init__(self) -> None:
        super().__init__()
        self.pontos_selecao = []

    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        print(canva.AREA)
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
        pontos_formatados = [0,0]


        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]

        primeiro_ponto = True
        margem_erro = 5
        for i_forma in range(len(formas_selecionadas)):
            forma_selecionada = formas_selecionadas[i_forma]
            for i_ponto in range(len(forma_selecionada.pontos)):
                if (
                    forma_selecionada.pontos[i_ponto][0] >= (canva.x - margem_erro) and forma_selecionada.pontos[i_ponto][0] <= (canva.x + margem_erro)  
                    and 
                    forma_selecionada.pontos[i_ponto][1] >= (canva.y - margem_erro) and forma_selecionada.pontos[i_ponto][1] <= (canva.y + margem_erro) 
                    ):
                        self.pontos_selecao = [[i_forma,i_ponto]]

    def OnMouseMotion(self, canva, evt): 
        if evt.Dragging() and evt.LeftIsDown():
            canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
            canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)

            # self.Refresh(False)
            formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]
            print(self.pontos_selecao)
            for indices_ponto_selecionado in self.pontos_selecao:
                formas_selecionadas[indices_ponto_selecionado[0]].pontos[indices_ponto_selecionado[1]] = [canva.x, canva.y]
            canva.Refresh(True)

    def OnDraw(self, canva):
        pass