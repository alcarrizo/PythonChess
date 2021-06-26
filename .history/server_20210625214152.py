import socket
from threading import Thread
from Game import Game
import pickle
from movement import Movement

server = "192.168.1.122"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0



def threaded_client(conn,tempMovement,gameId):
    global idCount
    restart = False
    #conn.send(str.encode("test"))
    conn.sendall(pickle.dumps(tempMovement))

    reply = ""
    while True:
        moveInfo = Movement()
        try:
            data = pickle.loads(conn.recv(8192))

            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "restart":
                        if restart == False:
                            games[gameId] = Game(0, 3, 8 - 1, 3, gameId)
                            restart = True
                        moveInfo.playerTeam = game.currPlayer
                        #if game.newGame == False:
                         #   game.restart()

                    elif data != "get":
                        restart = False

                        if game.Move(data.x1,data.y1,data.x2,data.y2,data,data.playerTeam):
                            moveInfo.playerTeam = game.currPlayer
                            moveInfo.validMove = game.validMove
                            if game.enemyChecks(data.x2,data.y2,data):
                                moveInfo.checkMate = True
                            if data.playerTeam:
                                data.playerTeam = False
                            else:
                                data.playerTeam = True

                        else:
                            moveInfo.validMove = False
                            pass
                    elif data == "get":
                        moveInfo.validMove = game.validMove
                        moveInfo.playerTeam = game.currPlayer
                        moveInfo.checkMate = game.check_mate
                       # print("server: " + str(game.validMove) + "  moveinfo:" + str(moveInfo.validMove))


                    moveInfo.Board = game.board

                    reply = moveInfo
                    conn.sendall(pickle.dumps(reply))
            else:
                break

        except:
            break
    print("lost Connection")


    try:
        del games[gameId]
        print("Closing game",gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("connected to:", addr)

    idCount += 1
    p = 0
    gameId = int((idCount - 1)/2)
    if idCount%2 == 1:
        games[gameId] = Game(0, 3, 8 - 1, 3, gameId)
        print("creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    tempMovement = Movement()
    tempMovement.Board = games[gameId].board
    if p == 0:
        tempMovement.playerTeam = True
    else:
        tempMovement.playerTeam = False

    t = Thread(target = threaded_client, args = (conn,tempMovement, gameId))
    t.start()
    #start_new_thread(threaded_client, (conn,p, gameId))
