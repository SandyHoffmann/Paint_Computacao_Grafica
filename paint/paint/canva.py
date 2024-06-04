from wxCanvaBase import MyCanvasBase
from OpenGL.GL import *
from OpenGL.GLUT import *
from paint.layer import Layer
from paint.formas.poligono import Poligono
from lib.coordenadas.getWorldCoords import *
from paint.estados.estado_desenho import *
from paint.estados.estado_idle import *
from paint.estados.estado_selecao import *
from paint.estados.estado_mover import *
from paint.estados.estado_mover_ponto import *
from paint.estados.estado_transformacao import *

left=-10
right=110
top=-10
bottom=90
w,h = 500, 500
AREA = 250
class CanvaPaint(MyCanvasBase):                

    layers = [Layer()]
    estado_desenho = EstadoDesenho()
    estado_idle = EstadoIdle()
    estado_selecao = EstadoSelecao()
    estado_mover = EstadoMover()
    estado_atual = estado_desenho
    estado_mover_ponto = EstadoMoverPonto()
    estado_transformacao = EstadoTransformacao()

    def InitGL(self):

        glutInit(sys.argv)
        glViewport(0, 0, 500, 500) # dizendo para ele ocupar a janela toda. Poderia, por exemplo, ocupar somente uma parte.
        glutInitWindowPosition(0, 0)
        glMatrixMode(GL_PROJECTION) # controla os parametros de visualizacao - camera
        glLoadIdentity() #
        #glOrtho(right, left, top, bottom, -1, 1)  # profundidade - no meu mundo eu quero ver de qual coordenada a qual coordenada? - left - right - bottom - top - se aumentar os valores diminui o zoom e se aumentar ocorre o inverso - projecao ortogonal
        glOrtho(-AREA, AREA, -AREA, AREA, -AREA, AREA)
        glMatrixMode(GL_MODELVIEW) # pilha de matrizes de modelo - faz a rotacao, translacao de objetos - move os objetos pelo mundo - operacoes de visualizacao
        glLoadIdentity() #
        # glutIdleFunc(self.OnDraw)
        # funcao motion (drag)
        # glutMotionFunc(self.OnMouseMotion)
        # funcao click
        # glutMouseFunc(self.OnMouseDown)
        # glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)

    def showScreen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Trocando background color para roxo
        glClearColor(0.5,0.2,0.8,1)
        init()
        # glutPostRedisplay()
        glLoadIdentity()

    def OnMouseDown(self, evt):
        self.estado_atual.OnMouseDown(self,evt)

    def OnMouseMotion(self, evt):
        self.estado_atual.OnMouseMotion(self,evt)
            
    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Trocando background color para roxo
        glClearColor(0.5,0.2,0.8,1)
        glutInit(sys.argv)
        self.showScreen
        self.InitGL()

        glLoadIdentity()
    
        # ? desenho do eixo x com comprimento 40
        glColor3f(1.0, 0.0, 0.0) # definir a cor vermelha
        glBegin(GL_LINES) # tipo de primitiva que eu quero
        glVertex2f(-20.0, 0.0) # passar as coordenadas de um dos vertices
        glVertex2f(20.0, 0.0) # passar as coordenadas do outro vertice
        glEnd()

        # ! Desenhando formas
        for layer in self.layers:
            for forma in layer.formas:
                forma.draw()
       
        # glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);
        self.estado_atual.OnDraw(self)
        self.SwapBuffers()

    def setState(self, state):
        match state:
            case "poligono":
                self.estado_atual = self.estado_desenho
            case "idle":
                self.estado_atual = self.estado_idle
            case "selecao":
                self.estado_atual = self.estado_selecao
            case "mover":
                self.estado_atual = self.estado_mover
            case "deletar":
                #implementar deletar
                for layer in self.layers:
                    novasFormas = []
                    for forma in layer.formas:
                        if not forma.selecionado:
                            novasFormas.append(forma)
                    layer.formas = novasFormas
                self.Refresh(True)
            case "mover_ponto":
                self.estado_atual = self.estado_mover_ponto
            case "transformacao":
                self.estado_transformacao.inicializa_malha(self)
                self.estado_atual = self.estado_transformacao

            case _:
                self.estado_atual = self.estado_desenho