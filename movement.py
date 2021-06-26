from Board import Board

class Movement:
    def __init__(self):
        self.check = False
        self.checkMate = False
        self.forfeit = False
        self.askForDraw = False
        self.enPassant = False
        self.castling = False
        self.promotion = False
        self.Draw = False
        self.askForRematch = False
        self.Rematch = False
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.playerTeam = False
        self.Board = None
        self.move = False
        self.validMove = False
