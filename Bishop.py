from Piece import Piece
import pygame
import os

class Bishop(Piece):
    def __init__(self,team):
        self.team = team
        if self.team:
            name = "white bishop.png"
        else:
            name = "black bishop.png"

        self.surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        image = pygame.image.load(os.path.join(os.path.dirname(__file__) + "\images", name))
        image = pygame.transform.scale(image, (60, 60))
        self.surf.blit(image, (0, 0))

    def ValidMove(self, x1,y1,x2,y2,p):
        if x2 == x1:
            return False

        slope = abs((y2-y1)/(x2 - x1))
        if slope == 1 and self.ValidPath(x1,y1,x2,y2,p):
            return True
        else:
            return False

    def ValidPath(self,x1,y1,x2,y2,p):

        changeX = 1
        changeY = 1

        if x1 > x2:
            changeX = -1
        if y1 > y2:
            changeY = -1
        while x2 != (x1 + changeX) and y2 != (y1 + changeY):
            y1 += changeY
            x1 += changeX
            if p[x1][y1] is not None:
                return False

        return True

        pass
