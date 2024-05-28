from windowPaint import WindowPaint

class wxCanvaBaseConector(WindowPaint):
    def __init__(self):
        pass
    def OnMouseDown(WindowPaint, evt):
        WindowPaint.CaptureMouse()
        WindowPaint.x, WindowPaint.y = WindowPaint.lastx, WindowPaint.lasty = evt.GetPosition()
        print(f'MOUSEDOWN = x: {WindowPaint.x}, y:{WindowPaint.y}')
        WindowPaint.mouseDown(WindowPaint, evt)
        WindowPaint.Refresh(False)
        