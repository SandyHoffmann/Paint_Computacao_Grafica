from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *


#estado que move formas pelos seus pontos, se estas estiverem selecionadas
class EstadoMoverPonto(Estado):

    def __init__(self) -> None:
        super().__init__()
        self.pontos_selecao = []

    # detecta qual ponto foi pressionado
    def OnMouseDown(self, canva, evt):

        # pegando pontos
        canva.CaptureMouse() 
        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)

        # formas selecionadas são pegas
        formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]
        # margem de erro para saber se o ponto foi selecionado
        margem_erro = 5
        for i_forma in range(len(formas_selecionadas)):
            forma_selecionada = formas_selecionadas[i_forma]
            for i_ponto in range(len(forma_selecionada.pontos)):
                # verifica se ponto foi selecionado e move para os pontos da selecao
                if (
                    forma_selecionada.pontos[i_ponto][0] >= (canva.x - margem_erro) and forma_selecionada.pontos[i_ponto][0] <= (canva.x + margem_erro)  
                    and 
                    forma_selecionada.pontos[i_ponto][1] >= (canva.y - margem_erro) and forma_selecionada.pontos[i_ponto][1] <= (canva.y + margem_erro) 
                    ):
                        self.pontos_selecao = [[i_forma,i_ponto]]

    def OnMouseMotion(self, canva, evt): 
        # cada ponto da selecao deve ser movido conforma drag do mouse
        if evt.Dragging() and evt.LeftIsDown():
            canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
            canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
            formas_selecionadas = [forma for forma in canva.layers[0].formas if forma.selecionado]
            for indices_ponto_selecionado in self.pontos_selecao:
                formas_selecionadas[indices_ponto_selecionado[0]].pontos[indices_ponto_selecionado[1]] = [canva.x, canva.y]
            canva.Refresh(True)

    def OnDraw(self, canva):
        pass