from wxCanvaBase import MyCanvasBase
from OpenGL.GL import *
from OpenGL.GLUT import *

class WindowPaint(MyCanvasBase):
    def InitGL(self):
        glutInit(sys.argv)
        glViewport(0, 0, 500, 500) # dizendo para ele ocupar a janela toda. Poderia, por exemplo, ocupar somente uma parte.
        glMatrixMode(GL_PROJECTION) # controla os parametros de visualizacao - camera
        glLoadIdentity() #
        glOrtho(right, left, top, bottom, -1, 1) # profundidade - no meu mundo eu quero ver de qual coordenada a qual coordenada? - left - right - bottom - top - se aumentar os valores diminui o zoom e se aumentar ocorre o inverso - projecao ortogonal
        glMatrixMode(GL_MODELVIEW) # pilha de matrizes de modelo - faz a rotacao, translacao de objetos - move os objetos pelo mundo - operacoes de visualizacao
        glLoadIdentity() 
        glutIdleFunc(showScreen)
        # funcao motion (drag)
        glutMotionFunc(mousePos)
        # funcao click
        glutMouseFunc(mouseClick)
        # glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        print(f'MOUSEDOWN = x: {self.x}, y:{self.y}')
        mouseClick(False,False,self.x, self.y)
        self.Refresh(False)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            mousePos(self.x, self.y)
            self.Refresh(False)
            
    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        print(self.lastx)
        # Trocando background color para roxo
        glClearColor(0.5,0.2,0.8,1)
        glutInit(sys.argv)
        showScreen()

        # glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);

        self.SwapBuffers()
