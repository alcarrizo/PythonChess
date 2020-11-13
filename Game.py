from movement import Movement
from Pawn import Pawn
from Bishop import Bishop
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from _thread import *
import pygame

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

                        if board[x1][y1].team:
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

                    if enPassant == True and self.tempPawn is not None:
                        if self.tempPawn.enPassant:
                            self.tempPawn.enPassant = False
                        tempPawn = None
        return move


    def isEnpassant(self,x1,y1,x2,y2,board,moveInfo):
        capture = False

        if abs(x2-x1) == 1 and abs(y2 -y1) == 1 and abs((y2 -y1) / (x2-x1)) == 1:
            if board[x1][y1].team == True and x2 > x1:
                if board[x2 - 1][y2] is not None and board[x2 - 1][y2].team != board[x1][y1].team:
                    temp = board[x2 - 1][y2]
                    if temp.enPassant:
                        moveInfo.pawnX = x2 - 1
                        moveInfo.pawnY = y2

                        capture = True
                        board[x2 - 1][y2] = None;

            elif board[x1][y1].team == False and x2 < x1:
                if board[x2 + 1][y2] is not None and board[x2 + 1][y2].team != board[x1][y1].team:
                    temp = board[x2 + 1][y2]
                    if temp.enPassant == True:
                        moveInfo.pawnX = x2 + 1
                        moveInfo.pawnY = y2

                        capture = True
                        board[x2 + 1][y2] = None

        return capture


    def isCastling(self,x1,y1,x2,y2,board,moveInfo):
        castling = False
        clearSpace = True
        tempKing = board[x1][y1]
        tempRook = None


        if y1 - y2 == -2 and x1 == x2:

            if board[x1][self.width - 1] is not None and isinstance(board[x1][self.width - 1],Rook):
                tempRook = board[x1][self.width - 1]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(y1 + 1,self.width - 1):
                        if board[x1][i] is not None or (i <= y2 and self.Capture(x1, i, board[x1][y1].team, board)):
                            clearSpace = False
                else:
                    clearSpace = False

            if clearSpace == True:

                moveInfo.rookStartX = x1
                moveInfo.rookStartY = self.width - 1
                moveInfo.rookEndX = x1
                moveInfo.rookEndY = y2 - 1

                board[x1][y2-1],board[x1][self.width - 1] = board[x1][self.width - 1],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        elif y1 - y2 == 2 and x1 == x2:

            if board[x1][0] is not None and isinstance(board[x1][0],Rook):
                tempRook = board[x1][0]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(y1 - 1,0,-1):
                        if board[x1][i] is not None or (i >= y2 and self.Capture(x1, i, board[x1][y1].team, board)):
                            clearSpace = False

                else:
                    clearSpace = False

            if clearSpace:

                moveInfo.rookStartX = x1
                moveInfo.rookStartY = 0
                moveInfo.rookEndX = x1
                moveInfo.rookEndY = y2 + 1

                board[x1][y2 + 1],board[x1][0] = board[x1][0],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        return castling


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
            if self.Capture(self.blackKingX,self.blackKingY,False, board):
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

        stopped = False
        kx = 0
        ky = 0

        if board[x][y].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        # checking if the king can capture the piece putting it in check
        if board[kx][ky].ValidMove(kx,ky,x,y,board) and not self.allyKinginCheck(kx,ky,x,y,board):
            stopped = True

        # checking if the piece putting the king in check can be captured
        for i in range(8):
            for j in range(8):
                if board[i][j] is not None and board[i][j].team == board[x][y].team and board[i][j].ValidMove(i, j, x, y, board) and not self.allyKinginCheck(kx, ky, x, y, board):
                    stopped = True

        if not isinstance(board[x][y],Knight) and stopped == False:
            yMove = 0
            xMove = 0
            tempX = x
            tempY = y

            if x > kx:
                xMove = -1
            else:
                xMove = 1
            if y > ky:
                yMove = -1
            else:
                yMove = 1

            while tempX + xMove != kx or tempY + yMove != ky:
                tempX += xMove
                tempY += yMove
                for i in range(8):
                    for j in range(8):
                        if board[i,j] is not None:
                            if not isinstance(board[i][j], King) and board[i][j].team != board[x, y].team and board[i][j].ValidMove(i, j,tempX, tempY, board) and not self.AllyKinginCheck(i, j, tempX, tempY, board):
                                stopped = True;
        return stopped


    def FindCheckPieces(self,team,board):
        kx = 0
        ky = 0

        if team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY
        self.Capture(kx,ky,board[kx][ky].team,board)

    def Capture(self,x,y,team,board):
        check = False
        checkPiece = False

        for i in range(8):
            for j in range(8):
                checkPiece = False
                if board[i][j] is not None and board[i][j].team != team:
                    if isinstance(board[i][j],Pawn):

                        if abs(x - i) <= 1 and abs(y -j) <= 1 and abs(y - j) / abs(x - i) == 1:
                            if board[i][j].team and y > j:
                                check = True
                                checkPiece = True
                            elif board[i][j].team and y < j:
                                check = True
                                checkPiece = True
                            if checkPiece == True and board[x][y] is not None and isinstance(board[x][y],King):
                                self.checkPieces.append((i,j))
                    elif board[i][j].ValidMove(i,j,x,y,board):
                        check = True
                        if board[i][j] is not None and isinstance(board[i][j],King):
                            self.checkPieces.append((i,j))
        return check


    def removePieces(self,tempPiece,moveInfo,livePieces,whitePieces,blackPieces,board):
        livePieces.remove(tempPiece)
        if tempPiece.team:
            whitePieces.remove(tempPiece)
        else:
            blackPieces.remove(tempPiece)

        tempBool = False

        tempBool = start_new_thread(self.insufficientMaterial,(livePieces,whitePieces,blackPieces,board))

        if tempBool:
            moveInfo.Draw = True


    def insufficientMaterial(self,livePieces,whitePieces,blackPieces,board):
        if len(livePieces) == 2:
            return True
        elif len(livePieces) == 3:
            for piece in livePieces:
                if isinstance(piece,Bishop) or isinstance(piece,Knight):
                    return True
        elif len(whitePieces) == 2 and len(blackPieces) == 2:
            bishops = [piece for piece in livePieces if isinstance(piece,Bishop)]

            if len(bishops) == 2:
                wbx = 0
                wby = 0
                bbx = 0
                bby = 0

                for i in range(8):
                    for j in range(8):
                        if isinstance(board[i][j],Bishop):
                            if board[i][j].team:
                                wbx = i
                                wby = j
                            else:
                                bbx = i
                                bby = j
                if ((wbx*8) + wby)%2 == ((bbx*8) + bby)%2:
                    return True
        return False

    def updateEnemyPieces(self, moveInfo, board,livePieces,whitePieces,blackPieces):
        tempPawn2 = None
        tempPiece = None

        #castling
        if moveInfo.Castling == True:
            board[moveInfo.rookEndX][moveInfo.rookEndY] = board[moveInfo.rookStartX][moveInfo.rookStartY]
            board[moveInfo.rookStartX][ moveInfo.rookStartY] = None

            board[moveInfo.endX][moveInfo.endY] = board[moveInfo.startX][moveInfo.startY]
            board[moveInfo.startX][moveInfo.startY] = None

            if board[moveInfo.endX][moveInfo.endY].team == True:

                self.whitekingX = moveInfo.endX;
                self.whitekingY = moveInfo.endY;
            else:
                self.blackKingX = moveInfo.endX;
                self.blackKingY = moveInfo.endY;
        #enPassant
        elif moveInfo.enPassant == True:
            board[moveInfo.endX][moveInfo.endY] = board[moveInfo.startX][moveInfo.startY]
            board[moveInfo.startX][moveInfo.startY] = None

            self.removePieces(board[moveInfo.pawnX][moveInfo.pawnY], moveInfo, livePieces, whitePieces, blackPieces, board)
            board[moveInfo.pawnX][moveInfo.pawnY] = None
        #promotion
        elif moveInfo.promotion == True:
            tempPiece = board[moveInfo.startX, moveInfo.startY]
            if moveInfo.pawnEvolvesTo == "Queen":
                board[moveInfo.startX][moveInfo.startY] = Queen(board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Knight":
                board[moveInfo.startX][moveInfo.startY] = Knight(board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Bishop":
                board[moveInfo.startX][moveInfo.startY] = Bishop(board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Rook":
                board[moveInfo.startX][moveInfo.startY] = Rook(board[moveInfo.startX][moveInfo.startY].team)

            livePieces.remove(tempPiece)
            livePieces.append(board[moveInfo.startX][moveInfo.startY])

            if tempPiece.team:
                whitePieces.remove(tempPiece)
                whitePieces.append(board[moveInfo.startX][moveInfo.startY])

            else:
                blackPieces.remove(tempPiece)
                blackPieces.append(board[moveInfo.startX][moveInfo.startY])
        #regular move
        else:
            if isinstance(board[moveInfo.startX][moveInfo.startY],King):
                if board[moveInfo.startX][moveInfo.startY].team == True:
                    self.whitekingX = moveInfo.endX
                    self.whitekingY = moveInfo.endY

                else:

                    self.blackKingX = moveInfo.endX;
                    self.blackKingY = moveInfo.endY;
            elif isinstance(board[moveInfo.startX][moveInfo.startY], Pawn):
                if abs(moveInfo.startY - moveInfo.endY) == 2 and (
                        (moveInfo.startX > 0 and isinstance(board[moveInfo.endX - 1][moveInfo.endY],Pawn)) or (
                        moveInfo.startX < self.width - 1 and isinstance(board[moveInfo.endX + 1][moveInfo.endY], Pawn))):
                    if tempPawn2 is not None:
                        if tempPawn2.enPassant == True:
                            tempPawn2.enPassant = False
                    tempPawn2 = board[moveInfo.startX][moveInfo.startY]
                    tempPawn2.enPassant = True
            else:
                if tempPawn2 is not None:
                    if tempPawn2.enPassant == True:
                        tempPawn2.enPassant = False
                    tempPawn2 = None

        if board[moveInfo.endX][moveInfo.endY] is not None and board[moveInfo.startX][moveInfo.startY] is not None and board[
            moveInfo.startX][moveInfo.startY].team != board[moveInfo.endX][moveInfo.endY].team:
                tempPiece = board[moveInfo.endX][moveInfo.endY]
        temp = board[moveInfo.startX][moveInfo.startY]
        board[moveInfo.startX][moveInfo.startY] = None
        board[moveInfo.endX][moveInfo.endY] = temp

        if tempPiece is not None:
            self.removePieces(tempPiece,moveInfo,livePieces,whitePieces,blackPieces,board)

        #checks
        if moveInfo.check == True:
            kx = 0
            ky = 0
            if board[moveInfo.endX][moveInfo.endY].team:
                kx = self.blackKingX
                ky = self.blackKingY
            else:
                kx = self.whitekingX
                ky = self.whitekingY
        else:
            kx = 0
            ky = 0
            if board[moveInfo.endX][moveInfo.endY].team:
                kx = self.blackKingX
                ky = self.blackKingY
            else:
                kx = self.whitekingX
                ky = self.whitekingY

    def allyPieces(self,x1,y1,x2,y2,board):
        if board[x2][y2] is None:
            return False
        if board[x1][y1].team == board[x2][y2].team:
            return True
        else:
            return False

    def Promotion(self,x,y,board,moveInfo,yPos):
        promoteChoices = [Queen(board[x][y].team),Knight(board[x][y].team),Bishop(board[x][y].team),Rook(board[x][y].team)]

        board[x][y] = promoteChoices[yPos]
        if isinstance(promoteChoices[yPos],Queen):
            moveInfo.pawnEvolvesTo = "Queen"
        elif isinstance(promoteChoices[yPos],Knight):
            moveInfo.pawnEvolvesTo = "Knight"
        elif isinstance(promoteChoices[yPos],Bishop):
            moveInfo.pawnEvolvesTo = "Bishop"
        elif isinstance(promoteChoices[yPos],Rook):
            moveInfo.pawnEvolvesTo = "Rook"


