from wxCanvaBase import MyCanvasBase
from OpenGL.GL import *
from OpenGL.GLUT import *
from paint.layer import Layer
from paint.formas.poligono import Poligono
from paint.estados.estado_desenho import *
from paint.estados.estado_idle import *
from paint.estados.estado_selecao import *
from paint.estados.estado_mover import *
from paint.estados.estado_mover_ponto import *
from paint.estados.estado_transformacao import *
from paint.estados.estado_rotacao import *
from paint.estados.estado_pan import *

import re

#definicao medidas iniciais

left=-10
right=110
top=-10
bottom=90
w,h = 500, 500
class CanvaPaint(MyCanvasBase):                
    AREA = 250
    # parametros para operação de pan
    pan_x = 0
    pan_y = 0
    #definicao de layer
    layers = [Layer()]

    #definicao de estados no padrão state
    estado_desenho = EstadoDesenho()
    estado_idle = EstadoIdle()
    estado_selecao = EstadoSelecao()
    estado_mover = EstadoMover()
    estado_atual = estado_desenho
    estado_mover_ponto = EstadoMoverPonto()
    estado_transformacao = EstadoTransformacao()
    estado_rotacao = EstadoRotacao()
    estado_pan = EstadoPan()
    #cor selecionada para desenho de formas
    cor_selecionada = (255, 0, 0)
    def InitGL(self):
        glutInit(sys.argv)
        glViewport(0, 0, 500, 500) # dizendo para ele ocupar a janela toda. Poderia, por exemplo, ocupar somente uma parte.
        glutInitWindowPosition(0, 0)
        glMatrixMode(GL_PROJECTION) # controla os parametros de visualizacao - camera
        glLoadIdentity() #
        glOrtho(-self.AREA + self.pan_x, self.AREA + self.pan_x, -self.AREA + self.pan_y, self.AREA + self.pan_y, -self.AREA, self.AREA) #ortho considerando area e pan
        glMatrixMode(GL_MODELVIEW) # pilha de matrizes de modelo - faz a rotacao, translacao de objetos - move os objetos pelo mundo - operacoes de visualizacao
        glLoadIdentity() #
    

    def showScreen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Trocando background color para roxo
        glClearColor(0.5,0.2,0.8,1)
        init()
        # glutPostRedisplay()
        glLoadIdentity()

    #funcoes onMouseDown e onMouseMotion padrões para cada state
    def OnMouseDown(self, evt):
        self.estado_atual.OnMouseDown(self,evt)

    def OnMouseMotion(self, evt):
        self.estado_atual.OnMouseMotion(self,evt)
            
    #funcao para desenho (tbm leva em conta ondraw dos estados)
    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Trocando background color para roxo
        glClearColor(0.5,0.2,0.8,1)
        glutInit(sys.argv)
        self.showScreen
        self.InitGL()

        glLoadIdentity()
        # desenhando as formas com seu metodo padrão
        for layer in self.layers:
            for forma in layer.formas:
                forma.draw()
       
        self.estado_atual.OnDraw(self)
        self.SwapBuffers()
    # definicao dos states,mudando estado atual
    def setState(self, state):
        print(state)
        pattern = re.compile(r'^#')
        self.pan_x = 0
        self.pan_y = 0
        match state:
            case "poligono":
                self.estado_atual = self.estado_idle
            case "idle":
                self.estado_atual = self.estado_idle
            case "selecao":
                self.estado_atual = self.estado_selecao
            case "mover":
                self.estado_atual = self.estado_mover
            case "deletar":
                #deletando todas as formas selecionadas
                for layer in self.layers:
                    novasFormas = []
                    for forma in layer.formas:
                        if not forma.selecionado:
                            novasFormas.append(forma)
                    layer.formas = novasFormas
                self.Refresh(True)
            case "mover_ponto":
                self.estado_atual = self.estado_mover_ponto
            case "rotacao":
                self.estado_rotacao.forma_original = False
                self.estado_atual = self.estado_rotacao
            case "transformacao":
                self.estado_transformacao.inicializa_malha(self)
                self.estado_atual = self.estado_transformacao
            case "zoomin":
                if self.AREA > 1:
                    self.AREA-=self.AREA/10
                    self.Refresh(True)
                    print("zoom")
            case "zoomout":
                self.AREA+=self.AREA/10
                self.Refresh(True)
                print("zoom-out")

            case "pan":
                self.estado_atual = self.estado_pan
                print("pan")
            case "size":
                print("size")
                for layer in self.layers:
                    for forma in layer.formas:
                        forma.calcularArea()
            case _:
                print("COLOR")
                # cor ja vem no padrão de hexadecimais, entao so é necessário coloca-lo na cor do estado de desenho
                if state[0] == '#':
                    print(state[1:3], state[3:5], state[5:7])
                    self.cor_selecionada = (int(state[1:3], 16), int(state[3:5], 16), int(state[5:7], 16)) 
                    self.estado_desenho.cor_selecionada = self.cor_selecionada
                self.estado_atual = self.estado_idle