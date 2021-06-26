from Piece import Piece
import pygame
import os

class Knight(Piece):
    def __init__(self,team):
        self.team = team
        if self.team:
            self.name = "white knight.png"
        else:
            self.name = "black knight.png"

        # self.surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        # image = pygame.image.load(os.path.join(os.path.dirname(__file__) + "\images", name))
        # image = pygame.transform.scale(image, (60, 60))
        # self.surf.blit(image, (0, 0))

    def ValidMove(self, x1,y1,x2,y2,p):
        if x2 == x1:
            return False
        slope = abs((y2-y1)/(x2 - x1))

        if slope == .5 or slope == 2:
            if abs(y2 - y1) <= 2 and abs(x2 - x1) <= 2:
                return True
            else:
                return False
        else:
            return False

    def ValidPath(self,x1,y1,x2,y2,p):
        return p[x1][y1].team == p[x2][y2].team
