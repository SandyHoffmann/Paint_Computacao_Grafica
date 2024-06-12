from abc import ABC, abstractmethod
# classe abstrata de estado
class Estado(ABC):
    @abstractmethod
    def OnMouseDown(self, evt):
        pass
    
    @abstractmethod
    def OnMouseMotion(self, evt):
        pass

    @abstractmethod
    def OnDraw(self, canva):
        pass