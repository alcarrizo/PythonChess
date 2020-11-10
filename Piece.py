from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self,team):
        pass
    def ValidMove(self, x1,y1,x2,y2,p):
        pass
    def ValidPath(self,x1,y1,x2,y2,p):
        pass



