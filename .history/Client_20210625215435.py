import pygame
from Board import Board
from movement import Movement
from Game import Game
from Queen import Queen
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
import os
from network import Network
from threading import Thread
from multiprocessing import Process, Value, Pool
import asyncio

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Client")

pygame.font.init()

game = Game(0,3,8 - 1,3,0)

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

def redrawWindow(board,x,y,click,playerTeam):
    drawBoard(win)

    board.boardUpdate(win,playerTeam)
    #game.board.boardUpdate(win,playerTeam)

    # white player rotation
    if playerTeam:
        win.blit(pygame.transform.flip(win,True,True), (0, 0))
    if click:
        x,y = y,x
        if playerTeam:
            x = 7 - x
            y = 7 - y
        pygame.draw.circle(win, 'green',(round((SCREEN_WIDTH / 2 - (60 * 4)) + (60 * y) + 60/2), round((SCREEN_HEIGHT / 2 - (60 * 4)) + (60 * x)) + 60/2), 30, width=4)

    pygame.display.update()

def drawPromoteWindow(b,x,y,board):

    promoteChoices = [Queen(board.getTeam(x, y)), Knight(board.getTeam(x, y)),
                      Bishop(board.getTeam(x, y)), Rook(board.getTeam(x, y))]
    # promoteChoices = [Queen(game.board.getTeam(x,y)), Knight(game.board.getTeam(x,y)), Bishop(game.board.getTeam(x,y)),
    #                   Rook(game.board.getTeam(x,y))]
    pygame.draw.rect(win, 'green', ((700 / 2) - 70 / 2, (700 / 2) - 250 / 2, 70, 250))
    for i in range(4):
        image = pygame.image.load(os.path.join(os.path.dirname(__file__) + "\images", promoteChoices[i].name))
        image = pygame.transform.scale(image, (60, 60))

        win.blit(image, ((700 / 2) - 65 / 2, (700 / 2) - 250 / 2 + 60 * i))
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

async def WaitForMove(n,run,playerTeam):
    temp = None
    run = True
    #await asyncio.sleep(1)

    try:
        temp = n.send("get")

    except:
        run = False
        print("Couldn't get game")

    return temp, run



async def main():
#def main():

    run = True

    n = Network()
    movement = n.getBoard()
    print(n.getBoard())
    playerTeam = movement.playerTeam
    print(playerTeam)
    board = movement.Board



    currPlayer = True

    click = False
    win.fill((120, 120, 120))
    win2 = pygame.transform.rotate(win,360)
    x,y = 0,0
    while run:
        if playerTeam != currPlayer:

            waiting = asyncio.create_task(WaitForMove(n,run,playerTeam))
            temp, run = await waiting

            #need this loop to actually interact with the window while waiting on the move information,
            # without it the window freezes while the player is waiting for the opponent's move
            # It took me way too long to figure this out T_T
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            board = temp.Board
            if temp.validMove and playerTeam == temp.playerTeam:
                if temp.checkMate or temp.Draw:
                    redrawWindow(board, 0, 0, False, playerTeam)
                    await EndGame(currPlayer, temp, n)
                    currPlayer = temp.playerTeam
                    temp = n.send("get")
                    board = temp.Board
                    redrawWindow(board, 0, 0, False, playerTeam)
                else:
                    redrawWindow(board, 0, 0, False, playerTeam)
                    currPlayer = temp.playerTeam




        else:
            move = False
            moveInfo = Movement()
            moveInfo.playerTeam = playerTeam
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    if chessLeft <= x <= chessRight and chessUp <= y <= chessDown:
                        if currPlayer:
                            y = 7 - int((y - chessLeft) / 60)
                            x = 7 - int((x - chessUp) / 60)
                        else:
                            y = int((y - chessLeft) / 60)
                            x = int((x - chessUp) / 60)

                        #if click == False and not game.board.isEmpty(y, x) and game.board.getTeam(y, x) == currPlayer:
                        if click == False and not board.isEmpty(y ,x) and board.getTeam(y,x) == playerTeam and playerTeam == currPlayer:
                            y1 = x
                            x1 = y
                            click = True

                        elif click:


                            y2 = x
                            x2 = y
                            #black player rotation
                            if playerTeam == False:
                                moveInfo.x1 = x1
                                moveInfo.y1 = y1
                                moveInfo.x2 = x2
                                moveInfo.y2 = y2

                            # white player rotation
                            else:
                                x1, y1, x2, y2 = x1, y1, x2, y2
                                moveInfo.x1 = x1
                                moveInfo.y1 = y1
                                moveInfo.x2 = x2
                                moveInfo.y2 = y2


                            moveInfo.Board = board
                            try:
                                moveInfo = n.send(moveInfo)

                            except:
                                run = False
                                print("Couldn't get game")
                                break

                            board = moveInfo.Board
                            move = moveInfo.validMove

                            click = False

                            if move == True:

                                # #if game.board.isPawn(x2,y2)and (x2 == 0 or x2 == 7 ):
                                # #   yPos = drawPromoteWindow(game.board, x2, y2)
                                # if board.isPawn(x2,y2)and (x2 == 0 or x2 == 7 ):
                                #     yPos = drawPromoteWindow(board,x2,y2, board)
                                #     game.Promotion(x2, y2,moveInfo,yPos)
                                #
                                # game.enemyChecks(x2, y2,moveInfo)
                                #
                                #
                                if moveInfo.checkMate or moveInfo.Draw:
                                    redrawWindow(board, x, y, click, playerTeam)

                                    await EndGame(currPlayer, moveInfo, n)

                                if currPlayer:
                                    currPlayer = False
                                else:
                                    currPlayer = True




        #redrawWindow(game.board,x,y,click,currPlayer)
        redrawWindow(board,x,y,click,playerTeam)


async def EndGame(currPlayer, moveInfo, n):
    font = pygame.font.SysFont("comicsans", 60)
    if moveInfo.Draw:
        text = font.render("Its a draw", 1, "red")
        win.blit(text, (
        round(SCREEN_WIDTH / 2) - round(text.get_width() / 2), round(SCREEN_HEIGHT / 2) - round(text.get_height() / 2)))
    elif currPlayer:
        text = font.render("White Player Wins", 1, "red")
        win.blit(text, (
        round(SCREEN_WIDTH / 2) - round(text.get_width() / 2), round(SCREEN_HEIGHT / 2) - round(text.get_height() / 2)))
    else:
        text = font.render("Black Player Wins", 1, "red")
        win.blit(text, (
        round(SCREEN_WIDTH / 2) - round(text.get_width() / 2), round(SCREEN_HEIGHT / 2) - round(text.get_height() / 2)))
    pygame.display.update()
    run2 = True
    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                temp = n.send("restart")
                currPlayer = temp.playerTeam
                print(currPlayer)
                run2 = False


asyncio.run(main())
#main()