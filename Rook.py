from Piece import Piece
import pygame
import os

class Rook(Piece):
    def __init__(self,team):
        self.firstMove = True
        self.team = team
        if self.team:
            name = "white rook.png"
        else:
            name = "black rook.png"

        self.surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        image = pygame.image.load(os.path.join(os.path.dirname(__file__) + "\images", name))
        image = pygame.transform.scale(image, (60, 60))
        self.surf.blit(image, (0, 0))

    def ValidMove(self, x1,y1,x2,y2,p):



        if x2 == x1 or abs((y2 - y1) / (x2 - x1)) == 0:
            if self.ValidPath(x1,y1,x2,y2,p):
                return True
            else:
                return False
        else:
            return False

    def ValidPath(self,x1,y1,x2,y2,p):
        changeX = 1
        changeY = 1

        if x1 > x2:
            changeX = -1

        elif x1 == x2:
            changeX = 0

        if y1 > y2:
            changeY = -1

        elif y1 == y2:
            changeY = 0

        while x2 != (x1 + changeX) or y2 != (y1 + changeY):
            y1 += changeY
            x1 += changeX
            if p[x1][y1] is not None:
                return False

        return True