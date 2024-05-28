from abc import ABC, abstractmethod

class Estado(ABC):
    @abstractmethod
    def OnMouseDown(self, evt):
        pass
    
    @abstractmethod
    def OnMouseMotion(self, evt):
        pass

