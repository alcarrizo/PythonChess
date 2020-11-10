from Piece import Piece
import pygame
import os

class Pawn(Piece):
    def __init__(self,team):
        self.firstMove = True
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
        pass
    def ValidPath(self,x1,y1,x2,y2,p):
        pass
    def enPassant(self):
        pass
    def Capture(self):
        pass