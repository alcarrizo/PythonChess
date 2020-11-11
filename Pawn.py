from Piece import Piece
import pygame
import os

class Pawn(Piece):
    def __init__(self,team):
        self.firstMove = True
        self.enPassant = False
        self.team = team
        if(self.team):
            name = "white pawn.png"
        else:
            name = "black pawn.png"

        self.surf = pygame.Surface((60,60),pygame.SRCALPHA)
        image = pygame.image.load(os.path.join(os.path.dirname(__file__)+ "\images",name))
        image = pygame.transform.scale(image, (60, 60))
        self.surf.blit(image,(0,0))

    def ValidMove(self, x1,y1,x2,y2,p):
        if x2 == x1:
            return False

        slope = abs((y2 - y1) / (x2 - x1))
        moveSize = 1

        #white piece
        if(self.team):
            if x2 > x1 and y2 == y1 and p[x2][y2] is None or slope == 1 and self.Capture(x1,y1,x2,y2,p) and x2 > x1:
                if self.firstMove:
                    moveSize = 2
                if abs(x2-x1) <= moveSize and self.ValidPath(x1,y1,x2,y2,p):
                    self.firstMove = False
                    return True
                else:
                    return False
        # black piece
        else:
            if x2 < x1 and y2 == y1 and p[x2][y2] is None or slope == 1 and self.Capture(x1,y1,x2,y2,p) and x2 < x1:
                if self.firstMove:
                    moveSize = 2
                if abs(x2-x1) <= moveSize and self.ValidPath(x1,y1,x2,y2,p):
                    self.firstMove = False
                    return True
                else:
                    return False

    def ValidPath(self,x1,y1,x2,y2,p):
        changeX = 1
        if x1 > x2:
            changeX = -1

        while x2 != x1 + changeX:
            x1 += changeX
            if p[x1][y1] is not None:
                return False
        return True


    def Capture(self,x1,y1,x2,y2,p):
        if p[x2][y2] is None or abs(x2 - x1) > 1 and abs(y2 - y1) > 1:
            return False
        return True
