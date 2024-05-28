import wx

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from wx import glcanvas
    haveGLCanvas = True 
except ImportError:
    haveGLCanvas = False

"""
MyCanvasBase representa a base para ligação das funcionalidades com a biblioteca do wxPython
Seus métodos devem ser implementados pelas classes filhas
"""
class MyCanvasBase(glcanvas.GLCanvas):

    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        pass
        # size = self.size = self.GetClientSize()
        # self.SetCurrent(self.context)
        # glViewport(0, 0, 500, 500)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        # if not self.init:
        #     self.InitGL()
        #     self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        print(f'x: {self.x}, y:{self.y}')

    def OnMouseUp(self, evt):
        try:
            self.ReleaseMouse()
        except:
            pass
        pass
    
    def OnMouseMotion(self, evt):
        pass
        # if evt.Dragging() and evt.LeftIsDown():
        #     self.lastx, self.lasty = self.x, self.y
        #     self.x, self.y = evt.GetPosition()
        #     self.Refresh(False)
