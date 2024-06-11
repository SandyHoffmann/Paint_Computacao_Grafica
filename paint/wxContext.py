import wx
import sys
from windowPaint import WindowPaint
from paint.canva import CanvaPaint
try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

#----------------------------------------------------------------------
    
w=700
h=900

buttons = [
    {'id': wx.NewId(), 'label': '', 'pic': 'LineToolIcon.192.png', 'value': 'poligono'},
    {'id': wx.NewId(), 'label': '', 'pic': 'RectangleSelectToolIcon.192.png', 'value': 'selecao'},
    {'id': wx.NewId(), 'label': '', 'pic': 'MenuWindowToolsIcon.192.png', 'value': 'deletar'},
    {'id': wx.NewId(), 'label': '', 'pic': 'PanToolIcon.192.png', 'value': 'pan'},
    {'id': wx.NewId(), 'label': '', 'pic': 'MoveSelectionToolIcon.192.png', 'value': 'mover'},
    {'id': wx.NewId(), 'label': '', 'pic': 'MoveToolIcon.192.png', 'value': 'mover_ponto'},
    {'id': wx.NewId(), 'label': '', 'pic': 'IconFourWayArrow.png', 'value': 'transformacao'},
    {'id': wx.NewId(), 'label': '', 'pic': 'RectangleSelectToolIcon+.192.png', 'value': 'selecao+'},
    {'id': wx.NewId(), 'label': '', 'pic': 'rotate_right.png', 'value': 'rotacao'},
    {'id': wx.NewId(), 'label': '', 'pic': 'rotate_right.png', 'value': 'rotacao'},
    {'id': wx.NewId(), 'label': '', 'pic': 'zoom.png', 'value': 'zoomin'},
    {'id': wx.NewId(), 'label': '', 'pic': 'zoomout.png', 'value': 'zoomout'},


]

buttonsColors = [
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ff0000', 'wxValue': wx.RED},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#0000ff', 'wxValue': wx.BLUE},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#00ff00', 'wxValue': wx.GREEN},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ffff00', 'wxValue': wx.YELLOW},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ff00ff', 'wxValue': wx.Colour(255, 0, 255)},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#00ffff',   'wxValue': wx.CYAN},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#a52a2a',  'wxValue': wx.Colour(165, 42, 42)},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ffc0cb',   'wxValue': wx.Colour(255, 192, 203)},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ffa500', 'wxValue': wx.Colour(255, 165, 0)},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#800080', 'wxValue': wx.Colour(128, 0, 128)},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#ffffff',  'wxValue': wx.WHITE},
    {'id': wx.NewId(), 'label': '', 'pic': '', 'value': '#000000',  'wxValue': wx.BLACK},

]

buttonDefs = {
    wx.NewId() : ('Poligono',      'P'),
    wx.NewId() : ('ConeCanvas',      'C'),
     wx.NewId() : ('Poligono',      'A'),
    wx.NewId() : ('ConeCanvas',      'B'),
    }

class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        # appOpenGL=appOpenGL
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH) 
        box = wx.BoxSizer(wx.VERTICAL)
        
        #add background color to the box
        

        self.SetBackgroundColour((220,50,255))

        boxAbsolute = wx.BoxSizer(wx.HORIZONTAL)

        box.Add((40, 40))
        keys = buttonDefs.keys()
        caixaAtiva = wx.BoxSizer(wx.HORIZONTAL)

        alinhamento = 1
        for b in buttons:
            # text = buttonDefs[k][1]
            pic = wx.Bitmap(f'paint/paint/images/{b["pic"]}')
            pic = pic.ConvertToImage().Scale(20, 20).ConvertToBitmap()
            # pic.SetSize((30, 30))
            # btn = wx.BitmapButton(self, k, pic, pos=(0,0), size=(30,30))
            btn = wx.BitmapButton(self, b["id"], size=(35,35), style=wx.BU_AUTODRAW)
            #btn.SetBackgroundColour('RED')
            btn.SetBitmap(pic,wx.LEFT)
            btn.SetWindowStyleFlag(wx.BORDER_DOUBLE)
            caixaAtiva.Add(btn, 0, wx.ALIGN_CENTER)
            if (alinhamento % 2 == 0):
                box.Add(caixaAtiva, 0, wx.ALIGN_LEFT|wx.ALL, 3)
                caixaAtiva = wx.BoxSizer(wx.HORIZONTAL)

            alinhamento+=1
            
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn)

        caixaColors = wx.BoxSizer(wx.HORIZONTAL)
        for b in buttonsColors:
            btn = wx.Button(self, b["id"], size=(35,35), style=wx.BU_AUTODRAW)
            btn.SetWindowStyleFlag(wx.BORDER_DOUBLE)
            btn.SetBackgroundColour(b["wxValue"])
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn)
            caixaColors.Add(btn, 0, wx.ALIGN_CENTER)
            if (alinhamento % 2 == 0):
                box.Add(caixaColors, 0, wx.ALIGN_LEFT|wx.ALL, 3)
                caixaColors = wx.BoxSizer(wx.HORIZONTAL)

            alinhamento+=1

        # With this enabled, you see how you can put a GLCanvas on the wx.Panel
        
        boxAbsolute.Add(box, 0, wx.ALIGN_LEFT)
        boxAbsolute.Add(caixaColors, 0, wx.ALIGN_LEFT)

        self.c = CanvaPaint(self)
        self.c.SetMinSize((500, 500))
        boxAbsolute.Add(self.c, 0, wx.ALIGN_LEFT|wx.ALL, 15)

        self.SetAutoLayout(True)
        self.SetSizer(boxAbsolute)

    def OnButton(self, evt):
        if not haveGLCanvas:
            dlg = wx.MessageDialog(self,
                                   'The GLCanvas class has not been included with this build of wxPython!',
                                   'Sorry', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        elif not haveOpenGL:
            dlg = wx.MessageDialog(self,
                                   'The OpenGL package was not found.  You can get it at\n'
                                   'http://PyOpenGL.sourceforge.net/',
                                   'Sorry', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        else:
            canvasClassName = list(filter(lambda x: x['id'] == evt.GetId(), buttons))
            if len(canvasClassName) == 0:
                canvasClassName = list(filter(lambda x: x['id'] == evt.GetId(), buttonsColors))
            self.c.setState(canvasClassName[0]["value"])
            # canvasClass = eval(canvasClassName)
            # cx = 0
            # if canvasClassName == 'ConeCanvas': cx = 400
            # frame = wx.Frame(None, -1, canvasClassName, size=(400,400), pos=(cx,400))



            # canvasClass(frame) # CubeCanvas(frame) or ConeCanvas(frame); frame passed to MyCanvasBase
            # frame.Show(True)



class RunDemoApp(wx.App):
    global w,x
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1, "Paint: ", pos=(0,0),
                        style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        #frame.CreateStatusBar()

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")
        
        frame.SetMenuBar(menuBar)
        frame.Show(True)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        win = runTest(frame)
        
        # set the frame to a good size for showing the two buttons
        frame.SetSize((w,h)) 
        #paint.SetFocus()
        win.SetFocus()
        self.window = win
        frect = frame.GetRect()

        self.SetTopWindow(frame)
        self.frame = frame


        return True
        
    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()

def runTest(frame):
    win = ButtonPanel(frame)
    return win

app = RunDemoApp()
app.MainLoop()
