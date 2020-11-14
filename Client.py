import pygame
from Board import Board
from movement import Movement
from Game import Game
from Queen import Queen
from Knight import Knight
from Bishop import Bishop
from Rook import Rook

from network import Network

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Client")

pygame.font.init()

game = Game(0,3,8 - 1,3)

def drawBoard(win):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 != 0:
                col = (0, 100, 200)
            else:
                col = (255, 255, 255)
            pygame.draw.rect(win, col, ( (SCREEN_WIDTH/2 - (60*4)) +(60 * j), (SCREEN_HEIGHT/2 - (60*4)) + (60*i), 60, 60))


# getting the border of the chess board to help find mouse position
chessLeft, chessUp = (SCREEN_WIDTH/2 - (60*4)),(SCREEN_HEIGHT/2 - (60*4))
chessRight, chessDown = (SCREEN_WIDTH/2 - (60*4))+(60 * 8),(SCREEN_HEIGHT/2 - (60*4))+  (60*8)

def redrawWindow(b):
    drawBoard(win)

    b.boardUpdate(win)

    # white player rotation
    # win.blit(pygame.transform.flip(win,True,True), (0, 0))

    pygame.display.update()

def drawPromoteWindow(b,x,y):
    promoteChoices = [Queen(b.getTeam(x,y)), Knight(b.getTeam(x,y)), Bishop(b.getTeam(x,y)),
                      Rook(b.getTeam(x,y))]
    pygame.draw.rect(win, 'green', ((700 / 2) - 70 / 2, (700 / 2) - 250 / 2, 70, 250))
    for i in range(4):
        win.blit(promoteChoices[i].surf, ((700 / 2) - 65 / 2, (700 / 2) - 250 / 2 + 60 * i))
    pygame.display.update()
    chessLeft, chessUp = (700 / 2 - 70 / 2), (700 / 2 - 250 / 2)
    chessRight, chessDown = (700 / 2 - 70 / 2 + 70), ((700 / 2 - 250 / 2) + 250)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if chessLeft <= mx <= chessRight and chessUp <= my <= chessDown:
                    yPos = int((my - chessUp) / 60)
                    run = False
    return yPos

def main():
    run = True

   # n = Network()
    #playerNum = n.getP()
    #if playerNum == 0:
     #   playerTeam = True
   # else:
    #    playerTeam = False

    currPlayer = True
    b = Board()
    game.getPieces(b.board)

    click = False
    win.fill((120, 120, 120))
    win2 = pygame.transform.rotate(win,360)

    while run:
        move = False
        moveInfo = Movement()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if chessLeft <= x <= chessRight and chessUp <= y <= chessDown:
                    if click == False and not b.isEmpty(int((y - chessUp)/60),int((x - chessLeft) /60)):
                        y1 = x - chessLeft
                        x1 = y - chessUp
                        click = True
                        #print(int(x1/60),int(y1/60))
                    elif click:
                        y2 = x - chessLeft
                        x2 = y - chessUp
                        #black player rotation
                        #if b.move(int(x1/60),int(y1/60),int(x2/60),int(y2/60),moveInfo,currPlayer,win):
                        if game.Move(int(x1 / 60), int(y1 / 60), int(x2 / 60), int(y2 / 60),b.board, moveInfo, currPlayer):

                            move = True
                        else:
                            move = False
                        #white player rotation
                        #b.move(7 - int(x1 / 60), 7 - int(y1 / 60), 7 - int(x2 / 60),7 - int(y2 / 60))

                        if move == True:
                            click = False
                            if b.isPawn(int(x2/60),int(y2/60))and (int(x2/60) == 0 or int(x2/60) == 7 ):
                                yPos = drawPromoteWindow(b,int(x2/60),int(y2/60))
                                game.Promotion(int(x2/60),int(y2/60),b.board,moveInfo,yPos)

                            game.enemyChecks(int(x2/60),int(y2/60),b.board,moveInfo)


                            if moveInfo.checkMate or moveInfo.Draw:
                                redrawWindow(b)

                                font = pygame.font.SysFont("comicsans", 60)
                                if moveInfo.Draw:
                                    text = font.render("Its a draw",1,"red")
                                    win.blit(text,(round(SCREEN_WIDTH/2) - round(text.get_width()/2),round(SCREEN_HEIGHT/2) - round(text.get_height()/2)))
                                elif currPlayer:
                                    text = font.render("White Player Wins",1,"red")
                                    win.blit(text,(round(SCREEN_WIDTH/2) - round(text.get_width()/2),round(SCREEN_HEIGHT/2) - round(text.get_height()/2)))
                                else:
                                    text = font.render("Black Player Wins", 1, "red")
                                    win.blit(text,(round(SCREEN_WIDTH/2) - round(text.get_width()/2),round(SCREEN_HEIGHT/2) - round(text.get_height()/2)))
                                pygame.display.update()
                                run2 = True
                                while run2:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            run2 = False
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            b = Board()
                                            run2 = False

                        if currPlayer:
                            currPlayer = False
                        else:
                            currPlayer = True




        redrawWindow(b)



main()