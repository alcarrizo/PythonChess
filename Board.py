import pygame
from Pawn import Pawn
from Bishop import Bishop
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from movement import Movement

from Piece import Piece
from _thread import *

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
        self.whitePieces = []
        self.blackPieces = []
        self.livePieces = []

    def getPieces(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] is not None:
                    if self.board[i][j].team:
                        self.whitePieces.append(self.board[i][j])
                        self.livePieces.append(self.board[i][j])
                    else:
                        self.blackPieces.append(self.board[i][j])
                        self.livePieces.append(self.board[i][j])

    def removePiece(self,piece):
        pass
    def enemyChecks(self,x2,y2):
        pass

    def changePiece(self,x2,y2,name):
        name = name.upper()
        tempPiece = self.board[x2][y2]

        if name == "QUEEN":
            self.board[x2][y2] = Queen(self.board[x2][y2].team)
        elif name == "ROOK":
            self.board[x2][y2] = Rook(self.board[x2][y2].team)
        elif name == "KNIGHT":
            self.board[x2][y2] = Knight(self.board[x2][y2].team)
        elif name == "BISHOP":
            self.board[x2][y2] = Bishop(self.board[x2][y2].team)

        self.livePieces.remove(tempPiece)
        self.livePieces.append(self.board[x2][y2])

        if tempPiece.team:
            self.whitePieces.remove(tempPiece)
            self.whitePieces.append(self.board[x2][y2])
        else:
            self.blackPieces.remove(tempPiece)
            self.blackPieces.append(self.board[x2][y2])

        tempBool = False
        # insufficient material draw code here








    def boardUpdate(self,win):
        width,height = pygame.display.get_surface().get_size()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    # black player rotation
                    win.blit(self.board[i][j].surf,((width/2 ) - (60 * 4) + (60 * j),(height / 2 - (60 * 4)) + (60 * i)))
                    # white player rotation
                    #win.blit(pygame.transform.flip(self.board[i][j].surf, False, True),((width/2 ) - (60 * 4) + (60 * j),(height / 2 - (60 * 4)) + (60 * i)))


    def move(self,x1,y1,x2,y2):
        if self.board[x1][y1] is not None:
            if (self.board[x2][y2] is not None and self.board[x1][y1].team != self.board[x2][y2].team) or self.board[x2][y2] is None:
                if self.board[x1][y1].ValidMove(x1,y1,x2,y2,self.board):
                    self.board[x1][y1],self.board[x2][y2] = None,self.board[x1][y1]

    def isEmpty(self,x,y):
        return self.board[x][y] is None