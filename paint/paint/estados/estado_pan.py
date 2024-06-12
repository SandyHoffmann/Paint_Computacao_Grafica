from paint.estados.estado import *
from lib.coordenadas.getWorldCoords import *
from paint.formas.poligono import Poligono
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# estado para visualizacao do tipo pan
class EstadoPan(Estado):

    def __init__(self) -> None:
        super().__init__()
        self.is_panning = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0


    def OnDraw(self, canva):
        pass

    #guarda ultima movimentacao do mouse
    def OnMouseDown(self, canva, evt):
        canva.CaptureMouse() 

        canva.x, canva.y = canva.lastx, canva.lasty = evt.GetPosition()
        canva.x, canva.y  = getWorldCoords(canva.x, canva.y , canva.AREA, -canva.AREA, canva.AREA, -canva.AREA)
        self.is_panning = True
        self.last_mouse_x = canva.x
        self.last_mouse_y = canva.y
    # compara ultima movimentacao com movimentacao atual e arrasta o campo de visao (é resetado quando sai do modo pan)
    def OnMouseMotion(self, canva, evt): 
        if self.is_panning:
            dx = evt.x - self.last_mouse_x
            dy = evt.y - self.last_mouse_y
            canva.pan_x += dx * (canva.AREA / (500*4))  # Scale the pan speed
            canva.pan_y -= dy * (canva.AREA / (500*4))  # Scale the pan speed
            self.last_mouse_x = evt.x
            self.last_mouse_y = evt.y
            canva.Refresh(True)
        if not evt.LeftIsDown():
            self.is_panning = False