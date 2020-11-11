from movement import Movement

class Game:
    def __init__(self,wkx,wky,bkx,bky):
        self.whitekingX = wkx
        self.whitekingY = wky
        self.blackKingX = bkx
        self.blackKingY = bky
        self.checkPieces = []

    def Move(self,x1,y1,x2,y2,board,moveInfo):
        pass

    def isEnpassant(self,x1,y1,x2,y2,board,moveInfo):
        pass

    def isCastling(self,x1,y1,x2,y2,board,moveInfo):
        pass

    def enemyChecks(self,x2,y2,board,moveInfo):
        pass

    def allyKinginCheck(self,x1,y1,x2,y2,board):
        pass

    def enemyKinginCheck(self,x2,y2,board):
        pass

    def checkMate(self,x,y,board):
        pass

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