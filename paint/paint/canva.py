from wxCanvaBase import MyCanvasBase
from OpenGL.GL import *
from OpenGL.GLUT import *
from paint.layer import Layer
from paint.formas.poligono import Poligono
from lib.coordenadas.getWorldCoords import *

left=-10
right=110
top=-10
bottom=90
w,h = 500, 500
AREA = 250
class CanvaPaint(MyCanvasBase):                

    layers = [Layer()]
    estado_desenho = 1
    estado_idle = 2
    estado_selecao = 3
    estado_mover = 4
    estado_atual = estado_desenho
    estado_mover_ponto = 5


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
        if self.estado_atual == 1:
            self.CaptureMouse() 
            self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
            
            self.x, self.y  = getWorldCoords(self.x, self.y , AREA, -AREA, AREA, -AREA)
            print(f'MOUSEDOWN = x: {self.x}, y:{self.y}')
            # ! Verifica modo ativo.
            if (not self.layers[0].formas):
                self.layers[0].formas = [Poligono(self.x,self.y)]
            else:
                self.layers[0].formas[-1].mouseClick(self.x, self.y)
            self.Refresh(False)
        elif self.estado_atual == 2:
            self.CaptureMouse() 
            self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
            
            self.x, self.y  = getWorldCoords(self.x, self.y , AREA, -AREA, AREA, -AREA)

            self.layers[0].formas.append(Poligono(self.x, self.y))
            estado_atual = 1

        # self.estado_atual.OnMouseDown(self,evt)

    def OnMouseMotion(self, evt):
        if self.estado_atual == 1:
           if evt.RightDown():
                self.layers[0].formas[-1].setPontoTemporario()
                self.layers[0].formas[-1].draw()
                self.estado_atual = 2
                self.Refresh(True)
                return 
            
           self.lastx, self.lasty = self.x, self.y
           self.x, self.y = evt.GetPosition()
           self.x, self.y  = getWorldCoords(self.x, self.y , AREA, -AREA, AREA, -AREA)

           if (self.layers[0].formas):
               self.layers[0].formas[-1].mouseMov(self.x, self.y)
               self.Refresh(False)


        elif self.estado_atual == 2:
            pass

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

        self.SwapBuffers()

    def setState(self, state):
        match state:
            case "poligono":
                self.estado_atual = 1
            case "idle":
                self.estado_atual = 2
