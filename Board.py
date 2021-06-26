import pygame
from Pawn import Pawn
from Bishop import Bishop
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
import os



class Board:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.board = [[None for i in range(self.width)] for j in range(self.height)]

        self.board[0][0] = Rook(True)
        self.board[0][1] = Knight(True)
        self.board[0][2] = Bishop(True)
        self.board[0][3] = King(True)
        self.board[0][4] = Queen(True)
        self.board[0][5] = Bishop(True)
        self.board[0][6] = Knight(True)
        self.board[0][7] = Rook(True)
        for i in range(self.width):
            self.board[1][i] = Pawn(True)
            self.board[self.height - 2][i] = Pawn(False)
        self.board[self.height - 1][0] = Rook(False)
        self.board[self.height - 1][1] = Knight(False)
        self.board[self.height - 1][2] = Bishop(False)
        self.board[self.height - 1][3] = King(False)
        self.board[self.height - 1][4] = Queen(False)
        self.board[self.height - 1][5] = Bishop(False)
        self.board[self.height - 1][6] = Knight(False)
        self.board[self.height - 1][7] = Rook(False)

    def boardUpdate(self,win, playerTeam):
        width,height = pygame.display.get_surface().get_size()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    image = pygame.image.load(os.path.join(os.path.dirname(__file__) + "\images", self.board[i][j].name))
                    image = pygame.transform.scale(image, (60, 60))
                    # black player rotation
                    if playerTeam == False:
                       win.blit(image,((width/2 ) - (60 * 4) + (60 * j),(height / 2 - (60 * 4)) + (60 * i)))
                    # white player rotation
                    else:
                        win.blit(pygame.transform.flip(image, False, True),((width/2 ) - (60 * 4) + (60 * j),(height / 2 - (60 * 4)) + (60 * i)))


    def isPawn(self,x,y):
        return isinstance(self.board[x][y],Pawn)

    def getTeam(self,x,y):
        return self.board[x][y].team

    def isEmpty(self, x, y):
        return self.board[x][y] is None