from movement import Movement
from Pawn import Pawn
from Bishop import Bishop
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight

class Game:
    def __init__(self,wkx,wky,bkx,bky):
        self.whitekingX = wkx
        self.whitekingY = wky
        self.blackKingX = bkx
        self.blackKingY = bky
        self.checkPieces = []
        self.width = 8
        self.height = 8
        self.tempPawn = None


    def Move(self,x1,y1,x2,y2,board,moveInfo):
        enPassant = False
        move = False

        if not self.allyPieces(x1,y1,x2,y2,board) and not self.allyKinginCheck(x1,y1,x2,y2,board):

            if board[x1][y1] is not None:

                #standard move
                if board[x1][y1].ValidMove(x1, y1, x2, y2, board):
                    move = True

                    if isinstance(board[x1][y1],King):

                        if board[x1,y1].team:
                            self.whitekingX = x2
                            self.whitekingY = y2
                        else:
                            self.blackKingX = x2
                            self.blackKingY = y2

                        tempKing = board[x1][y1]
                        tempKing.firstMove = False
                    elif isinstance(board[x1][y1],Rook):
                        tempRook = board[x1][y1]
                        tempRook.firstMove = False
                    elif isinstance(board[x1][y1], Pawn):
                        if abs(x1-x2) == 2 and ((y1 > 0 and isinstance(board[x2][y2-1],Pawn)) or (y1 < self.width - 1 and isinstance(board[x2][y2+1],Pawn))):
                            if self.tempPawn is not None:
                                if self.tempPawn.enPassant:
                                    self.tempPawn.enPassant = False
                            self.enPassant = True
                            self.tempPawn = board[x1][y1]
                            self.tempPawn.enPassant = True
                #check castling
                elif(isinstance(board[x1][y1],King)) and self.isCastling(x1,y1,x2,y2,board,moveInfo):
                    move = True
                    if board[x1][y1].team:
                        self.whitekingX = x2
                        self.whitekingY = y2
                    else:
                        self.blackKingX = x2
                        self.blackKingY = y2
                    moveInfo.castling = True
                #check enPassant
                elif(isinstance(board[x1][y1],Pawn)) and self.isEnpassant(x1,y1,x2,y2,board,moveInfo):
                    move = True
                    moveInfo.enPassant = True

                if move == True:
                    board[x1][y1], board[x2][y2] = None, board[x1][y1]

                    if self.enPassant == True and self.tempPawn is not None:
                        if self.tempPawn.enPassant:
                            self.tempPawn.enPassant = False
                        tempPawn = None
        return move


    def isEnpassant(self,x1,y1,x2,y2,board,moveInfo):
        capture = False
        slope = abs((y2 -y1) / (x2-x1))
        if slope == 1 and abs(x2-x1) == 1 and abs(y2 -y1) == 1:
            if board[x1][y1].team == True and y2 > y1:
                if board[x2][y2 - 1] is not None and board[x2][y2 - 1].team != board[x1][y1].team:
                    temp = board[x2][y2 - 1]
                    if temp.enPassant:
                        moveInfo.pawnX = x2
                        moveInfo.pawnY = y2 - 1

                        capture = True
                        board[x2][y2 - 1] = None;

            elif board[x1][y1].team == False and y2 < y1:
                if board[x2][y2 + 1] is not None and board[x2][y2 + 1].team != board[x1][y1].team:
                    temp = board[x2][y2 + 1]
                    if temp.enPassant == True:
                        moveInfo.pawnX = x2
                        moveInfo.pawnY = y2 + 1

                        capture = True
                        board[x2][y2 + 1] = None

        return capture


    def isCastling(self,x1,y1,x2,y2,board,moveInfo):
        castling = False
        clearSpace = True
        tempKing = board[x1][y1]
        tempRook = None


        if x1 - x2 == -2 and y1 == y2:

            if board[0][y1] is not None and isinstance(board[0][y1],Rook):
                tempRook = board[self.width - 1][ y1]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(x1 + 1,self.width - 1):
                        if board[i][y1] is not None or (i <= x2 and self.Capture(i, y1, board[x1][y1].team, board)):
                            clearSpace = False
                else:
                    clearSpace = False

            if clearSpace == True:

                moveInfo.rookStartX = self.width - 1
                moveInfo.rookStartY = y1
                moveInfo.rookEndX = x2 - 1
                moveInfo.rookEndY = y1

                board[x2 - 1][y1],board[self.width - 1][y1] = board[self.width - 1][y1],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        elif x1 - x2 == 2 and y1 == y2:

            if board[0][y1] is not None and isinstance(board[0][y1],Rook):
                tempRook = board[0][y1]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(x1 - 1,0,-1):
                        if board[i][y1] is not None or (i >= x2 and self.Capture(i, y1, board[x1][y1].team, board)):
                            clearSpace = False

                else:
                    clearSpace = False

            if clearSpace:

                moveInfo.rookStartX = 0
                moveInfo.rookStartY = y1
                moveInfo.rookEndX = x2 + 1
                moveInfo.rookEndY = y1

                board[x2 + 1][ y1],board[0][y1] = board[0][y1],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        return castling;


    def enemyChecks(self,x2,y2,board,moveInfo):
        mate = False

        if self.enemyKinginCheck(x2,y2,board):
            moveInfo.check = True

            self.checkPieces.clear()
            self.FindCheckPieces(board[x2][y2].team,board)

            for point in self.checkPieces:
                if self.checkMate(point[0],point[1],board):
                    moveInfo.checkMate = True
                    mate = True
        return mate

    def allyKinginCheck(self,x1,y1,x2,y2,board):
        if isinstance(board[x1][y1],King):
            if board[x1][y1].team:
                self.whitekingX = x2
                self.whitekingY = y2
            else:
                self.blackKingX = x2
                self.blackKingY = y2

        temp = board[x2][y2] # keeping piece to revert the change later
        board[x2][y2],board[x1][y1] = board[x1][y1],None

        if(board[x2][y2].team):
            if self.Capture(self.whitekingX,self.whitekingY,True, board):
                board[x1][y1] = board[x2][y2]
                board[x2][y2] = temp
                if isinstance(board[x1][y1],King):
                    self.whitekingX = x1
                    self.whitekingY = y1
                return True
            else:
                board[x1][y1],board[x2][y2] = board[x2][y2],temp
                if isinstance(board[x1][y1],King):
                    self.whitekingX = x1
                    self.whitekingY = y1
                return False
        else:
            if self.Capture(self.blackKingX,self.blackKingY,True, board):
                board[x1][y1] = board[x2][y2]
                board[x2][y2] = temp
                if isinstance(board[x1][y1],King):
                    self.blackKingX = x1
                    self.blackKingY = y1
                return True
            else:
                board[x1][y1],board[x2][y2] = board[x2][y2],temp
                if isinstance(board[x1][y1],King):
                    self.blackKingX = x1
                    self.blackKingY = y1
                return False


    def enemyKinginCheck(self,x2,y2,board):

        kx = 0
        ky = 0

        if board[x2][y2].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        if self.Capture(kx,ky,board[kx][ky].team,board):
            return True

        return False

    def checkMate(self,x,y,board):

        checkMate = True
        kx = 0
        ky = 0

        if self.stopCheck(kx,ky,board):
            checkMate = False

        if board[x][y].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        for i in range (-1,2):
            for j in range(-1, 2):
                if not self.Capture(kx + i, ky + j, board[kx, ky].team, board) and not self.AllyPieces(kx,ky, kx + i, ky + j, board) and board[kx, ky].ValidMove(kx,ky, kx + i,ky + j, board):
                    checkMate = False

        return checkMate

    def stopCheck(self,x,y,board):
        pass

    def FindCheckPieces(self,team,board):
        pass

    def Capture(self,x,y,team,board):
        pass

    def removePieces(self,tempPiece,moveInfo,livePieces,whitePieces,blackPieces,board):
        pass

    def insufficientMaterial(self,livePieces,whitePieces,blackPieces,board):
        pass

    def updateEnemyPieces(self, moveInfo, board,livePieces,whitePieces,blackPieces):
        pass

    def allyPieces(self,x1,y1,x2,y2,board):
        if board[x1][y1].team == board[x2][y2].team:
            return True
        else:
            return False