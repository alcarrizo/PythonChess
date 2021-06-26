from movement import Movement
from Pawn import Pawn
from Bishop import Bishop
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from _thread import *
from threading import Thread
import queue
from Board import Board


class Game:
    def __init__(self,wkx,wky,bkx,bky,id):
        self.whitekingX = wkx
        self.whitekingY = wky
        self.blackKingX = bkx
        self.blackKingY = bky
        self.checkPieces = []
        self.width = 8
        self.height = 8
        self.tempPawn = None
        self.whitePieces = []
        self.blackPieces = []
        self.livePieces = []
        self.id = id
        self.board = Board()
        self.getPieces()
        self.currPlayer = True
        self.validMove = False
        self.check_mate = False
        self.newGame = False
        
    def getPieces(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.board.board[i][j] is not None and self.board.board[i][j]:
                    if self.board.board[i][j].team:
                        self.whitePieces.append(self.board.board[i][j])
                        self.livePieces.append(self.board.board[i][j])
                    else:
                        self.blackPieces.append(self.board.board[i][j])
                        self.livePieces.append(self.board.board[i][j])

    def Move(self,x1,y1,x2,y2,moveInfo,currPlayer):
        enPassant = False
        move = False
        tempPiece = None
        self.validMove = False
#        if self.board.board[x1][y1] is not None and self.board.board[x1][y1].team == currplayer:
        if not self.allyPieces(x1,y1,x2,y2) and not self.allyKinginCheck(x1,y1,x2,y2):
            if self.board.board[x1][y1] is not None:
                if (self.board.board[x2][y2] is not None and self.board.board[x1][y1].team != self.board.board[x2][y2].team) or \
                        self.board.board[x2][y2] is None:
                    tempPiece = self.board.board[x2][y2]

                #standard move
                if self.board.board[x1][y1].ValidMove(x1, y1, x2, y2, self.board.board):
                    move = True

                    if isinstance(self.board.board[x1][y1],King):

                        if self.board.board[x1][y1].team:
                            self.whitekingX = x2
                            self.whitekingY = y2
                        else:
                            self.blackKingX = x2
                            self.blackKingY = y2

                        tempKing = self.board.board[x1][y1]
                        tempKing.firstMove = False
                    elif isinstance(self.board.board[x1][y1],Rook):
                        tempRook = self.board.board[x1][y1]
                        tempRook.firstMove = False
                    elif isinstance(self.board.board[x1][y1], Pawn):
                        if abs(x1-x2) == 2 and ((y1 > 0 and isinstance(self.board.board[x2][y2-1],Pawn)) or (y1 < self.width - 1 and isinstance(self.board.board[x2][y2+1],Pawn))):
                            if self.tempPawn is not None:
                                if self.tempPawn.enPassant:
                                    self.tempPawn.enPassant = False
                            self.enPassant = True
                            self.tempPawn = self.board.board[x1][y1]
                            self.tempPawn.enPassant = True
                #check castling
                elif(isinstance(self.board.board[x1][y1],King)) and self.isCastling(x1,y1,x2,y2,moveInfo):
                    move = True
                    if self.board.board[x1][y1].team:
                        self.whitekingX = x2
                        self.whitekingY = y2
                    else:
                        self.blackKingX = x2
                        self.blackKingY = y2
                    moveInfo.castling = True
                #check enPassant
                elif(isinstance(self.board.board[x1][y1],Pawn)) and self.isEnpassant(x1,y1,x2,y2,moveInfo):
                    move = True
                    moveInfo.enPassant = True

                if move == True:
                    self.board.board[x1][y1], self.board.board[x2][y2] = None, self.board.board[x1][y1]

                    if enPassant == True and self.tempPawn is not None:
                        if self.tempPawn.enPassant:
                            self.tempPawn.enPassant = False
                        tempPawn = None
        if tempPiece is not None:

            self.removePieces(tempPiece,moveInfo)

        if move:
            self.validMove = True
            self.newGame = False
            if self.currPlayer:
                self.currPlayer = False
            else:
                self.currPlayer = True
        else:
            self.validMove = False

        return move


    def isEnpassant(self,x1,y1,x2,y2,moveInfo):
        capture = False

        if abs(x2-x1) == 1 and abs(y2 -y1) == 1 and abs((y2 -y1) / (x2-x1)) == 1:
            if self.board.board[x1][y1].team == True and x2 > x1:
                if self.board.board[x2 - 1][y2] is not None and self.board.board[x2 - 1][y2].team != self.board.board[x1][y1].team:
                    temp = self.board.board[x2 - 1][y2]
                    if temp.enPassant:
                        moveInfo.pawnX = x2 - 1
                        moveInfo.pawnY = y2

                        capture = True
                        self.board.board[x2 - 1][y2] = None;

            elif self.board.board[x1][y1].team == False and x2 < x1:
                if self.board.board[x2 + 1][y2] is not None and self.board.board[x2 + 1][y2].team != self.board.board[x1][y1].team:
                    temp = self.board.board[x2 + 1][y2]
                    if temp.enPassant == True:
                        moveInfo.pawnX = x2 + 1
                        moveInfo.pawnY = y2

                        capture = True
                        self.board.board[x2 + 1][y2] = None

        return capture


    def isCastling(self,x1,y1,x2,y2,moveInfo):
        castling = False
        clearSpace = True
        tempKing = self.board.board[x1][y1]
        tempRook = None


        if y1 - y2 == -2 and x1 == x2:

            if self.board.board[x1][self.width - 1] is not None and isinstance(self.board.board[x1][self.width - 1],Rook):
                tempRook = self.board.board[x1][self.width - 1]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(y1 + 1,self.width - 1):
                        if self.board.board[x1][i] is not None or (i <= y2 and self.Capture(x1, i, self.board.board[x1][y1].team, self.board.board,False)):
                            clearSpace = False
                else:
                    clearSpace = False

            if clearSpace == True:

                moveInfo.rookStartX = x1
                moveInfo.rookStartY = self.width - 1
                moveInfo.rookEndX = x1
                moveInfo.rookEndY = y2 - 1

                self.board.board[x1][y2-1],self.board.board[x1][self.width - 1] = self.board.board[x1][self.width - 1],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        elif y1 - y2 == 2 and x1 == x2:

            if self.board.board[x1][0] is not None and isinstance(self.board.board[x1][0],Rook):
                tempRook = self.board.board[x1][0]

                if tempKing.firstMove and tempRook.firstMove:
                    for i in range(y1 - 1,0,-1):
                        if self.board.board[x1][i] is not None or (i >= y2 and self.Capture(x1, i, self.board.board[x1][y1].team, self.board.board,False)):
                            clearSpace = False

                else:
                    clearSpace = False

            if clearSpace:

                moveInfo.rookStartX = x1
                moveInfo.rookStartY = 0
                moveInfo.rookEndX = x1
                moveInfo.rookEndY = y2 + 1

                self.board.board[x1][y2 + 1],self.board.board[x1][0] = self.board.board[x1][0],None
                castling = True
                tempRook.firstMove = False
                tempKing.firstMove = False

        return castling


    def enemyChecks(self,x2,y2,moveInfo):
        mate = False

        if self.enemyKinginCheck(x2,y2,):
            moveInfo.check = True

            self.checkPieces.clear()
            self.FindCheckPieces(self.board.board[x2][y2].team)

            for point in self.checkPieces:
                if self.checkMate(point[0],point[1]):
                    self.check_mate = True
                    mate = True
        return mate

    def allyKinginCheck(self,x1,y1,x2,y2):
        if isinstance(self.board.board[x1][y1],King):
            if self.board.board[x1][y1].team:
                self.whitekingX = x2
                self.whitekingY = y2
            else:
                self.blackKingX = x2
                self.blackKingY = y2

        temp = self.board.board[x2][y2] # keeping piece to revert the change later
        self.board.board[x2][y2],self.board.board[x1][y1] = self.board.board[x1][y1],None

        if(self.board.board[x2][y2].team):
            if self.Capture(self.whitekingX,self.whitekingY,True,False):
                self.board.board[x1][y1] = self.board.board[x2][y2]
                self.board.board[x2][y2] = temp
                if isinstance(self.board.board[x1][y1],King):
                    self.whitekingX = x1
                    self.whitekingY = y1
                return True
            else:
                self.board.board[x1][y1],self.board.board[x2][y2] = self.board.board[x2][y2],temp
                if isinstance(self.board.board[x1][y1],King):
                    self.whitekingX = x1
                    self.whitekingY = y1
                return False
        else:
            if self.Capture(self.blackKingX,self.blackKingY,False, False):
                self.board.board[x1][y1] = self.board.board[x2][y2]
                self.board.board[x2][y2] = temp
                if isinstance(self.board.board[x1][y1],King):
                    self.blackKingX = x1
                    self.blackKingY = y1
                return True
            else:
                self.board.board[x1][y1],self.board.board[x2][y2] = self.board.board[x2][y2],temp
                if isinstance(self.board.board[x1][y1],King):
                    self.blackKingX = x1
                    self.blackKingY = y1
                return False


    def enemyKinginCheck(self,x2,y2):

        kx = 0
        ky = 0

        if self.board.board[x2][y2].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        if self.Capture(kx,ky,self.board.board[kx][ky].team,False):
            return True

        return False

    def checkMate(self,x,y):

        checkMate = True
        kx = 0
        ky = 0

        if self.stopCheck(x,y):
            checkMate = False

        if self.board.board[x][y].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        for i in range (-1,2):
            for j in range(-1, 2):
                if kx + i >= 0 and kx + i < self.width and ky + j >= 0 and ky + j < self.height and not(i == 0 and j == 0):
                    if not self.Capture(kx + i, ky + j, self.board.board[kx][ky].team, False) and not self.allyPieces(kx,ky, kx + i, ky + j) and self.board.board[kx][ky].ValidMove(kx,ky, kx + i,ky + j, self.board):
                        checkMate = False

        return checkMate

    def stopCheck(self,x,y):

        stopped = False
        kx = 0
        ky = 0

        if self.board.board[x][y].team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        # checking if the king can capture the piece putting it in check
        if self.board.board[kx][ky].ValidMove(kx,ky,x,y,self.board.board) and not self.allyKinginCheck(kx,ky,x,y):
            stopped = True

        # checking if the piece putting the king in check can be captured
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] is not None and self.board.board[i][j].team != self.board.board[x][y].team and self.board.board[i][j].ValidMove(i, j, x, y, self.board.board) and not self.allyKinginCheck(i, j, x, y):
                    stopped = True

        if not isinstance(self.board.board[x][y],Knight) and stopped == False:
            yMove = 0
            xMove = 0
            tempX = x
            tempY = y

            if x > kx:
                xMove = -1
            elif x < kx:
                xMove = 1
            if y > ky:
                yMove = -1
            elif y < ky:
                yMove = 1

            while (tempX + xMove != kx and 0 <= tempX + xMove < self.width) or (tempY + yMove != ky and 0 <= tempY + yMove < self.height):
                tempX += xMove
                tempY += yMove
                for i in range(8):
                    for j in range(8):
                        if self.board.board[i][j] is not None:
                            if not isinstance(self.board.board[i][j], King) and self.board.board[i][j].team != self.board.board[x][y].team and self.board.board[i][j].ValidMove(i, j,tempX, tempY, self.board.board) and not self.allyKinginCheck(i, j, tempX, tempY):
                                stopped = True;
        return stopped


    def FindCheckPieces(self,team):
        kx = 0
        ky = 0

        if team:
            kx = self.blackKingX
            ky = self.blackKingY
        else:
            kx = self.whitekingX
            ky = self.whitekingY

        self.Capture(kx,ky,self.board.board[kx][ky].team,True)

    def Capture(self,x,y,team,findChecks):
        check = False
        checkPiece = False

        for i in range(8):
            for j in range(8):
                checkPiece = False
                if self.board.board[i][j] is not None and self.board.board[i][j].team != team:
                    if isinstance(self.board.board[i][j],Pawn):

                        if abs(x - i) <= 1 and abs(y -j) <= 1 and x != i and abs(y - j) / abs(x - i) == 1:
                            if self.board.board[i][j].team and y > j:
                                check = True
                                checkPiece = True
                            elif not self.board.board[i][j].team and y < j:
                                check = True
                                checkPiece = True
                            if checkPiece == True and self.board.board[x][y] is not None and isinstance(self.board.board[x][y],King) and findChecks:
                                self.checkPieces.append((i,j))
                    elif self.board.board[i][j].ValidMove(i,j,x,y,self.board.board):
                        check = True
                        if self.board.board[x][y] is not None and isinstance(self.board.board[x][y],King) and findChecks:
                            self.checkPieces.append((i,j))
        return check


    def removePieces(self,tempPiece,moveInfo):


        self.livePieces.remove(tempPiece)
        if tempPiece.team:
            self.whitePieces.remove(tempPiece)
        else:
            self.blackPieces.remove(tempPiece)

        tempBool = False

        que = queue.Queue()
        t = Thread(target=lambda q, arg1: q.put(self.insufficientMaterial(arg1)),
                   args=(que, self.board.board))
        t.start()

        t.join()
        tempBool = que.get()

        if tempBool:
            moveInfo.Draw = True


    def insufficientMaterial(self,board):
        if len(self.livePieces) == 2:
            return True
        elif len(self.livePieces) == 3:
            for piece in self.livePieces:
                if isinstance(piece,Bishop) or isinstance(piece,Knight):
                    return True
        elif len(self.whitePieces) == 2 and len(self.blackPieces) == 2:
            bishops = [piece for piece in self.livePieces if isinstance(piece,Bishop)]

            if len(bishops) == 2:
                wbx = 0
                wby = 0
                bbx = 0
                bby = 0

                for i in range(8):
                    for j in range(8):
                        if isinstance(self.board.board[i][j],Bishop):
                            if self.board.board[i][j].team:
                                wbx = i
                                wby = j
                            else:
                                bbx = i
                                bby = j
                if ((wbx*8) + wby)%2 == ((bbx*8) + bby)%2:
                    return True
        return False

    def updateEnemyPieces(self, moveInfo):
        tempPawn2 = None
        tempPiece = None

        #castling
        if moveInfo.Castling == True:
            self.board.board[moveInfo.rookEndX][moveInfo.rookEndY] = self.board.board[moveInfo.rookStartX][moveInfo.rookStartY]
            self.board.board[moveInfo.rookStartX][ moveInfo.rookStartY] = None

            self.board.board[moveInfo.endX][moveInfo.endY] = self.board.board[moveInfo.startX][moveInfo.startY]
            self.board.board[moveInfo.startX][moveInfo.startY] = None

            if self.board.board[moveInfo.endX][moveInfo.endY].team == True:

                self.whitekingX = moveInfo.endX
                self.whitekingY = moveInfo.endY
            else:
                self.blackKingX = moveInfo.endX
                self.blackKingY = moveInfo.endY
        #enPassant
        elif moveInfo.enPassant == True:
            self.board.board[moveInfo.endX][moveInfo.endY] = self.board.board[moveInfo.startX][moveInfo.startY]
            self.board.board[moveInfo.startX][moveInfo.startY] = None

            self.removePieces(self.board.board[moveInfo.pawnX][moveInfo.pawnY], moveInfo)
            self.board.board[moveInfo.pawnX][moveInfo.pawnY] = None
        #promotion
        elif moveInfo.promotion == True:
            tempPiece = self.board.board[moveInfo.startX, moveInfo.startY]
            if moveInfo.pawnEvolvesTo == "Queen":
                self.board.board[moveInfo.startX][moveInfo.startY] = Queen(self.board.board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Knight":
                self.board.board[moveInfo.startX][moveInfo.startY] = Knight(self.board.board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Bishop":
                self.board.board[moveInfo.startX][moveInfo.startY] = Bishop(self.board.board[moveInfo.startX][moveInfo.startY].team)
            if moveInfo.pawnEvolvesTo == "Rook":
                self.board.board[moveInfo.startX][moveInfo.startY] = Rook(self.board.board[moveInfo.startX][moveInfo.startY].team)

            self.livePieces.remove(tempPiece)
            self.livePieces.append(self.board.board[moveInfo.startX][moveInfo.startY])

            if tempPiece.team:
                self.whitePieces.remove(tempPiece)
                self.whitePieces.append(self.board.board[moveInfo.startX][moveInfo.startY])

            else:
                self.blackPieces.remove(tempPiece)
                self.blackPieces.append(self.board.board[moveInfo.startX][moveInfo.startY])
        #regular move
        else:
            if isinstance(self.board.board[moveInfo.startX][moveInfo.startY],King):
                if self.board.board[moveInfo.startX][moveInfo.startY].team == True:
                    self.whitekingX = moveInfo.endX
                    self.whitekingY = moveInfo.endY

                else:

                    self.blackKingX = moveInfo.endX;
                    self.blackKingY = moveInfo.endY;
            elif isinstance(self.board.board[moveInfo.startX][moveInfo.startY], Pawn):
                if abs(moveInfo.startY - moveInfo.endY) == 2 and (
                        (moveInfo.startX > 0 and isinstance(self.board.board[moveInfo.endX - 1][moveInfo.endY],Pawn)) or (
                        moveInfo.startX < self.width - 1 and isinstance(self.board.board[moveInfo.endX + 1][moveInfo.endY], Pawn))):
                    if tempPawn2 is not None:
                        if tempPawn2.enPassant == True:
                            tempPawn2.enPassant = False
                    tempPawn2 = self.board.board[moveInfo.startX][moveInfo.startY]
                    tempPawn2.enPassant = True
            else:
                if tempPawn2 is not None:
                    if tempPawn2.enPassant == True:
                        tempPawn2.enPassant = False
                    tempPawn2 = None

        if self.board.board[moveInfo.endX][moveInfo.endY] is not None and self.board.board[moveInfo.startX][moveInfo.startY] is not None and self.board.board[
            moveInfo.startX][moveInfo.startY].team != self.board.board[moveInfo.endX][moveInfo.endY].team:
                tempPiece = self.board.board[moveInfo.endX][moveInfo.endY]
        temp = self.board.board[moveInfo.startX][moveInfo.startY]
        self.board.board[moveInfo.startX][moveInfo.startY] = None
        self.board.board[moveInfo.endX][moveInfo.endY] = temp

        if tempPiece is not None:
            self.removePieces(tempPiece,moveInfo)

        #checks
        if moveInfo.check == True:
            kx = 0
            ky = 0
            if self.board.board[moveInfo.endX][moveInfo.endY].team:
                kx = self.blackKingX
                ky = self.blackKingY
            else:
                kx = self.whitekingX
                ky = self.whitekingY
        else:
            kx = 0
            ky = 0
            if self.board.board[moveInfo.endX][moveInfo.endY].team:
                kx = self.blackKingX
                ky = self.blackKingY
            else:
                kx = self.whitekingX
                ky = self.whitekingY

    def allyPieces(self,x1,y1,x2,y2):
        if self.board.board[x2][y2] is None:
            return False
        if self.board.board[x1][y1].team == self.board.board[x2][y2].team:
            return True
        else:
            return False

    def Promotion(self,x,y,moveInfo,yPos):
        promoteChoices = [Queen(self.board.board[x][y].team),Knight(self.board.board[x][y].team),Bishop(self.board.board[x][y].team),Rook(self.board.board[x][y].team)]

        tempPiece = self.board.board[x][y]
        self.board.board[x][y] = promoteChoices[yPos]
        if isinstance(promoteChoices[yPos],Queen):
            moveInfo.pawnEvolvesTo = "Queen"
        elif isinstance(promoteChoices[yPos],Knight):
            moveInfo.pawnEvolvesTo = "Knight"
        elif isinstance(promoteChoices[yPos],Bishop):
            moveInfo.pawnEvolvesTo = "Bishop"
        elif isinstance(promoteChoices[yPos],Rook):
            moveInfo.pawnEvolvesTo = "Rook"

        self.swapPieces(tempPiece,self.board.board[x][y],moveInfo)


    def swapPieces(self,tempPiece,newPiece,moveInfo):
        #self.livePieces.remove(tempPiece)
        self.livePieces.remove(tempPiece)
        self.livePieces.append(newPiece)

        if tempPiece.team:
            self.whitePieces.remove(tempPiece)
            self.whitePieces.append(newPiece)
        else:
            self.blackPieces.remove(tempPiece)
            self.blackPieces.append(newPiece)

    def restart(self):
        self.board = Board()
        self.newGame = True
        self.currPlayer = True
        self.validMove = False
        self.check_mate = False



